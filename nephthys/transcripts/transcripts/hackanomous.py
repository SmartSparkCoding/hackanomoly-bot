from nephthys.transcripts.transcript import Transcript


class Hackanomous(Transcript):
    """Transcript for Hackanomous."""

    program_name: str = "Hackanomous"
    program_owner: str = "U0AEYDUCLKF" # @Jacob

    help_channel: str = "C0AHTT4DQ82"  # #hackanomous-help
    ticket_channel: str = "C0AJRR7EPR6"  # #hackanomous-tickets
    team_channel: str = "C0AJRR7EPR6"  # #hackanomous-support-team

    faq_link: str = "https://hackclub.slack.com/docs/T0266FRGM/F0AHN2A5EFM"
    identity_help_channel: str = "C092833JXKK"  # #identity-help

    first_ticket_create: str = f"""
:hackanomoly-v1: Hey there (user), welcome to the Hackanomous help channel. While we wait for a human helper, a couple of quick things:
• Take a look through <{faq_link}|*the FAQ*> – you may find a solution waiting there for you
• If you have the answer to your question, hit that green button below!
"""
    ticket_create: str = f"""
:hackanomoly-v1: Quick check-in while we wait for a helper:
• Have a read of <{faq_link}|*the FAQ*> – it might have the answer you're looking for
• Once your question is (hopefully) answered, hit the button below!
"""
    ticket_resolve: str = f"""
Oh, :yayayayayay: ! This post has just been marked as resolved by <@{{user_id}}>! I'll go away and do whatever bots do now, \
but if you need any more help, just send another message in <#{help_channel}> and I'll be right back for you o/
"""

    faq_macro: str = f"""
Hi (user), this question is already answered in our FAQ! Here's the link again: <{faq_link}|*Hackanomous FAQ*>.

_I've marked this question as resolved for you, so please start a new thread if you need more help_
"""
    identity_macro: str = f"""
Hey (user), please ask identity verification questions in <#{identity_help_channel}>. :hackanomoly-v1:

That keeps the verification team organized.

_I've marked this thread as resolved btw!_
"""
    redirect_macro: str = "Oh! I will now tell the big boss people to come help you! (usergroup)"
    fraud_macro: str = """
Hey (user), send any fraud-related questions to <@U091HC53CE8>. :hackanomoly-v1:

That keeps your case confidential and easier for the fraud team to track.

_I've marked this thread as resolved btw!_
"""

    not_allowed_channel: str = f"hey, it looks like you're not supposed to be in that channel, pls talk to <@{program_owner}> if that's wrong"

    ship_cert_queue_macro: str | None = (
        "Hey (user), we currently have a backlog of projects waiting to be reviewed. Please be patient but we will be with you ASAP!\n>!"
    )