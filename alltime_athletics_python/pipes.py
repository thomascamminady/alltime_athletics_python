import polars as pl

from alltime_athletics_python.events import event_list


def pipe_remove_invalid(df: pl.DataFrame) -> pl.DataFrame:
    return (
        df.sort("event", "rank")
        .with_columns(
            (
                pl.col("result seconds") >= pl.col("result seconds").over("event").min()
            ).alias("valid")
        )
        .filter(pl.col("valid"))
    )


def pipe_get_event_distance(df: pl.DataFrame) -> pl.DataFrame:
    def distance_mapping(event) -> float:
        d = {event.name: event.distance for event in event_list}
        return d[event]

    return df.with_columns(  # get event distances
        pl.col("event").apply(lambda e: distance_mapping(e)).alias("distance")
    )


def pipe_remove_all_null_columns(df: pl.DataFrame) -> pl.DataFrame:
    return df.drop([col.name for col in df if col.is_null().all()])


def pipe_get_percentage_wrt_world_record(df: pl.DataFrame) -> pl.DataFrame:
    return df.with_columns(  # add percentages w.r.t world records
        (
            100
            * (pl.col("result seconds") / pl.col("result seconds").min().over("event"))
        ).alias("percentage of wr")
    ).with_columns(
        pl.col("percentage of wr").rank().over("event").cast(int).alias("rank")
    )


def pipe_assign_sprint_middle_long_distance(df: pl.DataFrame) -> pl.DataFrame:
    def assign(event) -> str:
        d = {event.name: event.distance_type for event in event_list}
        return d[event]

    return df.with_columns(
        pl.col("event").apply(lambda e: assign(e)).alias("distance type")
    )


def pipe_assign_has_hurdles_or_not(df: pl.DataFrame) -> pl.DataFrame:
    def assign(event) -> bool:
        d = {event.name: event.has_hurdles for event in event_list}
        return d[event]

    return df.with_columns(
        pl.col("event").apply(lambda e: assign(e)).alias("has hurdles")
    )


def pipe_assign_track_event_or_not(df: pl.DataFrame) -> pl.DataFrame:
    def assign(event):
        d = {event.name: event.is_track for event in event_list}
        return d[event]

    return df.with_columns(pl.col("event").apply(lambda e: assign(e)).alias("on track"))


def pipe_fix_issue_with_half_marathon_distance(df: pl.DataFrame) -> pl.DataFrame:
    return df.with_columns(
        pl.when(pl.col("event") == "half-marathon")
        .then(42195 / 2)
        .otherwise(pl.col("distance"))
        .alias("distance")
    )


def pipe_convert_time_to_seconds(df: pl.DataFrame) -> pl.DataFrame:
    def convert_time_to_seconds(time_string):
        to_replace = ["A", "y", "+", "#", "a", "d", "´", "@", "p", "m", "*", "e"]
        for r in to_replace:
            time_string = time_string.replace(r, "")

        time_parts = time_string.split(":")
        if len(time_parts) == 3:  # hours:minutes:seconds
            return (
                int(time_parts[0]) * 3600
                + int(time_parts[1]) * 60
                + float(time_parts[2])
            )
        elif len(time_parts) == 2:  # minutes:seconds
            return int(time_parts[0]) * 60 + float(time_parts[1])
        else:  # seconds
            return float(time_parts[0])

    return df.with_columns(
        pl.col("result").apply(convert_time_to_seconds).alias("result seconds")
    )


def pipe_fix_dtype(df: pl.DataFrame) -> pl.DataFrame:
    return df.with_columns(pl.col("rank").cast(int))


def pipe_rename_columns_names_men(df: pl.DataFrame) -> pl.DataFrame:
    def decide_mapping_men(name, number_columns, mappings):
        if "200m hurdles" in name:
            return mappings[4]
        if "300 metres" in name:
            return mappings[5]
        if "half" in name:
            return mappings[2]
        if "1500" in name or "400m hurdles" in name:
            return mappings[3]
        if number_columns == 12:
            return mappings[0]

        return mappings[1]

    def get_mappings_men() -> list[dict[str, str]]:
        return [
            {
                "0": "rank",
                "1": "result",
                "2": "wind",
                "3": "name",
                "4": "nationality",
                "5": "date of birth",
                "6": "rank in event",
                "7": "location of event",
                "8": "date of event",
            },
            {
                "0": "rank",
                "1": "result",
                "2": "name",
                "3": "nationality",
                "4": "date of birth",
                "5": "rank in event",
                "6": "location of event",
                "7": "date of event",
            },
            {
                "0": "rank",
                "1": "result",
                "2": "name",
                "3": "nationality",
                "4": "date of birth",
                "5": "rank in event",
                "6": "location of event",
                "8": "date of event",
            },
            {
                "0": "rank",
                "1": "result",
                "2": "name",
                "4": "nationality",
                "5": "date of birth",
                "6": "rank in event",
                "7": "location of event",
                "8": "date of event",
            },
            {
                "0": "rank",
                "1": "result",
                "2": "wind",
                "3": "name",
                "4": "nationality",
                "5": "date of birth",
                "6": "rank in event",
                "7": "location of event",
                "10": "date of event",
            },
            {
                "0": "rank",
                "1": "result",
                "2": "name",
                "4": "nationality",
                "5": "date of birth",
                "6": "rank in event",
                "7": "location of event",
                "8": "date of event",
            },
        ]

    mappings = get_mappings_men()

    return df.with_columns([pl.col(c).cast(str) for c in df.columns]).rename(
        mapping=decide_mapping_men(df["event"].unique()[0], len(df.columns), mappings)
    )


def pipe_rename_columns_names_women(df: pl.DataFrame) -> pl.DataFrame:
    def decide_mapping_women(name, number_columns, mappings):
        if "15k" in name or "20km" in name:
            return mappings[3]
        if "half" in name:
            return mappings[2]
        # if "1500" in name or "400m hurdles" in name:
        #    return mappings[3]
        if number_columns == 12:
            return mappings[0]
        return mappings[1]

    def get_mappings_women() -> list[dict[str, str]]:
        return [
            {
                "0": "rank",
                "1": "result",
                "2": "wind",
                "3": "name",
                "4": "nationality",
                "5": "date of birth",
                "6": "rank in event",
                "7": "location of event",
                "8": "date of event",
            },
            {
                "0": "rank",
                "1": "result",
                "2": "name",
                "3": "nationality",
                "4": "date of birth",
                "5": "rank in event",
                "6": "location of event",
                "7": "date of event",
            },
            {
                "0": "rank",
                "1": "result",
                "2": "name",
                "3": "nationality",
                "4": "date of birth",
                "5": "rank in event",
                "6": "location of event",
                "8": "date of event",
            },
            {
                "0": "rank",
                "1": "result",
                "2": "name",
                "3": "nationality",
                "4": "date of birth",
                "5": "rank in event",
                "6": "location of event",
                "8": "date of event",
            },
        ]

    mappings = get_mappings_women()

    return df.with_columns([pl.col(c).cast(str) for c in df.columns]).rename(
        mapping=decide_mapping_women(df["event"].unique()[0], len(df.columns), mappings)
    )


def pipe_assign_file_name(df: pl.DataFrame, file: str) -> pl.DataFrame:
    return df.with_columns(
        [
            pl.lit(file.split("/")[4]).alias("event"),
            pl.lit(file).alias("file"),
        ]
    )


def pipe_drop_unwanted_columns(df: pl.DataFrame) -> pl.DataFrame:
    should_be_dropped = ["3", "valid", "", "7", "8", "9", "10"]
    columns = [c for c in should_be_dropped if c in df.columns]
    return df.drop(columns=columns)


def pipe_get_wr_strength_by_comparing_with_tenth(df: pl.DataFrame) -> pl.DataFrame:
    return df.with_columns(  # add percentages w.r.t world records
        (
            100
            * (
                pl.col("result seconds")
                / pl.col("result seconds").head(10).last().over("event")
            )
        ).alias("percentage of 10th")
    )


def pipe_convert_dates(df: pl.DataFrame) -> pl.DataFrame:
    # make sure that date of births like 01.01.10 are parsed as 01.01.2010
    return df.with_columns(
        pl.when(pl.col("date of birth").str.split(".").list[2].cast(int) < 10)
        .then(
            pl.col("date of birth").str.split(".").list[0]
            + "."
            + pl.col("date of birth").str.split(".").list[1]
            + "."
            + "20"
            + pl.col("date of birth").str.split(".").list[2]
        )
        .otherwise(
            pl.col("date of birth").str.split(".").list[0]
            + "."
            + pl.col("date of birth").str.split(".").list[1]
            + "."
            + "19"
            + pl.col("date of birth").str.split(".").list[2]
        )
    ).with_columns(
        [
            pl.col("date of birth").str.strptime(
                pl.Date, format="%d.%m.%Y", strict=False
            ),
            pl.col("date of event").str.strptime(
                pl.Date, format="%d.%m.%Y", strict=False
            ),
        ]
    )


def pipe_reorder_and_select_subset_of_columns(df: pl.DataFrame) -> pl.DataFrame:
    return df.select(
        "event",
        "event type",
        "distance",
        "sex",
        "rank",
        "rank in event",
        "name",
        "nationality",
        "date of birth",
        "result",
        "wind",
        "result seconds",
        "date of event",
        "location of event",
        "distance type",
        "has hurdles",
        "on track",
        # "percentage of wr",
        # "percentage of 10th",
        "file",
    )


def pipe_compute_age_at_event(df: pl.DataFrame) -> pl.DataFrame:
    return df.with_columns(
        ((pl.col("date of event") - pl.col("date of birth")).dt.days() / 365).alias(
            "age at event in years"
        )
    )


def pipe_give_same_name_to_100m_and_110m_hurdles(df: pl.DataFrame) -> pl.DataFrame:
    return df.with_columns(
        pl.when(pl.col("event").is_in(["110m hurdles", "100m hurdles"]))
        .then(pl.lit("100m/110m hurdles"))
        .otherwise(pl.col("event"))
        .alias("event")
    )
