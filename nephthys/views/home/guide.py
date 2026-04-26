from nephthys.views.home.components.header import get_header
from prisma.models import User


async def get_guide_view(user: User | None) -> dict:
    return {
        "type": "home",
        "blocks": [
            *get_header(user, "guide"),
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": ":hackanomoly-transparent: Hackanomoly Guide",
                    "emoji": True,
                },
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Hackanomoly is mostly self-managed. Here is what it does today, plus helper macros and alias commands.",
                },
            },
            {"type": "divider"},
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "Core Features",
                    "emoji": True,
                },
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": (
                        "• *Duplicate guard*: closes a new ticket only when all 3 are true: same user, within 10 minutes, and related issue.\n"
                        "• *AI auto-categorization*: suggests and applies team tags based on ticket message content.\n"
                        "• *AI ticket titles*: generates a short title for each new ticket.\n"
                        "• *Tag subscriptions*: manage which team-tag pings you receive in the *Team Tags* tab.\n"
                        "• *Mention replies*: responds when you tag Hackanomoly in chat.\n"
                        "• *Maintainer DM tool (beta)*: DM users from App Home (currently maintainer-only).\n"
                        "• *Helper sync*: members in the support team channel are synced as helpers and can manage tickets.\n"
                        "• *Daily summaries*: posts daily stats around midnight (Europe/London).\n"
                        "• *Fulfillment reminder*: posts fulfillment-ticket reminders around 14:00 (Europe/London).\n"
                        "• *24h stale monitor*: checks hourly and alerts when tickets are open longer than 24 hours."
                    ),
                },
            },
            {"type": "divider"},
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "Helper Macros",
                    "emoji": True,
                },
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": (
                        "• *?resolve* / *?close*\n"
                        "Marks the ticket resolved, updates reactions, and cleans up the backend message/thread as configured.\n\n"
                        "• *?redirect* / *?admin*\n"
                        "Replies with a support-team user-group ping for escalation.\n\n"
                        "• *?ai* / *?ask-ai*\n"
                        "Sends ticket + thread context to AI and posts a draft support response with a close button.\n\n"
                        "• *?hii*\n"
                        "Friendly in-thread greeting.\n\n"
                        "• *?faq*\n"
                        "Posts your program FAQ link and resolves the ticket.\n\n"
                        "• *?identity*\n"
                        "Redirects identity-verification questions to the identity channel and resolves.\n\n"
                        "• *?fraud*\n"
                        "Redirects fraud-related questions to the fraud contact and resolves.\n\n"
                        "• *?shipqueue* / *?shipcert* / *?shipcertqueue*\n"
                        "Explains ship certification backlog/queue and resolves (if configured).\n\n"
                        "• *?thread*\n"
                        "Cleans bot replies/reaction clutter in-thread; resolves if still open.\n\n"
                        "• *?reopen* / *?unresolve* / *?open*\n"
                        "Reopens a closed ticket, recreates backend visibility, and updates reactions.\n\n"
                        "• *?shipwrights*\n"
                        "Redirects shipping/certification questions to the shipwrights channel and resolves."
                    ),
                },
            },
            {"type": "divider"},
            {
                "type": "context",
                "elements": [
                    {
                        "type": "mrkdwn",
                        "text": "Need changes to this guide text? Update this view in nephthys/views/home/guide.py.",
                    }
                ],
            },
        ],
    }