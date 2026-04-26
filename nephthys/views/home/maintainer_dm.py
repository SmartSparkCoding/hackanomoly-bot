from nephthys.utils.env import env
from nephthys.views.home.components.header import get_header
from prisma.models import User


async def get_maintainer_dm_view(user: User | None) -> dict:
    header = get_header(user, "maintainer-dm")

    if not user or user.slackId != env.slack_maintainer_id:
        return {
            "type": "home",
            "blocks": [
                *header,
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": ":hackanomoly-v1: this tab is only for the maintainer.",
                    },
                },
            ],
        }

    return {
        "type": "home",
        "blocks": [
            *header,
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": ":hackanomoly-v1: maintainer dm tool",
                    "emoji": True,
                },
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Pick a user and send them a direct message from the bot.",
                },
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": ":hackanomoly-v1: compose dm",
                            "emoji": True,
                        },
                        "action_id": "open-maintainer-dm",
                        "style": "primary",
                    }
                ],
            },
        ],
    }