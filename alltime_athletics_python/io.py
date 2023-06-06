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
    pipe_compute_age_at_event,
    pipe_convert_dates,
    pipe_convert_time_to_seconds,
    pipe_drop_unwanted_columns,
    pipe_fix_dtype,
    pipe_fix_issue_with_half_marathon_distance,
    pipe_get_event_distance,
    pipe_get_percentage_wrt_world_record,
    pipe_get_wr_strength_by_comparing_with_tenth,
    pipe_give_same_name_to_100m_and_110m_hurdles,
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
    df_men_standard = import_running_only_events_gender(
        data_root, pipe_rename_columns_names_men, "men", "standard"
    ).with_columns(
        [
            pl.lit("male").alias("sex"),
            pl.lit("standard").alias("event type"),
        ]
    )
    df_women_standard = import_running_only_events_gender(
        data_root, pipe_rename_columns_names_women, "women", "standard"
    ).with_columns(
        [
            pl.lit("female").alias("sex"),
            pl.lit("standard").alias("event type"),
        ]
    )
    df_men_special = import_running_only_events_gender(
        data_root, pipe_rename_columns_names_men, "men", "special"
    ).with_columns(
        [
            pl.lit("male").alias("sex"),
            pl.lit("special").alias("event type"),
        ]
    )
    df_women_special = import_running_only_events_gender(
        data_root, pipe_rename_columns_names_women, "women", "special"
    ).with_columns(
        [
            pl.lit("female").alias("sex"),
            pl.lit("special").alias("event type"),
            pl.lit("").alias("wind"),
        ]
    )

    df = (
        pl.concat(
            [
                df_women_standard.pipe(pipe_reorder_and_select_subset_of_columns),
                df_men_standard.pipe(pipe_reorder_and_select_subset_of_columns),
                df_women_special.pipe(pipe_reorder_and_select_subset_of_columns),
                df_men_special.pipe(pipe_reorder_and_select_subset_of_columns),
            ]
        )
        .pipe(pipe_compute_age_at_event)
        .pipe(pipe_give_same_name_to_100m_and_110m_hurdles)
    )
    # remove duplicates
    df = df.filter(~df.is_duplicated())

    df = df.sort(
        "event type",
        "sex",
        "distance",
        "event",
        "rank",
        descending=[True, False, False, False, False],
    )

    return df


def import_running_only_events_gender(
    data_root: str,
    pipe_rename_column_names: Callable[[pl.DataFrame], pl.DataFrame],
    gender: str,
    event_type: str,
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
            for event in get_running_only_files(data_root, gender, event_type)
        ],
        how="diagonal",
    )


def get_running_only_files(data_root: str, gender: str, event_type: str) -> list[str]:
    files = [
        f
        for f in glob.glob(  # Get all csv files recursively.
            f"{data_root}/{gender}/{event_type}/*/legal/0*.csv", recursive=True
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
    return files
