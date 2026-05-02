import logging
from datetime import date
from datetime import datetime
from datetime import timedelta
from zoneinfo import ZoneInfo

from nephthys.utils.env import env


RSVP_URL = "https://rsvp.ysws.workers.dev/rsvp/count"
RSVP_GOALS = [80, 90, 100, 115, 130, 150, 300]

_last_known_count: int | None = None
_current_day_start_count: int | None = None
_current_day: date | None = None
_last_completed_day: date | None = None
_last_completed_day_start_count: int | None = None
_last_completed_day_end_count: int | None = None
_last_summary_day: date | None = None
_announced_goals: set[int] = set()


def _london_now() -> datetime:
    return datetime.now(ZoneInfo("Europe/London"))


def _goal_progress(current_count: int) -> tuple[int | None, int | None, int | None]:
    previous_goal = 0
    for goal in RSVP_GOALS:
        if current_count < goal:
            return previous_goal, goal, goal - current_count
        previous_goal = goal
    return previous_goal, None, None


def _progress_bar(current_count: int) -> str:
    previous_goal, next_goal, _remaining = _goal_progress(current_count)
    if next_goal is None:
        return "██████████"

    span = max(next_goal - previous_goal, 1)
    progress = min(max(current_count - previous_goal, 0), span) / span
    filled = round(progress * 10)
    return "█" * filled + "░" * (10 - filled)


def _format_until_next_goal(current_count: int) -> str:
    _previous_goal, next_goal, remaining = _goal_progress(current_count)
    if next_goal is None:
        return "No goals left - incredible work."
    return f"{remaining} until the next goal of {next_goal}!"


def _update_day_rollover(current_count: int) -> None:
    global _current_day
    global _current_day_start_count
    global _last_completed_day
    global _last_completed_day_start_count
    global _last_completed_day_end_count

    london_today = _london_now().date()
    if _current_day is None:
        _current_day = london_today
        if _current_day_start_count is None:
            _current_day_start_count = current_count
        return

    if london_today != _current_day:
        _last_completed_day = _current_day
        _last_completed_day_start_count = _current_day_start_count
        _last_completed_day_end_count = _last_known_count if _last_known_count is not None else current_count
        _current_day = london_today
        _current_day_start_count = current_count


async def _post_message(text: str) -> None:
    if not env.slack_rsvp_channel:
        return

    await env.slack_client.chat_postMessage(channel=env.slack_rsvp_channel, text=text)


async def _fetch_current_count() -> int | None:
    try:
        async with env.session.get(RSVP_URL) as response:
            response.raise_for_status()
            payload = await response.json()
    except Exception as exc:
        logging.warning("Failed to fetch RSVP count: %s", exc, exc_info=True)
        return None

    count = payload.get("count")
    if not isinstance(count, int):
        logging.warning("RSVP API returned an invalid payload: %s", payload)
        return None

    return count


async def poll_rsvp_count():
    global _last_known_count

    if not env.slack_rsvp_channel:
        logging.debug("RSVP polling skipped: SLACK_RSVP_CHANNEL not set")
        return

    logging.info("RSVP polling started")
    current_count = await _fetch_current_count()
    if current_count is None:
        logging.warning("RSVP polling failed to fetch count")
        return

    logging.info(f"RSVP current count: {current_count}")
    _update_day_rollover(current_count)

    if _last_known_count is None:
        _last_known_count = current_count
        logging.info(f"RSVP initialized with count: {current_count}")
        return

    previous_count = _last_known_count
    if current_count <= _last_known_count:
        if current_count < _last_known_count:
            logging.info(f"RSVP count decreased from {_last_known_count} to {current_count}")
        _last_known_count = current_count
        return

    delta = current_count - _last_known_count
    _last_known_count = current_count

    until_next_goal = _format_until_next_goal(current_count)

    logging.info(f"RSVP increase detected: {delta} new RSVPs (total: {current_count})")
    await _post_message(
        f":incoming_envelope: {delta} new RSVP{'s' if delta != 1 else ''} just came in. Total: *{current_count}* RSVP{'s' if current_count != 1 else ''}. {until_next_goal}"
    )

    for goal in RSVP_GOALS:
        if previous_count < goal <= current_count and goal not in _announced_goals:
            _announced_goals.add(goal)
            logging.info(f"RSVP milestone {goal} reached!")
            await _post_message(
                f":tada::partyparrot: *We just hit {goal} RSVPs!!* Keep them coming! :fireworks:"
            )


async def send_rsvp_daily_summary():
    global _last_summary_day

    if not env.slack_rsvp_channel:
        return

    current_count = await _fetch_current_count()
    if current_count is None:
        return

    _update_day_rollover(current_count)

    london_today = _london_now().date()
    summary_day = london_today - timedelta(days=1)

    if _last_summary_day == summary_day:
        return

    summary_start_count: int | None = None
    summary_end_count: int | None = None

    if (
        _last_completed_day == summary_day
        and _last_completed_day_start_count is not None
        and _last_completed_day_end_count is not None
    ):
        summary_start_count = _last_completed_day_start_count
        summary_end_count = _last_completed_day_end_count
    elif _current_day == summary_day and _current_day_start_count is not None:
        summary_start_count = _current_day_start_count
        summary_end_count = current_count

    if summary_start_count is None or summary_end_count is None:
        logging.warning(
            "RSVP daily summary skipped because the day start count is unavailable."
        )
        return

    today_total = summary_end_count - summary_start_count
    _previous_goal, next_goal, _remaining = _goal_progress(current_count)
    progress_bar = _progress_bar(current_count)
    until_next_goal = _format_until_next_goal(current_count)

    if next_goal is None:
        goal_line = "All RSVP goals have been cleared."
    else:
        goal_line = f"Progress to {next_goal}: `{progress_bar}`"

    await _post_message(
        f"*:calendar: RSVP daily summary*\n"
        f"RSVPs today: *{today_total}*\n"
        f"Current total: *{current_count}*\n"
        f"{until_next_goal}\n"
        f"{goal_line}"
    )

    _last_summary_day = summary_day