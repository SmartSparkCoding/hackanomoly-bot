import logging

from nephthys.utils.env import env
from nephthys.views.home.components.header import get_header
from prisma.models import User


def _fallback_user_ticket_profile(descriptions: list[str]) -> str:
    combined = " ".join(descriptions).lower()
    keywords = {
        "shipping": ["ship", "shipping", "cert", "certificate", "delivery"],
        "identity": ["identity", "verify", "verification", "kyc"],
        "fraud": ["fraud", "scam", "suspicious", "chargeback"],
        "ai": ["ai", "model", "prompt", "response"],
        "account": ["account", "login", "password", "access"],
    }
    counts = {
        label: sum(combined.count(token) for token in tokens)
        for label, tokens in keywords.items()
    }
    top = sorted(counts.items(), key=lambda item: item[1], reverse=True)[0][0]
    if counts[top] == 0:
        return "Usually opens support tickets across mixed topics and follows up when needed."
    if top == "shipping":
        return "Usually opens tickets about shipping or certification progress and queue status."
    if top == "identity":
        return "Usually opens tickets related to identity verification or account checks."
    if top == "fraud":
        return "Usually opens tickets related to suspicious activity and fraud concerns."
    if top == "ai":
        return "Usually opens tickets about AI behavior, responses, or prompt-related issues."
    return "Usually opens tickets related to account access and support setup issues."


async def _build_profiles_from_tickets(users: list[User]) -> dict[str, str]:
    user_ids = [profile_user.id for profile_user in users]
    if not user_ids:
        return {}

    recent_tickets = await env.db.ticket.find_many(
        where={"openedById": {"in": user_ids}},
        order={"createdAt": "desc"},
        take=500,
    )

    descriptions_by_user: dict[str, list[str]] = {user_id: [] for user_id in user_ids}
    for ticket in recent_tickets:
        if ticket.description and len(descriptions_by_user[ticket.openedById]) < 10:
            descriptions_by_user[ticket.openedById].append(ticket.description)

    return {
        user_id: _fallback_user_ticket_profile(descriptions)
        for user_id, descriptions in descriptions_by_user.items()
        if descriptions
    }


async def get_user_profiles_view(user: User | None) -> dict:
    missing_profile_field = False
    profiles_from_tickets: dict[str, str] = {}
    try:
        users = await env.db.user.find_many(
            where={"ticketProfile": {"not": None}},
            order={"ticketProfileUpdatedAt": "desc"},
        )
    except Exception as e:
        if "ticketProfile" in str(e):
            logging.warning(
                f"User profile fields unavailable in Prisma schema yet: {e}"
            )
            users = await env.db.user.find_many(order={"createdAt": "desc"})
            missing_profile_field = True
            profiles_from_tickets = await _build_profiles_from_tickets(users[:50])
        else:
            raise

    profile_blocks = []
    for profile_user in users[:50]:
        profile_text = getattr(profile_user, "ticketProfile", None)
        if not profile_text:
            profile_text = (
                profiles_from_tickets.get(profile_user.id)
                if missing_profile_field
                else "No profile summary yet."
            )
        if not profile_text:
            profile_text = "No profile summary yet."
        profile_blocks.append(
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"<@{profile_user.slackId}>\n{profile_text}",
                },
            }
        )
        profile_blocks.append({"type": "divider"})

    if not profile_blocks:
        profile_blocks.append(
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": ":hackanomoly-transparent: No user ticket profiles yet. They appear after users open tickets.",
                },
            }
        )

    return {
        "type": "home",
        "blocks": [
            *get_header(user, "user-profiles"),
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": ":hackanomoly-transparent: user ticket profiles",
                    "emoji": True,
                },
            },
            {
                "type": "context",
                "elements": [
                    {
                        "type": "mrkdwn",
                        "text": "One sentence per user, updated only when that user opens a new ticket.",
                    }
                ],
            },
            {"type": "divider"},
            *profile_blocks,
        ],
    }
