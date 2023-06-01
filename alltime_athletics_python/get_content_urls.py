import re
import urllib.request

import pandas as pd

BASEURL = "http://www.alltime-athletics.com/"


def get_content_urls() -> pd.DataFrame:
    """Returns a data frame that contains information on all data pages.

    Returns
    -------
    pd.DataFrame
        Data frame with information on all data pages.
    """
    df_list = []
    sexes = ["men", "women"]
    for sex in sexes:
        # get content of website
        url = BASEURL + sex + ".htm"
        fp = urllib.request.urlopen(url)
        contentbytes = fp.read()
        content = contentbytes.decode("ISO-8859-1")

        # find all listings of outgoing links to data with their respective description
        pattern = r'href="(?!http)(.*?).htm">(.*?)</a>'
        matches = re.findall(pattern, content)

        # create dataframe from matches
        urls = pd.DataFrame(matches, columns=["url", "event"])

        # do some postprocessing with the dataframe
        urls = post_process_df(urls, sex)

        # add to list containing data from both sexes
        df_list.append(urls)

    df = pd.concat(df_list).reset_index()
    return df


def post_process_df(df: pd.DataFrame, sex: str) -> pd.DataFrame:
    # Full url to data
    df["url"] = df["url"].apply(lambda url: BASEURL + url + ".htm")

    # Legal or non-legal marks
    # TODO: this assumes, that we have the legal events first
    df["mark"] = (
        df.groupby("event")["url"]
        .transform(lambda x: x.index == x.index.min())
        .transform(lambda x: "legal" if x else "non-legal")
    )
    # Standard or special event type
    # TODO: this assumes that the first special event is the 60 metres
    special_event_index_start = df.loc[df["event"] == "60 metres"].index.min()
    df.loc[:special_event_index_start, "event type"] = "standard"
    df.loc[special_event_index_start:, "event type"] = "special"

    # Men or Women
    df["sex"] = sex
    return df
