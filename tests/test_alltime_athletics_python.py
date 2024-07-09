"""Tests for `alltime_athletics_python` package."""

import polars as pl

from alltime_athletics_python.events import event_list
from alltime_athletics_python.io import import_running_only_events

df = import_running_only_events("./data")


def test_reads_df_without_crashing():
    assert df.filter(pl.col("legality") == "standard").shape[0] == 154594
    assert df.shape[0] == 179233


def test_every_event_in_event_list_present_in_df():
    events_in_df = df["event"].unique().to_list()
    for event in event_list:
        assert event.name in events_in_df


def test_every_event_in_df_is_present_in_event_list():
    events_in_df = df["event"].unique().to_list()
    event_list_names = [e.name for e in event_list]
    for event in events_in_df:
        assert event in event_list_names
