# fangraphs-webscraper
A tool to scrape player game logs from fangraphs as they relate to daily fantasy sports.  Built out of necessity for another project, but pretty useful in and of itself. 

## Getting Started

```
git clone https://github.com/conorkcorbin/fangraphs-webscraper.git
```

## Python Environment 
Python 3.6.  

## Scrape Game Logs

The repo comes with a text file that matches every player playing back to 2002 with the fangraphs player ID. This is used to access their game logs. 

To scrape game logs, we utilize the following method in scraper.py

```
import scaper
data = scraper.ScrapePlayerLogs("Clayton Kershaw',t1='2017-09-30',t2='2016-09-30')
```

Or if we want to get game logs through his entire carear

```
data = scraper.ScrapePlayerLogs("Clayton Kershaw")
```

This works for pitchers and batters

```
data = scraper.ScrapePlayerLogs("Buster Posey")
```

logs2csv.py was built as a wrapper for this method. It creates a csv from the returned dataframe

From the terminal

```
python logs2csv.py -PlayerName "Clayton Kershaw" -Date1 2017-09-30 -Date2 2016-09-30
```

or similarily

```
python logs2csv.py -PlayerName "Clayton Kershaw"
```

### Scrape Player IDs

The repo uses a player ID database that goes back to 2002.  To create a new database going back further (say 1990) you can do the following. This can take ~20 min or more depending on how far you go back. 

```
python getPlayerIDS.py -year 1990
```

Then in scraper.py change the get_ext() helper method to read in the new playerID file. 

## Authors

* **Conor K Corbin** 


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
