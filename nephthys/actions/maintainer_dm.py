from slack_bolt.async_app import AsyncAck
from slack_sdk.web.async_client import AsyncWebClient

from nephthys.events.app_home_opened import open_app_home
from nephthys.utils.env import env
from nephthys.utils.logging import send_heartbeat
from nephthys.views.modals.maintainer_dm import get_maintainer_dm_modal


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
    message = state["message"]["message"]["value"].strip()

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