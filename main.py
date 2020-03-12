import requests
import os


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
    newData = pageContent[fromIndexData:toIndexData]
    print(newData)

    # read timestamp
    timeTag = "peildatum "
    fromIndexTS = newData.index(timeTag) + len(timeTag)
    toIndexTS = newData.find(";", fromIndexTS)
    timeStamp = newData[fromIndexTS:toIndexTS]

    # verify if timestamp is new (csv does not yet exist)
    # dataPath = os.path.
    # print(dataPath)
    # dataFiles = os.listdir(dataPath)
    # print(dataFiles)


    # Store to csv


# Main script execution
if __name__ == '__main__':
    getData()