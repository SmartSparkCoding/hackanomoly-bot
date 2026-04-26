from nephthys.utils.env import env
from nephthys.views.home.components.error_screen import error_screen
from nephthys.views.home.components.header import get_header
from prisma.models import User


async def get_category_tags_view(user: User | None):
    header = get_header(user, "category-tags")
    is_admin = bool(user and user.admin)

    if not user or not user.helper:
        return error_screen(
            header,
            ":rac_info: you're not a helper!",
            ":rac_believes_in_theory_about_green_lizards_and_space_lasers: only helpers can use ticket categories right now.",
        )

    category_tags = await env.db.categorytag.find_many(include={"tickets": True})

    if not category_tags:
        blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": ":rac_info: Category Tags",
                    "emoji": True,
                },
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": ":rac_nooo: no category tags yet.",
                },
            },
        ]

        if is_admin:
            blocks.append(
                {
                    "type": "actions",
                    "elements": [
                        {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": ":rac_cute: add a category tag?",
                                "emoji": True,
                            },
                            "action_id": "create-category-tag",
                            "style": "primary",
                        }
                    ],
                }
            )

        return {"type": "home", "blocks": [*header, *blocks]}

    blocks = [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": ":rac_info: Category Tags",
                "emoji": True,
            },
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": ":rac_thumbs: AI picks one category tag per new ticket to help classify it.",
            },
        },
        {"type": "divider"},
    ]

    if is_admin:
        blocks.append(
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": ":rac_cute: add a category tag?",
                            "emoji": True,
                        },
                        "action_id": "create-category-tag",
                        "style": "primary",
                    }
                ],
            }
        )
        blocks.append({"type": "divider"})

    for tag in category_tags:
        ticket_count = len(tag.tickets) if tag.tickets else 0
        blocks.append(
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*{tag.name}*\n{ticket_count} ticket{'s' if ticket_count != 1 else ''}",
                },
            }
        )
        blocks.append({"type": "divider"})

    return {
        "type": "home",
        "blocks": [
            *header,
            *blocks,
        ],
    }
