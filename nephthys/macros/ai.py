from pathlib import Path

from nephthys.macros.types import Macro
from nephthys.utils.env import env
from nephthys.utils.ticket_methods import reply_to_ticket


AI_CONTEXT_PATH = Path(__file__).resolve().parents[2] / "docs" / "ai_context.md"


def load_ai_context() -> str:
    if not AI_CONTEXT_PATH.exists():
        return ""

    context = AI_CONTEXT_PATH.read_text(encoding="utf-8").strip()
    if not context:
        return ""

    return context


class AI(Macro):
    name = "ai"
    aliases = ["ask-ai"]

    async def run(self, ticket, helper, **kwargs):
        """Ask AI to answer the current help thread using the thread context."""
        if not env.ai_client:
            await env.slack_client.chat_postEphemeral(
                channel=env.slack_help_channel,
                thread_ts=ticket.msgTs,
                user=helper.slackId,
                text="AI is not available right now.",
            )
            return

        thread_messages = await env.slack_client.conversations_replies(
            channel=env.slack_help_channel,
            ts=ticket.msgTs,
        )
        messages = thread_messages.get("messages", [])
        extra_context = load_ai_context()

        context_lines = [
            "Main message:",
            ticket.description,
            "",
            "Thread:",
        ]
        for message in messages:
            if message.get("ts") == ticket.msgTs:
                continue
            user = message.get("user", "unknown")
            text = message.get("text", "")
            if not text:
                continue
            context_lines.append(f"<@{user}>: {text}")

        if extra_context:
            context_lines.extend([
                "",
                "Extra context:",
                extra_context,
            ])

        prompt = "\n".join(context_lines)
        try:
            response = await env.ai_client.chat.completions.create(
                model="google/gemini-3-flash-preview",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are Hackanomoly, a concise but helpful support assistant for Hack Club. "
                            "Answer the user's issue using the main message and thread context. "
                            "Be direct, practical, and friendly. If the context is insufficient, say what is missing. "
                            "Return only the answer text. Do not include markdown headings."
                        ),
                    },
                    {"role": "user", "content": prompt},
                ],
            )
        except Exception as e:
            await env.slack_client.chat_postEphemeral(
                channel=env.slack_help_channel,
                thread_ts=ticket.msgTs,
                user=helper.slackId,
                text=f"AI failed to generate a response: {e}",
            )
            return

        answer = response.choices[0].message.content if response.choices else None
        if not answer:
            await env.slack_client.chat_postEphemeral(
                channel=env.slack_help_channel,
                thread_ts=ticket.msgTs,
                user=helper.slackId,
                text="AI did not return a response.",
            )
            return

        await reply_to_ticket(
            ticket=ticket,
            client=env.slack_client,
            text=f"*AI RESPONSE*\n{answer.strip()}",
            blocks=[
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*AI RESPONSE*\n{answer.strip()}",
                    },
                },
                {
                    "type": "actions",
                    "elements": [
                        {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": "Close ticket",
                                "emoji": True,
                            },
                            "style": "primary",
                            "action_id": "mark_resolved",
                            "value": ticket.msgTs,
                        }
                    ],
                },
            ],
        )
