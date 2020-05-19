import bs4 as bs
import time
import re
import io
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


SCROLL_PAUSE_TIME = 0.25

def parseThroughSource(resultsRow, file):
    results = []


    for result in resultsRow:


        if (result.select('div.search_price span strike')):
            price = result.select('div.search_price span strike')[0].text.strip(' \t\n\r')
            if (price != None):
                continue

        gameURL = result.get('href')

        title = result.find('span',{'class': 'title'}).text

        file.write(repr({title + " - " + gameURL}) + '\n')



def main():
    global SCROLL_PAUSE_TIME

    sel = webdriver.ChromeOptions()
    sel.add_argument('--ignore-certificate-errors')
    sel.add_argument('--incognito')
    sel.add_argument('--headless')

    cdm = ChromeDriverManager()

    driver = webdriver.Chrome(cdm.install(), options=sel)
    driver.get("https://store.steampowered.com/search/?sort_by=Released_DESC&category1=998&unvrsupport=401&genre=Free+to+Play")


    lastHeight = driver.execute_script("return document.body.scrollHeight")

    #Load the entire List of Games
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        time.sleep(SCROLL_PAUSE_TIME)

        newHeight = driver.execute_script("return document.body.scrollHeight")

        #Check to see if TF2 is in the list (It's the last Free Game that Steam will list)
        if(newHeight == lastHeight):
            TF2 = re.search(r'Team_Fortress_2', driver.page_source)
            if(TF2 != None):
                break

        lastHeight = newHeight

    #Grab the Source Code from the driver and close it
    pageSource = driver.page_source
    driver.close()


    soup = bs.BeautifulSoup(pageSource, 'lxml')

    resultsRow = soup.find_all('a',{'class': 'search_result_row'})

    io.open('FreeSteamGamesList.txt', 'w', encoding="utf-8").close()
    file = io.open("FreeSteamGamesList.txt","a",encoding="utf-8")

    parseThroughSource(resultsRow, file)

    print("DONE!")
    file.close()

if __name__ == "__main__":
    main()