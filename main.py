# TODO: create merged dataframe with columns per datestamp
# TODO: Make pretty plots
# TODO: Clean up (docstrings, ...)
# TODO: Create consistent data file names


from bs4 import BeautifulSoup as bs
import io
import pandas as pd
import requests
import string


def makeFilename(filename, replacements={":": "-"}):
    """
    Strip input string down to only valid characters for a Windows filename and return.
    Replacements is an optional dictionary keys representing characters to replace by the corresponding value before stripping invalid characters.
    If the substituted value is not a valid filename character, it will be stripped anyway after the replacement. 
    """
    valid_chars = frozenset("-_.() %s%s" % (string.ascii_letters, string.digits))
       
    filename = ''.join(replacements[c] if c in replacements else c for c in filename)

    return ''.join(c for c in filename if c in valid_chars)


def getData():
    """Scrape Corona infections per Dutch municipality from the RIVM and store data as CSV."""

    url = "https://www.rivm.nl/coronavirus-kaart-van-nederland"
    r = requests.get(url)

    if r.status_code != 200:
        print("Loading webpage failed!")
        return
    
    soup = bs(r.text, 'lxml')
    csv_data = str(soup.find("div", {"id": "csvData"}).contents[0]).strip()

    raw_timestamp = soup.find("span", {"class": "content-date-edited"}).contents[0]
    timestamp_as_filename = makeFilename(raw_timestamp)

    # TODO: Check if file already exists. If so, return.
   
    # Define how to deal with NA values
    naInt = lambda x: int(x) if len(x) else 0

    # Convert csv_data to StringIO class for pd.read_table() compatibility
    csv_data = io.StringIO(csv_data)
    df = pd.read_table(csv_data, sep=";", index_col=0, dtype={"Gemeente:":str}, converters={"Gemnr": naInt, "Aantal": naInt})
    
    df.to_csv("data/" + timestamp_as_filename + ".csv")


# Main script execution
if __name__ == '__main__':
    getData()