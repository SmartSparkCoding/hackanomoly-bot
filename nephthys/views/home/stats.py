import logging

import pytz
from blockkit import Header, Section
from blockkit import Home

from nephthys.utils.env import env
from nephthys.utils.performance import perf_timer
from nephthys.views.home.components.header import get_header_components
from nephthys.views.home.components.rsvp_progress_pie import (
    rsvp_progress_pie_chart_component,
)
from nephthys.views.home.error import get_error_view
from prisma.models import User


async def get_stats_view(user: User | None):
    """Displays RSVP statistics with progress toward the next goal."""
    try:
        # Fetch current RSVP count
        async with perf_timer("Fetching RSVP count"):
            current_count = await _fetch_rsvp_count()

        if current_count is None:
            return get_error_view(
                ":hackanomoly-transparent: I couldn't fetch RSVP data right now. Try again in a moment."
            )

        # Calculate goal progress
        previous_goal, next_goal, remaining = _calculate_goal_progress(current_count)

        # Get user's timezone for pie chart
        user_info_response = await env.slack_client.users_info(user=user.slackId) if user else None
        user_info = user_info_response.get("user") if user_info_response else None
        tz_string = user_info.get("tz") if user_info else None
        if not tz_string:
            tz_string = "Europe/London"
        tz = pytz.timezone(tz_string)

        # Generate pie chart
        async with perf_timer("Rendering RSVP progress pie chart"):
            if next_goal is None:
                # All goals reached
                pie_chart = None
                goal_text = ":tada: All RSVP goals have been reached! Incredible work!"
            else:
                pie_chart = await rsvp_progress_pie_chart_component(
                    current_count, next_goal, tz
                )
                goal_text = f":rocket: *{remaining}* RSVPs until goal *{next_goal}*"

        # Build blocks
        blocks = [
            *get_header_components(user, "my-stats"),
            Header(":incoming_envelope: RSVP Statistics"),
            Section(
                text=f"*Current RSVPs:* {current_count}\n{goal_text}\n*Previous Goal:* {previous_goal if previous_goal > 0 else 'N/A'}"
            ),
        ]

        if pie_chart:
            blocks.append(pie_chart)

        # Add milestones section
        milestones = _get_milestone_status(current_count)
        blocks.append(
            Section(
                text=f"*Goal Progress*\n{milestones}"
            )
        )

        return Home(blocks).build()

    except Exception as e:
        logging.error(f"Error rendering RSVP stats: {e}", exc_info=True)
        return get_error_view(
            ":hackanomoly-transparent: Something went wrong while fetching your RSVP stats."
        )


async def _fetch_rsvp_count() -> int | None:
    """Fetch current RSVP count from API."""
    try:
        async with env.session.get("https://rsvp.ysws.workers.dev/rsvp/count") as response:
            response.raise_for_status()
            payload = await response.json()
            count = payload.get("count")
            if isinstance(count, int):
                return count
    except Exception as e:
        logging.warning(f"Failed to fetch RSVP count: {e}")
    return None


def _calculate_goal_progress(current_count: int) -> tuple[int, int | None, int | None]:
    """Calculate previous goal, next goal, and remaining RSVPs."""
    RSVP_GOALS = [80, 90, 100, 115, 130, 150, 300]
    previous_goal = 0
    for goal in RSVP_GOALS:
        if current_count < goal:
            return previous_goal, goal, goal - current_count
        previous_goal = goal
    return previous_goal, None, None


def _get_milestone_status(current_count: int) -> str:
    """Generate a string showing which milestones have been reached."""
    RSVP_GOALS = [80, 90, 100, 115, 130, 150, 300]
    lines = []
    for goal in RSVP_GOALS:
        if current_count >= goal:
            lines.append(f":white_check_mark: {goal}")
        else:
            lines.append(f":white_circle: {goal}")
    return " ".join(lines)

