from slack_bolt.async_app import AsyncAck
from slack_sdk.web.async_client import AsyncWebClient

from nephthys.events.app_home_opened import open_app_home
from nephthys.utils.env import env
from nephthys.utils.logging import send_heartbeat
from nephthys.views.modals.maintainer_dm import get_maintainer_dm_modal


def _rich_text_to_plain_text(rich_text_value: dict) -> str:
    parts = []
    rich_text_elements = rich_text_value.get("elements", [])

    if isinstance(rich_text_elements, list):
        blocks = rich_text_elements
    else:
        blocks = []

    for block in blocks:
        if block.get("type") != "rich_text_section":
            continue

        for element in block.get("elements", []):
            element_type = element.get("type")

            if element_type == "text":
                parts.append(element.get("text", ""))
            elif element_type == "user":
                user_id = element.get("user_id")
                parts.append(f"<@{user_id}>")
            elif element_type == "channel":
                channel_id = element.get("channel_id")
                parts.append(f"<#{channel_id}>")
            elif element_type == "link":
                url = element.get("url", "")
                text = element.get("text") or url
                parts.append(f"<{url}|{text}>")
            elif element_type == "emoji":
                parts.append(f":{element.get('name', '')}:")

        parts.append("\n")

    return "".join(parts).strip()


async def maintainer_dm_btn_callback(
    ack: AsyncAck, body: dict, client: AsyncWebClient
):
    await ack()
    user_id = body["user"]["id"]

    if user_id != env.slack_maintainer_id:
        await send_heartbeat(f"Non-maintainer tried to open DM modal: <@{user_id}>")
        return

    trigger_id = body["trigger_id"]
    await client.views_open(trigger_id=trigger_id, view=get_maintainer_dm_modal())


async def maintainer_dm_view_callback(
    ack: AsyncAck, body: dict, client: AsyncWebClient
):
    await ack()
    user_id = body["user"]["id"]

    if user_id != env.slack_maintainer_id:
        await send_heartbeat(f"Non-maintainer tried to submit DM modal: <@{user_id}>")
        return

    state = body["view"]["state"]["values"]
    recipient_id = state["recipient"]["recipient"]["selected_user"]
    message_value = state["message"]["message"]["value"]

    if isinstance(message_value, dict):
        message = _rich_text_to_plain_text(message_value)
    else:
        message = str(message_value).strip()

    if not recipient_id or not message:
        await send_heartbeat(f"Maintainer DM submission was missing data for <@{user_id}>")
        return

    await client.chat_postMessage(
        channel=recipient_id,
        text=message,
    )

    await send_heartbeat(
        f"Sent maintainer DM from <@{user_id}> to <@{recipient_id}>",
        messages=[message],
    )

    await open_app_home("maintainer-dm", client, user_id)