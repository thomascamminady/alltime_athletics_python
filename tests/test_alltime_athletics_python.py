"""Tests for `alltime_athletics_python` package."""
from alltime_athletics_python.io import import_running_only_events


def test_reads_df_without_crashing():
    df = import_running_only_events("./data")
    assert df.shape[0] == 154594
