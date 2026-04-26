from nephthys.transcripts.transcript import Transcript


class Jumpstart(Transcript):
    """Transcript for Hack Club Jumpstart"""

    program_name: str = "Jumpstart"
    program_owner: str = "U06UYA4AH6F"  # @ Magic Frog

    help_channel: str = "C0A620A4FGF"  # #jumpstart-help
    ticket_channel: str = "C0A7CCXC8AU"  # #jumpstart-tickets
    team_channel: str = "C0A6ELTS38V"  # #jumpstart-support-team

    faq_link: str = "https://hackclub.enterprise.slack.com/docs/T0266FRGM/F0A6AMXU744"
    identity_help_channel: str = "C092833JXKK"  # #identity-help
    readme_link: str = (
        "https://hackclub.enterprise.slack.com/docs/T0266FRGM/F0A6MFGFW56"
    )

    first_ticket_create: str = f"""
:hackanomoly-v1: Hey (user), I’m Godorpheus. While a human helper gets to your question, you can:
• Check out <{faq_link}|*the FAQ*> and <{readme_link}|*the README*> in case the answer is already there
• When your question is solved, hit the green button below so we can close the loop
"""
    ticket_create: str = f"""
:hackanomoly-v1: Hey (user), Godorpheus here. While we wait for a human helper:
• Take a peek at <{faq_link}|*the FAQ*> and <{readme_link}|*the README*> in case the answer is already there
• Once your question is resolved, tap the green button below to wrap it up
"""
    ticket_resolve: str = f"""
✅ This post has been marked as resolved by <@{{user_id}}>.
Need more help? Post in <#{help_channel}> and we’ll jump back in.
"""

    faq_macro: str = f"""
Hey (user), this question is already covered in the FAQ or README: <{faq_link}|*Jumpstart FAQ*> 🎮
<{readme_link}|*Jumpstart README*> 👾
_I’ve marked this thread as resolved. Start a new thread if you need more help._
"""
    identity_macro: str = f"""
Hey (user), for identity verification questions, please head over to <#{identity_help_channel}>. :hackanomoly-v1:

It keeps things tidy and makes it easier for the verification team to help.

_I’ve marked this thread as resolved!_
"""
    fraud_macro: str = """
Hey (user), fraud-related questions go to <@U08TU92QGHM> — they handle it securely 🛡️

_I’ve marked this thread as resolved to keep things organized._
"""

    not_allowed_channel: str = f"hey, it looks like you're not supposed to be in that channel, pls talk to <@{program_owner}> if that's wrong"
