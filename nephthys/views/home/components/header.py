from blockkit import Actions
from blockkit import Button
from blockkit import Divider
from blockkit import Header
from blockkit.core import ModalBlock

from nephthys.utils.env import env
from nephthys.views.home import APP_HOME_VIEWS
from prisma.models import User


def _can_see_maintainer_tabs(user: User | None) -> bool:
    return bool(user and user.slackId == env.slack_maintainer_id)


def header_buttons(user: User | None, current_view: str):
    buttons = Actions()

    for view in APP_HOME_VIEWS:
        if view.maintainer_only and not _can_see_maintainer_tabs(user):
            continue
        style = Button.PRIMARY if view.id == current_view else None
        buttons.add_element(
            Button(
                text=view.name,
                action_id=view.id,
                style=style,
            )
        )

    return buttons


def title_line():
    return Header(f":hackanomoly-v1: {env.app_title}")


def get_header(user: User | None, current: str = "dashboard") -> list[dict]:
    """Returns the app home header in Slack API JSON format

    Deprecated over using blockkit and `get_header_components()`
    """
    return [
        title_line().build(),
        header_buttons(user, current).build(),
        {"type": "divider"},
    ]


def get_header_components(
    user: User | None, current: str = "dashboard"
) -> list[ModalBlock]:
    """Returns the app home header as blockkit components"""
    return [
        title_line(),
        header_buttons(user, current),
        Divider(),
    ]
