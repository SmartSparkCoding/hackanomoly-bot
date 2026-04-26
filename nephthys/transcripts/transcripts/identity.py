from nephthys.transcripts.transcript import Transcript


class Identity(Transcript):
    """Transcript for identity-help"""

    program_name: str = "Identity"
    program_owner: str = "U054VC2KM9P"

    help_channel: str = "C092833JXKK"
    ticket_channel: str = "C093FV95GGJ"
    team_channel: str = "C091URN0G9G"

    faq_link: str = "https://hackclub.slack.com/docs/T0266FRGM/F0945AV6AKA"
    summer_help_channel: str = "C091D312J85"
    identity_help_channel: str = "C092833JXKK"

    first_ticket_create: str = f"""
Hey (user), welcome in. This looks like your first ticket here. Someone should be with you soon, but please check the <{faq_link}|faq> since it covers a lot of common questions.
If you are all set, use the button below to mark it as resolved.
"""
    ticket_create: str = f"Someone should be with you soon. In the meantime, check the faq <{faq_link}|here> to make sure your question has not already been answered. If it has, please use the button below to mark it as resolved."
    resolve_ticket_button: str = "got it"
    ticket_resolve: str = f"This post has been marked as resolved by <@{{user_id}}>. If you have more questions, make a new post in <#{help_channel}> and a helper will jump in."

    not_allowed_channel: str = f"Hey, it looks like you are not supposed to be in that channel. If that is wrong, please talk to <@{program_owner}>."
