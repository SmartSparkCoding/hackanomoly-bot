import pytz

from nephthys.utils.env import env
from nephthys.utils.ticket_methods import get_question_message_link
from nephthys.views.home.components.error_screen import error_screen
from nephthys.views.home.components.header import get_header
from prisma.enums import TicketStatus
from prisma.models import User


async def get_assigned_tickets_view(user: User | None):
    header = get_header(user, "assigned-tickets")

    if not user or not user.helper:
        return error_screen(
            header,
            ":hackanomoly-transparent: you are not a helper, which is a setup problem rather than a personality problem.",
            "Only helpers can be assigned to tickets, so there is nothing here for you yet.",
        )

    tickets = await env.db.ticket.find_many(
        where={"assignedToId": user.id, "NOT": [{"status": TicketStatus.CLOSED}]},
        include={"openedBy": True},
    )

    if not tickets:
        return error_screen(
            header,
            ":hackanomoly-transparent: no assigned tickets",
            "You do not have any assigned tickets right now. The queue is, for once, behaving itself.",
        )

    ticket_blocks = []
    for ticket in tickets:
        unix_ts = int(ticket.createdAt.timestamp())
        time_ago_str = f"<!date^{unix_ts}^opened {{ago}}|at {ticket.createdAt.astimezone(pytz.timezone('Europe/London')).strftime('%H:%M %Z')}>"
        opened_by_str = (
            f"<@{ticket.openedBy.slackId}>" if ticket.openedBy else "unknown user"
        )
        ticket_blocks.append(
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*{ticket.title}*\n _from {opened_by_str}. {time_ago_str}_",
                },
                "accessory": {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": ":hackanomoly-v1: view ticket",
                        "emoji": True,
                    },
                    "action_id": f"view-ticket-{ticket.msgTs}",
                    "url": get_question_message_link(ticket),
                    "value": ticket.msgTs,
                },
            }
        )
        ticket_blocks.append({"type": "divider"})

    return {
        "type": "home",
        "blocks": [
            *header,
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                        "text": ":hackanomoly-transparent: here are your assigned tickets",
                    "emoji": True,
                },
            },
            *ticket_blocks,
        ],
    }
