import logging

from nephthys.utils.env import env
from nephthys.views.home.components.header import get_header
from prisma.models import User


async def get_user_profiles_view(user: User | None) -> dict:
    missing_profile_field = False
    try:
        users = await env.db.user.find_many(
            where={"ticketProfile": {"not": None}},
            order={"ticketProfileUpdatedAt": "desc"},
        )
    except Exception as e:
        # If the deployed schema/client is behind, don't crash App Home.
        if "ticketProfile" in str(e):
            logging.warning(
                f"User profile fields unavailable in Prisma schema yet: {e}"
            )
            users = await env.db.user.find_many(order={"createdAt": "desc"})
            missing_profile_field = True
        else:
            raise

    profile_blocks = []
    for profile_user in users[:50]:
        profile_text = getattr(profile_user, "ticketProfile", None)
        if not profile_text:
            profile_text = (
                "Profile summaries are not available yet on this deployment."
                if missing_profile_field
                else "No profile summary yet."
            )
        profile_blocks.append(
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"<@{profile_user.slackId}>\n{profile_text}",
                },
            }
        )
        profile_blocks.append({"type": "divider"})

    if not profile_blocks:
        profile_blocks.append(
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": ":hackanomoly-transparent: No user ticket profiles yet. They appear after users open tickets.",
                },
            }
        )

    return {
        "type": "home",
        "blocks": [
            *get_header(user, "user-profiles"),
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": ":hackanomoly-transparent: user ticket profiles",
                    "emoji": True,
                },
            },
            {
                "type": "context",
                "elements": [
                    {
                        "type": "mrkdwn",
                        "text": "One sentence per user, updated only when that user opens a new ticket.",
                    }
                ],
            },
            {"type": "divider"},
            *profile_blocks,
        ],
    }
