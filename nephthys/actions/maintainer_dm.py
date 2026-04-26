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


def _extract_message_from_state(state: dict) -> str:
    message_state = state.get("message", {}).get("message", {})

    if isinstance(message_state.get("value"), str):
        return message_state["value"].strip()

    rich_text_value = message_state.get("rich_text_value")
    if isinstance(rich_text_value, dict):
        return _rich_text_to_plain_text(rich_text_value)

    if isinstance(message_state.get("value"), dict):
        return _rich_text_to_plain_text(message_state["value"])

    return ""


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

    state = body.get("view", {}).get("state", {}).get("values", {})
    recipient_id = (
        state.get("recipient", {}).get("recipient", {}).get("selected_user")
    )
    message = _extract_message_from_state(state)

    if not recipient_id or not message:
        await send_heartbeat(
            f"Maintainer DM submission was missing data for <@{user_id}>"
        )
        return

    try:
        await client.chat_postMessage(
            channel=recipient_id,
            text=message,
        )
    except Exception as e:
        await send_heartbeat(
            f"Failed to send maintainer DM from <@{user_id}> to <@{recipient_id}>: {e}"
        )
        return

    await send_heartbeat(
        f"Sent maintainer DM from <@{user_id}> to <@{recipient_id}>",
        messages=[message],
    )

    await open_app_home("maintainer-dm", client, user_id)