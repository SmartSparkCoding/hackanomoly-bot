from nephthys.transcripts.transcript import Transcript


class Flavortown(Transcript):
    """Transcript for Hack Club Flavortown."""

    program_name: str = "Flavortown"
    program_owner: str = "U073M5L9U13"  # @Mish

    help_channel: str = "C09MATKQM8C"  # #flavortown-help
    ticket_channel: str = "C09LS4SAWNB"  # #flavortown-tickets
    team_channel: str = "C09M16FHL0K"  # #flavortown-support-team

    faq_link: str = "https://hackclub.slack.com/docs/T0266FRGM/F09NKF58FL5"
    identity_help_channel: str = "C092833JXKK"  # #identity-help

    first_ticket_create: str = f"""
:hackanomoly-v1: Hey there (user), welcome to the support channel. While we wait for a human helper, a couple of quick things:
• Take a look through <{faq_link}|*the FAQ*> – you may find a solution waiting there
• Once your question has been answered, hit that green button below!
"""
    ticket_create: str = f"""
:hackanomoly-v1: Quick check-in while we wait for a helper:
• Have a read of <{faq_link}|*the FAQ*> – it might have the answer you're looking for
• Once your question is answered, hit the button below!
"""
    ticket_resolve: str = f"""
Aha, this post has just been marked as resolved by <@{{user_id}}>! I'll head back to the kitchen now, \
but if you need any more help, just send another message in <#{help_channel}> and I'll be right back o/
"""

    faq_macro: str = f"""
Hi (user), this question is already answered in our FAQ! Here's the link again: <{faq_link}|*Flavortown FAQ*>.

_I've marked this question as resolved, so please start a new thread if you need more help_
"""
    identity_macro: str = f"""
Hey (user), please ask identity verification questions in <#{identity_help_channel}>. :hackanomoly-v1:

That keeps the verification team organized.

_I've marked this thread as resolved_
"""
    fraud_macro: str = """
Hey (user), send any fraud-related questions to <@U091HC53CE8>. :hackanomoly-v1:

That keeps your case confidential and easier for the fraud team to track.

_I've marked this thread as resolved_
"""

    not_allowed_channel: str = f"hey, it looks like you're not supposed to be in that channel, pls talk to <@{program_owner}> if that's wrong"

    ship_cert_queue_macro: str | None = (
        "Hey (user), we currently have a backlog of projects waiting to be certified. Please be patient.\n\n*You can keep track of the queue <https://us.review.hackclub.com/queue | here>!*"
    )
