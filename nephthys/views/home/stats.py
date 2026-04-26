from nephthys.views.home.components.header import get_header
from prisma.models import User


async def get_stats_view(user: User | None):
    return {
        "type": "home",
        "blocks": [
            *get_header(user, "my-stats"),
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": ":rac_info: My Stats",
                    "emoji": True,
                },
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": ":hackanomoly-transparent: I do not have personal stats to show, but I can still help you find support data. I am, tragically, all business.",
                },
            },
        ],
    }
