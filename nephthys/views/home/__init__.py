from dataclasses import dataclass


@dataclass
class View:
    name: str
    id: str
    maintainer_only: bool = False
    # Not today
    # render: Callable[[User | None], dict]


APP_HOME_VIEWS: list[View] = [
    View("Dashboard", "dashboard"),
    View("Guide", "guide"),
    View("Assigned Tickets", "assigned-tickets"),
    View("Team Tags", "team-tags"),
    View("DM User", "maintainer-dm", maintainer_only=True),
    View("My Stats", "my-stats"),
]
