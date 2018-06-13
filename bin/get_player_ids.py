from fangraphs_webscraper.scrape_player_ids import scrape_player_ids_from_year
import argparse
import pandas as pd 

parser = argparse.ArgumentParser()
parser.add_argument('-year','--year',
					default=None,
					type=int,
					required=True) # Get players who played back to this year
args = parser.parse_args()

scrape_player_ids_from_year(args.year)

