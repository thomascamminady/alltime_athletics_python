# %%
import os
from pathlib import Path

import fire
from rich.progress import track

from alltime_athletics_python.get_content import get_content
from alltime_athletics_python.get_content_urls import get_content_urls


def parse(folder: str = "./data"):
    metadata = get_content_urls()

    Path(folder).mkdir(parents=True, exist_ok=True)
    metadata.to_csv(os.path.join(folder, "metadata.csv"))

    for i in track(
        range(len(metadata)),
        description="Downloading data from http://www.alltime-athletics.com:",
    ):
        row = metadata.iloc[i, :]
        list_of_content = get_content(row)
        for content in list_of_content:
            Path(os.path.join(folder, content.folder)).mkdir(
                parents=True, exist_ok=True
            )
            content.df.to_csv(os.path.join(folder, content.folder, content.filename))


if __name__ == "__main__":
    fire.Fire()
