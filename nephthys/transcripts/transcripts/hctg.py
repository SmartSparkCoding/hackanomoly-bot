from nephthys.transcripts.transcript import Transcript


class Hctg(Transcript):
    """Transcript for Hack Club The Game"""

    program_name: str = "hctg"
    program_owner: str = "U01MPHKFZ7S"

    help_channel: str = "C0A9XULS1SL"  # hctg-help
    ticket_channel: str = "C0AF2HXHNSG"  # hctg-tickets
    team_channel: str = "C08B3M2DNSW"  # hack-club-the-game-internals

    faq_link: str = "https://hackclub.enterprise.slack.com/docs/T0266FRGM/F0AEVK71A69"

    first_ticket_create: str = f"""
Hey (user), welcome in. This looks like your first ticket here. Someone should be with you soon, but please check the <{faq_link}|faq> since it covers a lot of common questions.
If you are all set, use the button below to mark it as resolved.
"""
    ticket_create: str = f"Someone should be with you soon. In the meantime, check the faq <{faq_link}|here> to make sure your question has not already been answered. If it has, please use the button below to mark it as resolved."
    resolve_ticket_button: str = "got it"
    ticket_resolve: str = f"This post has been marked as resolved by <@{{user_id}}>. If you have more questions, make a new post in <#{help_channel}> and a helper will jump in."

    not_allowed_channel: str = f"Hey, it looks like you are not supposed to be in that channel. If that is wrong, please talk to <@{program_owner}>."
