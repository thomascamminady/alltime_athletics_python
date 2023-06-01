import html
import re
import urllib.request
from dataclasses import dataclass
from io import StringIO

import pandas as pd


@dataclass
class Content:
    folder: str
    filename: str
    df: pd.DataFrame


def get_content(content_metadata: pd.Series) -> list[Content]:
    """Returns content objects.

    Given a single row with metadata, we return a list of Content objects,
    containing the data that can be found under the url specified in the
    content_metadata.

    Parameters
    ----------
    content_metadata : pd.Series
        The metadata information regarding the event.

    Returns
    -------
    list[Content]
        List of content objects, storing the data regarding the requested event.
    """
    # Extract parameter from metadata
    url = content_metadata["url"]
    event = content_metadata["event"]
    sex = content_metadata["sex"]
    mark = content_metadata["mark"]
    event_type = content_metadata["event type"]

    # Get content from data page.
    fp = urllib.request.urlopen(url)
    content_bytes = fp.read()
    content = content_bytes.decode("ISO-8859-1")
    content = html.unescape(content)

    # Per event, there are multiple sub entries, differing by their description.
    # Example content taken from http://www.alltime-athletics.com/mhmaraok.htm:
    #
    # <H1>All-time men's best half-marathon </H1>
    # <p>
    # <H5>@=uncertified course or uncertain certification</H5>
    # <p>
    # <A name="1"><H3>a=slightly downhill</h3></A>
    # <p>
    # <H3>+ = en route in race at longer distance</H3>
    # <PRE>
    #         1      57:31      Jacob Kiplimo                  UGA     14.11.00
    #         2      57:32      Kibiwott Kandie                KEN     20.06.96
    #         3      57:37      Jacob Kiplimo                  UGA     14.11.00
    #         4      57:49      Rhonex Kipruto                 KEN     12.10.99
    #         5      57:56      Jacob Kiplimo                  UGA     14.11.00
    #
    pattern = r"(?i)<a name=(.*?)<pre>(.*?)</pre>"
    regex = re.compile(pattern, re.DOTALL)
    matches = regex.findall(content)
    # Now iterate through all the sub entries and gather the respective data.
    output = []
    for i, match in enumerate(matches):
        # Remove some font color tags in the output data frame.
        content = re.sub("<[^<]+?>", "", match[1])

        # Get data of sub entry-
        df = pd.read_fwf(StringIO(content), header=None)

        # Each sub entry has a text with some description on what the
        # subsequent data relates to, e.g., downhill course, etc.
        # There might be more than one field of this.
        description_pattern = r"[hH](\d+)>(.*?)<(/[hH]\d+)>"
        description_matches = re.findall(description_pattern, match[0])

        description = ";".join([match[1] for match in description_matches])

        # Remove / in the description because we use this to create a folder.
        description = description.replace("/", " or ")

        # Which folder we might want to store the data in.
        folder = f"{sex}/{event_type}/{event}/{mark}/"
        c = Content(folder, f"{i} {description.lower()}.csv", df)
        output.append(c)
    return output
