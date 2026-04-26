from pydantic import BaseModel
from pydantic import Field
from pydantic import model_validator


class Transcript(BaseModel):
    """Class to hold all the transcript messages and links used in the bot."""

    class Config:
        """Configuration for the Pydantic model."""

        extra = "forbid"

    program_name: str = Field(
        default="Summer of Making", description="Name of the program"
    )
    program_owner: str = Field(
        default="U054VC2KM9P",
        description="Slack ID of the support manager",
    )
    help_channel: str = Field(
        default="",
        description="Slack channel ID for help requests",
    )
    ticket_channel: str = Field(
        default="",
        description="Slack channel ID for ticket creation",
    )
    team_channel: str = Field(
        default="",
        description="Slack channel ID for team discussions and stats",
    )
    ticket_reopen: str = Field(
        default="",
        description="Message when ticket is reopened",
    )

    @property
    def program_snake_case(self) -> str:
        """Snake case version of the program name."""
        return self.program_name.lower().replace(" ", "_")

    faq_link: str = Field(
        default="https://hackclub.slack.com/docs/T0266FRGM/F093F8D7EE9",
        description="FAQ link URL",
    )

    summer_help_channel: str = Field(
        default="C091D312J85", description="Summer help channel ID"
    )

    identity_help_channel: str = Field(
        default="C092833JXKK", description="Identity help channel ID"
    )

    first_ticket_create: str = Field(
        default="", description="Message for first-time ticket creators"
    )

    ticket_create: str = Field(default="", description="Message for ticket creation")

    resolve_ticket_button: str = Field(
        default="Mark as resolved",
        description="Text for the green resolve-ticket button",
    )

    ticket_resolve: str = Field(
        default="", description="Message when ticket is resolved"
    )

    ticket_resolve_stale: str = Field(
        default="",
        description="Message when ticket is resolved due to being stale",
    )

    thread_broadcast_delete: str = Field(
        default="hey! please keep your messages *all in one thread* to make it easier to read! i've gone ahead and removed that message from the channel for ya :D",
    )

    faq_macro: str = Field(
        default="", description="Message to be sent when the FAQ macro is used"
    )

    fraud_macro: str = Field(
        default="Hey (user)! Please send any fraud-related questions to <@U091HC53CE8>. :hackanomoly-v1:\n\nThat keeps your case confidential and makes it easier for the fraud team to track.",
        description="Message to be sent when the fraud macro is used",
    )

    shipwrights_macro: str = Field(
        default="Hey, (user)!\nPlease ask questions about project shipping or certifications in <#C099P9FQQ91>.\n\nThe Shipwrights Team will help with your question!",
        description="Message to be sent when the shipwrights macro is used",
    )

    identity_macro: str = Field(
        default="", description="Message to be sent when the identity macro is used"
    )

    redirect_macro: str = Field(
        default="Oh! I will now tell the big boss people to come help you! (usergroup)",
        description="Message to be sent when the redirect macro is used",
    )

    ship_cert_queue_macro: str | None = Field(
        default=None,
        description="Message to be sent when the ship cert queue macro is used (only applies to Flavortown and SoM)",
    )

    not_allowed_channel: str = Field(
        default="", description="Message for unauthorized channel access"
    )

    # this stuff is only required for summer of making, but it's easier to keep it here :p
    dm_magic_link_no_user: str = Field(
        default=":hackanomoly-v1: please provide the user you want me to dm",
        description="Message when no user provided for magic link DM",
    )

    dm_magic_link_error: str = Field(
        default="", description="Error message for magic link generation"
    )

    dm_magic_link_success: str = Field(
        default=":hackanomoly-v1: magic link sent! tell them to check their dms.",
        description="Success message for magic link DM",
    )

    dm_magic_link_message: str = Field(
        default=":hackanomoly-v1: hey there! here’s a magic link to get you unstuck.\n{magic_link}",
        description="Magic link DM message",
    )

    dm_magic_link_no_permission: str = Field(
        default="", description="No permission message for magic link command"
    )

    @model_validator(mode="after")
    def set_default_messages(self):
        """Set default values for messages that reference other fields"""
        if not self.first_ticket_create:
            self.first_ticket_create = f"""Hey (user), welcome in. This looks like your first ticket here. Someone should be with you shortly, but while you wait, check the FAQ <{self.faq_link}|here> since it covers a lot of common questions.
If you’re all set, use the button below to mark this as resolved.
    """

        if not self.ticket_create:
            self.ticket_create = f"""Someone should be with you soon. In the meantime, check the FAQ <{self.faq_link}|here> to make sure your question hasn’t already been answered. If it has, use the button below to mark it as resolved.
    """

        if not self.ticket_resolve:
            self.ticket_resolve = f"""This post was marked as resolved by <@{{user_id}}>. If you need anything else, make a new post in <#{self.help_channel}> and a human helper will jump in.
    """

        if not self.ticket_resolve_stale:
            self.ticket_resolve_stale = f""":hackanomoly-v1: this post is a bit old. If you still need help, please make a new post in <#{self.help_channel}> and a helper will take a look.
        """

        if not self.faq_macro:
            self.faq_macro = f"Hey (user), this question is already covered in the FAQ I sent earlier. Please take a look. :hackanomoly-v1:\n\n<{self.faq_link}|here it is again>"

        if not self.identity_macro:
            self.identity_macro = f"Hey (user), please ask identity verification questions in <#{self.identity_help_channel}>. :hackanomoly-v1:\n\nThat keeps the verification team organized."

        if not self.not_allowed_channel:
            self.not_allowed_channel = f"Hey, it looks like you’re not supposed to be in that channel. If that’s wrong, please talk to <@{self.program_owner}>."

        if not self.dm_magic_link_error:
            self.dm_magic_link_error = f":hackanomoly-v1: something went wrong while generating the magic link. Please bug <@{self.program_owner}> (status: {{status}})."

        if not self.dm_magic_link_no_permission:
            self.dm_magic_link_no_permission = f":hackanomoly-v1: you don’t have permission to use this command. Please bug <@{self.program_owner}> if you think this is a mistake."

        if not self.ticket_reopen:
            self.ticket_reopen = "Hey! <@{helper_slack_id}> reopened this post. Someone will be with you shortly."

        return self
