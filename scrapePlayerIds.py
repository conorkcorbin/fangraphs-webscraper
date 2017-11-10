import urllib
from bs4 import BeautifulSoup

def scrapePlayerIdsFromYear(year=2002):
    """ 
    Fangraphs maps each player to a player ID. You can access player information
    by appending a player's ID to the base URL.  Here we scrape player Ids
    going back to a particular year and save them in a txt file so we can 
    scrape their game logs.

    Parameters
    ----------
    year : int (return all player IDs who have played baseball back to this year)

    """
    hrefs = GetUrls2PlayerRefs()
    batters, pitchers = GetPlayerMaps(hrefs,year=2002)

    with open('players' + str(year) + '.txt', 'w') as w:
        for key,val in batters.items():
            w.write(val[0] + '\t' + key + '\n')
        for key,val in pitchers.items():
            w.write(val[0] + '\t' + key + '\n')

def GetUrls2PlayerRefs(url='http://www.fangraphs.com/players.aspx'):
    """
    Parameters
    ----------
    url: url containing links to players by first two letters
    
    Returns
    -------
    hrefs: list of all the links to player pages by first two letters
    
    """
    page = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(page,'lxml')
    atags = soup.select('.s_name a')
    hrefs = [a['href'] for a in atags]
    
    return hrefs

def GetPlayerMaps(urls,year=None,base='http://www.fangraphs.com/'):
    """
    Parameters
    ----------
    urls: list of website urls containing list of players as links 
    year: threshold -- will only return map of players who played in or after said year
    base: Base name for website (fangraphs)
    
    Returns
    -------
    players: dictionary : Href is the key and tuple of (player_name,years_played,position) is value
    
    """
    players = {}
    for url in urls:
        try:
            page = urllib.request.urlopen(base+url).read()
            soup = BeautifulSoup(page, 'lxml')
            tables = soup.select('.search table') #selects tables in the div class=search tag
            rows = tables[0].find_all('tr')
            for row in rows:
                cols = row.select('td')
                #This adds element to player dictionary
                #Href is the key and tuple of (player_name,years_played,position) is value
                key=row.find('a')['href']
                key = reformat_key(key)
                players[key] = (cols[0].get_text(),cols[1].get_text(),cols[2].get_text())
        except:
            print(base+url)
    if (year != None):
        players = {key: val for (key,val) in players.items() if (played_in_year(year,val))}

    #Seperate pitchers and postion players
    pitchers = {key: val for (key,val) in players.items() if (val[2]=='P')}
    pos_players = {key: val for (key,val) in players.items() if (val[2]!='P')}
    return pos_players, pitchers

def played_in_year(year,player_info):
    #Helper Function for GetPlayerMaps
    try: 
        player_year = int(player_info[1].split()[2])
        if (player_year >= year):
            return True
        else:
            return False
    except:
        return False
        
def reformat_key(key):
    #Helper for Get player_map
    return key[:5] + 'd' + key[6:]



