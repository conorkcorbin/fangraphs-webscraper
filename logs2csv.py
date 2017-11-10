import scraper
import argparse
import pandas as pd 

parser = argparse.ArgumentParser()
parser.add_argument('-PlayerName','--PlayerName',required=True) # [FirstName LastName]
parser.add_argument('-Date1','--Date1',default=None,required=False) # Most Recent Date
parser.add_argument('-Date2','--Date2',default=None,required=False) # Least Recent Date
args = parser.parse_args()

data = scraper.ScrapePlayerLogs(args.PlayerName,args.Date1,args.Date2)
data.to_csv(args.PlayerName.replace(" ","")+'.csv',index=False)

