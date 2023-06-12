from datetime import date

from alltime_athletics_python.io import (
    download_data,
    import_running_only_events,
)

if __name__ == "__main__":
    download_data()
    df = import_running_only_events("./data")
    today = date.today()
    df.write_parquet(f"./dataframes/alltime_athletics_version_{today}.parquet")
    df.write_parquet("./dataframes/latest_version_alltime_athletics.parquet")
    df.write_csv("./dataframes/latest_version_alltime_athletics.csv")
