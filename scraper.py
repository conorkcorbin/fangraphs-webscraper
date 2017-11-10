import urllib
from bs4 import BeautifulSoup
import datetime
import pandas as pd
import urllib.request 

def ScrapePlayerLogs(player_name,t1=None,t2=None):
    """
    Parameters
    ----------
    player_name: name of player (Firstname Lastname)
    t1: start day to scrape from (most recent date)
    t2: end day to scrape from (least recent date)
        Parameters

    Returns
    --------
    GameLogs: pandas df object with everything in fangraphs standard batter game logs
    
    """

    def Between(date,t1,t2):
        #Helper -- returns true if year within the desired query 
        if (date <= t1 and date >= t2):
            return True
        else:
            return False

    # Declare some constants
    base='http://www.fangraphs.com/'
    logs_ext='&type=1&gds=&gde=&season=all'


    #Deal with dates
    if t1 == None:
        t1 = str(datetime.date.today()) # assume wish to scrape from last game played
    if t2 == None:
        t2 = '0000-00-00'

    #Get url of game logs for the desired player
    try:
        url = base + get_ext(player_name) + logs_ext
    except:
        print("Player [%s] not found. Check your spelling, and make sure in format (Firstname Lastname)" % player_name)
        exit()


    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page,'lxml')
    table = soup.find('table',class_='rgMasterTable') #store table

    column_names = [col.get_text().replace('%','p') for col in table.select('th')]
    column_names = [c.replace('/','div').replace('-','minus') for c in column_names]
    column_names.insert(0,"Handedness")
    column_names.insert(0,"Name") # rows

    handedness = soup.find('div',{'style' : 'font-size: 10pt; padding-left: 5px;'})
    handedness = handedness.get_text().split('/')[4].split()[0].strip()

    rows = [[player_name]+[handedness]+[data.get_text().replace('%','').strip() for data in r.select('td')] for r in GetRows(table)]
    rows = [r for r in rows if Between(r[2],t1,t2)] # Only returns dates within query. 
    data = pd.DataFrame(data=rows,columns=column_names)
    return data

def scrapeBatterSplits(playerName,yeart1,yeart2):
    """
    Parameters
    ----------
    player_name: name of player (Firstname Lastname)
    t1: start year (most recent date)
    t2: end year (least recent date)
        Parameters

    Returns
    --------
    splits: pandas df object with righty lefty splits , pull oppo center splits, monthly splits
    
    """
    extension = 'statsplits.aspx?' + get_ext(playerName).split('?')[1]
    url = 'http://www.fangraphs.com/' + extension
    # print(url)
    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page,'lxml')
    
    seasons = soup.find_all('div',{'class' : 'rtsLevel rtsLevel1'})
    seasons = seasons[-1:][0].find_all('li')
    seasons.pop(0)
    seasons = [int(s.get_text()) for s in seasons]
    counter = 0
    currentSeason = seasons[counter]
    data = []

    for season in seasons:
        if season >= yeart2:
            splitstable = soup.find('table',class_='rgMasterTable')
            column_names = [col.get_text() for col in splitstable.select('th')]
            column_names[1] = 'Split'
            column_names.insert(0,"Name")
            rows = [[playerName]+[data.get_text() for data in r.select('td')] for r in GetRows(splitstable)]
            data.append(pd.DataFrame(data=rows,columns=column_names))
            suffix = '&season=' + str(season)
            url = 'http://www.fangraphs.com/' + extension + suffix 
            if (season >= seasons[len(seasons)-1] and season >= yeart2):
                page = urllib.request.urlopen(url)
                soup = BeautifulSoup(page,'lxml')
            else: 
                break

    data = pd.concat(data,axis=0)
    return data



def scrapePitcherHandedness(playerName):
    url = 'http://www.fangraphs.com/' + get_ext(playerName)
    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page,'lxml')
    handedness = soup.find('div',{'style' : 'font-size: 10pt; padding-left: 5px;'})
    print(handedness.get_text().split('/')[4].split()[0].strip())


def get_ext(player_name):
    #returns url extension for a player from players.txt

    filename='players2002.txt'
    with open(filename) as f: 
        lines = f.read().splitlines()
        players = {l.split('\t')[0]:l.split('\t')[1] for l in lines}
    f.close()
    return players[player_name]


def GetRows(table):
    #Helper function for InsertGameLogstoSQL
    #For better readibility
    rows = table.find_all('tr', {'class':['rgRow','rgAltRow']})
    #rows = table.find_all('tr',class_='rgRow') + table.find_all('tr',class_='rgAltRow')
    return rows
