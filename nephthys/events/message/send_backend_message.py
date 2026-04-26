from slack_sdk.web.async_client import AsyncWebClient

from nephthys.utils.env import env
from prisma.models import User


async def backend_message_blocks(
    author_user_id: str,
    msg_ts: str,
    past_tickets: int,
    current_team_tag_ids: list[int] | None = None,
    reopened_by: User | None = None,
) -> list[dict]:
    thread_url = f"https://hackclub.slack.com/archives/{env.slack_help_channel}/p{msg_ts.replace('.', '')}"

    initial_options = []
    if current_team_tag_ids:
        selected_tags = await env.db.tag.find_many(
            where={"id": {"in": current_team_tag_ids}}
        )
        initial_options = [
            {
                "text": {"type": "plain_text", "text": tag.name, "emoji": True},
                "value": str(tag.id),
            }
            for tag in selected_tags
        ]

    return [
        {
            "type": "input",
            "label": {"type": "plain_text", "text": "Team tags", "emoji": True},
            "element": {
                "action_id": "team-tag-list",
                "type": "multi_external_select",
                "placeholder": {"type": "plain_text", "text": "Select tags"},
                "min_query_length": 0,
                **({"initial_options": initial_options} if initial_options else {}),
            },
        },
        {
            "type": "context",
            "elements": [
                {
                    "type": "mrkdwn",
                    "text": (
                        f"Reopened by <@{reopened_by.slackId}>. Originally submitted by <@{author_user_id}>. <{thread_url}|View thread>."
                        if reopened_by
                        else f"Submitted by <@{author_user_id}>. They have {past_tickets} past tickets. <{thread_url}|View thread>."
                    ),
                }
            ],
        },
    ]


def backend_message_fallback_text(
    author_user_id: str,
    description: str,
    reopened_by: User | None = None,
) -> str:
    return (
        f"Reopened ticket from <@{author_user_id}>: {description}"
        if reopened_by
        else f"New question from <@{author_user_id}>: {description}"
    )


async def send_backend_message(
    author_user_id: str,
    msg_ts: str,
    description: str,
    past_tickets: int,
    client: AsyncWebClient,
    current_team_tag_ids: list[int] | None = None,
    reopened_by: User | None = None,
    display_name: str | None = None,
    profile_pic: str | None = None,
):
    """Send a "backend" message to the tickets channel with ticket details."""

    return await client.chat_postMessage(
        channel=env.slack_ticket_channel,
        text=backend_message_fallback_text(author_user_id, description, reopened_by),
        blocks=await backend_message_blocks(
            author_user_id,
            msg_ts,
            past_tickets,
            current_team_tag_ids=current_team_tag_ids,
            reopened_by=reopened_by,
        ),
        username=display_name,
        icon_url=profile_pic,
        unfurl_links=True,
        unfurl_media=True,
    )
