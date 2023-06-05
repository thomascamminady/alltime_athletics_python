import glob
import os
from pathlib import Path
from typing import Callable

import polars as pl
from rich.progress import track

from alltime_athletics_python.get_content import get_content
from alltime_athletics_python.get_content_urls import get_content_urls
from alltime_athletics_python.pipes import (
    pipe_assign_file_name,
    pipe_assign_has_hurdles_or_not,
    pipe_assign_sprint_middle_long_distance,
    pipe_assign_track_event_or_not,
    pipe_convert_dates,
    pipe_convert_time_to_seconds,
    pipe_drop_unwanted_columns,
    pipe_fix_dtype,
    pipe_fix_issue_with_half_marathon_distance,
    pipe_get_event_distance,
    pipe_get_percentage_wrt_world_record,
    pipe_get_wr_strength_by_comparing_with_tenth,
    pipe_remove_all_null_columns,
    pipe_remove_invalid,
    pipe_rename_columns_names_men,
    pipe_rename_columns_names_women,
    pipe_reorder_and_select_subset_of_columns,
)


def download_data(folder: str = "./data"):
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


def import_running_only_events(data_root: str = "./data") -> pl.DataFrame:
    df_men = import_running_only_events_sex(
        data_root, pipe_rename_columns_names_men, "men"
    ).with_columns(pl.lit("men").alias("sex"))
    df_women = import_running_only_events_sex(
        data_root, pipe_rename_columns_names_women, "women"
    ).with_columns(pl.lit("women").alias("sex"))

    return pl.concat([df_women, df_men]).pipe(pipe_reorder_and_select_subset_of_columns)


def import_running_only_events_sex(
    data_root: str,
    pipe_rename_column_names: Callable[[pl.DataFrame], pl.DataFrame],
    sex: str,
) -> pl.DataFrame:
    return pl.concat(
        [
            pl.read_csv(event, infer_schema_length=10000)
            .pipe(pipe_assign_file_name, event)
            .pipe(pipe_rename_column_names)
            .pipe(pipe_fix_dtype)
            .pipe(pipe_convert_time_to_seconds)
            .pipe(pipe_remove_all_null_columns)
            .pipe(pipe_remove_invalid)
            .pipe(pipe_get_event_distance)
            .pipe(pipe_get_percentage_wrt_world_record)
            .pipe(pipe_assign_sprint_middle_long_distance)
            .pipe(pipe_assign_has_hurdles_or_not)
            .pipe(pipe_assign_track_event_or_not)
            .pipe(pipe_fix_issue_with_half_marathon_distance)
            .pipe(pipe_drop_unwanted_columns)
            .pipe(pipe_get_wr_strength_by_comparing_with_tenth)
            .pipe(pipe_convert_dates)
            for event in get_running_only_files(data_root, sex)
        ],
        how="diagonal",
    )


def get_running_only_files(data_root: str, sex: str) -> list[str]:
    return [
        f
        for f in glob.glob(  # Get all csv files recursively.
            f"{data_root}/{sex}/standard/*/legal/0*.csv", recursive=True
        )
        if (
            "metres" in f
            or "00m" in f
            or "Mile" in f
            or "One hour" in f
            or "km" in f
            or "marathon" in f
            or "110m" in f
        )
        and ("4x" not in f)
    ]
