import logging
from typing import Any
from typing import Dict

from slack_bolt.async_app import AsyncAck
from slack_sdk.web.async_client import AsyncWebClient

from nephthys.utils.env import env
from nephthys.utils.ticket_methods import get_backend_message_link
from nephthys.utils.ticket_methods import get_question_message_link


def _normalize_selected_tags(raw_tags: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {"name": tag["text"]["text"], "value": int(tag["value"])}
        for tag in raw_tags
        if "value" in tag
    ]


async def apply_team_tags(
    ticket_ts: str,
    selected_tags: list[dict[str, Any]],
    client: AsyncWebClient,
    user_id: str | None = None,
):
    ticket = await env.db.ticket.find_unique(
        where={"ticketTs": ticket_ts}, include={"tagsOnTickets": True, "openedBy": True}
    )
    if not ticket:
        logging.error(f"Failed to find ticket with ts {ticket_ts}.")
        return

    if user_id:
        user = await env.db.user.find_unique(where={"slackId": user_id})
        if not user or not user.helper:
            logging.warning(
                f"Unauthorized user attempted to assign team tag user_id={user_id}"
            )
            channel_id = env.slack_ticket_channel
            await client.chat_postEphemeral(
                channel=channel_id,
                user=user_id,
                text="You are not authorized to assign tags.",
            )
            return

    if ticket.tagsOnTickets:
        new_tags = [
            tag
            for tag in selected_tags
            if tag["value"] not in [t.tagId for t in ticket.tagsOnTickets]
        ]
        old_tags = [
            tag
            for tag in ticket.tagsOnTickets
            if tag.tagId not in [t["value"] for t in selected_tags]
        ]
    else:
        new_tags = selected_tags
        old_tags = []
    logging.info(f"New: {new_tags}, Old: {old_tags}")

    if new_tags:
        await env.db.tagsontickets.create_many(
            data=[{"tagId": tag["value"], "ticketId": ticket.id} for tag in new_tags]
        )

    if old_tags:
        await env.db.tagsontickets.delete_many(
            where={
                "tagId": {"in": [tag.tagId for tag in old_tags]},
                "ticketId": ticket.id,
            }
        )

    tag_subscriptions = await env.db.usertagsubscription.find_many(
        where={"tagId": {"in": [tag["value"] for tag in new_tags]}}
    )

    user_ids = [tag.userId for tag in tag_subscriptions]
    if user_id and user_id in user_ids:
        user_ids.remove(user_id)

    db_users = await env.db.user.find_many(where={"id": {"in": user_ids}})

    users = []
    for user in db_users:
        tag_ids = [tag.tagId for tag in tag_subscriptions if tag.userId == user.id]
        users.append(
            {
                "id": user.slackId,
                "tags": tag_ids,
            }
        )

    url = get_question_message_link(ticket)
    ticket_url = get_backend_message_link(ticket)

    for user in users:
        formatted_tags = ", ".join(
            [tag["name"] for tag in new_tags if tag["value"] in user["tags"]]
        )
        await client.chat_postMessage(
            channel=user["id"],
            text=(
                f"New ticket for {formatted_tags}! *{ticket.title}*\n"
                f"<{url}|ticket> <{ticket_url}|bts ticket>"
            ),
        )


async def assign_team_tag_callback(
    ack: AsyncAck, body: Dict[str, Any], client: AsyncWebClient
):
    await ack()
    user_id = body["user"]["id"]
    raw_tags = body["actions"][0]["selected_options"]
    tags = _normalize_selected_tags(raw_tags)
    logging.info(tags)
    await apply_team_tags(body["message"]["ts"], tags, client, user_id=user_id)
