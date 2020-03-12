import io
import requests
import pandas as pd


def getData():
    """
    Load source of the rivm corona page, then save as csv
    """
    # Download source from rivm corona page
    url = "https://www.rivm.nl/coronavirus-kaart-van-nederland"
    pageContent = requests.get(url).text

    # Find start and end of csv data <div>
    startTag, endTag = '<div id="csvData">', "</div>"
    fromIndexData = pageContent.index(startTag) + len(startTag)
    toIndexData = pageContent.index(endTag, fromIndexData)

    # Filter to keep only relevant data
    newData = io.StringIO(pageContent[fromIndexData:toIndexData])

    naInt = lambda x: x if str(x).isnumeric else 0
    df = pd.read_table(newData, sep=";", index_col=0, dtype={"Gemeente:":str}, na_values="", converters={"Gemnr": naInt, "Aantal": naInt})
    print(df)

    # read timestamp
    timeStamp = str(df.index[0][len("peildatum "):]).replace(":", "-").replace(" ", "_")
    
    # Store to csv
    df.to_csv("data/" + timeStamp + ".csv")



# Main script execution
if __name__ == '__main__':
    getData()