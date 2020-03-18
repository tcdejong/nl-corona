# TODO: create merged dataframe with column per datestamp
# TODO: Verify if datestamp.csv already exists, don't overwrite
# TODO: Make pretty plots
# TODO: Clean up (docstrings, ...)
# TODO: Create consistent data file names

import io
import pandas as pd
import requests

def getData():
    """
    Scrape Corona infections per Dutch municipality from the RIVM and store data as CSV.
    """
    ### Collect the data
    # Download source from rivm corona page
    url = "https://www.rivm.nl/coronavirus-kaart-van-nederland"
    pageContent = requests.get(url).text

    # Find start and end of csv data based on <div> tags
    startTag, endTag = '<div id="csvData">', '</div>'
    fromIndex = pageContent.index(startTag) + len(startTag)
    toIndex = pageContent.index(endTag, fromIndex)
    # Extract data, trim whitespace, split multi-line string to list
    csvLines = pageContent[fromIndex:toIndex].strip().splitlines()


    ### Clean up csv formatting
    # Count number of column headers
    numCols = csvLines[0].count(";") + 1
    # Remove fields without column headers
    csvLines = [";".join(str(line).split(";")[:numCols]) for line in csvLines]
    csvData = "\n".join(csvLines)


    
    # Define how to deal with NA values
    naInt = lambda x: int(x) if len(x) else 0

    # Convert csvData to StringIO class for pd.read_table() compatibility
    csvData = io.StringIO(csvData)
    df = pd.read_table(csvData, sep=";", index_col=0, dtype={"Gemeente:":str}, converters={"Gemnr": naInt, "Aantal": naInt})

    # read timestamp
    startTag, endTag = "<p>aantal per ", "</p>"
    fromIndex = pageContent.index(startTag) + len(startTag)
    toIndex = pageContent.index(endTag, fromIndex)
    timeStamp = str(pageContent[fromIndex:toIndex]).replace(" ", "_").replace(" ", "_").replace(".", "-") # second replace is no-break space U+00A0
    
    # Store to csv
    df.to_csv("data/" + timeStamp + ".csv")



# Main script execution
if __name__ == '__main__':
    getData()