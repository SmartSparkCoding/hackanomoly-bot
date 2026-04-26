import logging

from nephthys.utils.env import env
from nephthys.views.home.components.header import get_header
from prisma.models import User


async def get_team_tags_view(user: User | None) -> dict:
    header = get_header(user, "team-tags")
    is_admin = bool(user and user.admin)
    is_helper = bool(user and user.helper)
    tags = await env.db.tag.find_many(include={"userSubscriptions": True})
    blocks = []

    if not tags:
        blocks.append(
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                        "text": f":hackanomoly-v1: no team tags found{', but you can make one below' if is_admin else ''}",
                },
            }
        )

    for tag in tags:
        logging.info(f"Tag {tag.name} with id {tag.id} found in the database")
        logging.info(
            f"Tag {tag.name} has {len(tag.userSubscriptions) if tag.userSubscriptions else 0} subscriptions"
        )
        if tag.userSubscriptions:
            subIds = [user.userId for user in tag.userSubscriptions]

            subUsers = await env.db.user.find_many(where={"id": {"in": subIds}})

            subs = [user.slackId for user in subUsers]
        else:
            subs = []
        stringified_subs = [f"<@{user}>" for user in subs]
        blocks.append(
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*{tag.name}* - {''.join(stringified_subs) if stringified_subs else ':hackanomoly-v1: no subscriptions'}",
                },
                "accessory": (
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": f":hackanomoly-v1: {'subscribe' if user.id not in subs else 'unsubscribe'}",
                            "emoji": True,
                        },
                        "action_id": "tag-subscribe",
                        "value": f"{tag.id};{tag.name}",
                        "style": "primary" if user.id not in subs else "danger",
                    }
                    if user and is_helper
                    else {}
                ),
            }
        )

    view = {
        "type": "home",
        "blocks": [
            *header,
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": ":hackanomoly-v1: Manage Team Tags",
                    "emoji": True,
                },
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                        "text": (
                            ":hackanomoly-v1: you can manage tags and subscriptions here"
                            if is_admin
                            else (
                                ":hackanomoly-v1: you can manage your subscriptions here"
                                if is_helper
                                else ":hackanomoly-v1: you can only view team tags"
                            )
                        ),
                },
            },
            {"type": "section", "text": {"type": "plain_text", "text": " "}},
            *blocks,
        ],
    }

    if is_admin:
        view["blocks"].append(
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": ":hackanomoly-v1: add a tag?",
                            "emoji": True,
                        },
                        "action_id": "create-team-tag",
                        "style": "primary",
                    }
                ],
            }
        )

    return view
