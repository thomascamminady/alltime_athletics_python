"""Tests for `alltime_athletics_python` package."""
import polars as pl

from alltime_athletics_python.io import import_running_only_events


def test_reads_df_without_crashing():
    df = import_running_only_events("./data")

    assert df.filter(pl.col("legality") == "standard").shape[0] == 154594
    assert df.shape[0] == 179233
