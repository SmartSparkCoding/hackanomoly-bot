from datetime import timezone
from io import BytesIO

import numpy as np
from blockkit import Image

from nephthys.utils.bucky import upload_file
from nephthys.utils.env import env
from nephthys.utils.graphs.pie import generate_pie_chart
from nephthys.utils.performance import perf_timer
from nephthys.utils.time import is_day


async def generate_rsvp_progress_pie_image(
    current_count: int, next_goal: int, tz: timezone | None = None
) -> bytes:
    """Generates a pie chart showing RSVP progress toward the next goal."""
    is_daytime = is_day(tz) if tz else True

    if is_daytime:
        text_colour = "black"
        bg_colour = "white"
    else:
        text_colour = "white"
        bg_colour = "#181A1E"

    progress = min(current_count, next_goal)
    remaining = max(next_goal - current_count, 0)

    y = [progress]
    labels = [f"Progress ({current_count})"]
    colours = ["#00AA88"]

    if remaining > 0:
        y.append(remaining)
        labels.append(f"Remaining ({remaining})")
        colours.append("#CCCCCC")

    async with perf_timer("Building RSVP pie chart"):
        b = BytesIO()
        y_arr = np.array(y)
        plt = generate_pie_chart(
            y=y_arr,
            labels=labels,
            colours=colours,
            text_colour=text_colour,
            bg_colour=bg_colour,
        )

    async with perf_timer("Saving RSVP pie chart to buffer"):
        plt.savefig(
            b,
            bbox_inches="tight",
            pad_inches=0.1,
            transparent=False,
            dpi=300,
            format="png",
        )

    return b.getvalue()


async def rsvp_progress_pie_chart_component(
    current_count: int, next_goal: int, tz: timezone | None = None
):
    pie_chart_image = await generate_rsvp_progress_pie_image(
        current_count, next_goal, tz
    )

    async with perf_timer("Uploading RSVP pie chart"):
        url = await upload_file(
            file=pie_chart_image,
            filename="rsvp_progress.png",
            content_type="image/png",
        )

    if not url:
        return Image(
            image_url=f"{env.base_url}/public/binoculars.png",
            alt_text="Hackanomoly looking for RSVPs with binoculars",
            title="looks like hackanomoly is scrounging around for RSVPs",
        )

    return Image(image_url=url, alt_text="RSVP progress toward next goal")
