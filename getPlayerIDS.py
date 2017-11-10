import scrapePlayerIds
import argparse
import pandas as pd 

parser = argparse.ArgumentParser()
parser.add_argument('-year','--year',default=None,required=True) # Get players who played back to this year
args = parser.parse_args()

scrapePlayerIds.scrapePlayerIdsFromYear(args.year)

