# from flask import Flask 
import time
from datetime import datetime, timedelta

import dash
import dash_core_components as dcc 
import dash_html_components as html 
# import dash_table_experiments as dt


import numpy as np 
import pandas as pd 
import dota2api
api = dota2api.Initialise()


# server = Flask(__name__)
# app = dash.Dash(__name__, server = server)
app = dash.Dash(__name__)


# livegames = api.get_top_live_games()
# df = pd.DataFrame(livegames["game_list"])
# last_updated = df["last_update_time"][0].astype("datetime64[s]").astype(str).replace("T"," ")

# heroes = pd.DataFrame(api.get_heroes()["heroes"])
# for i in range(10):
#     df["player{}".format(i+1)] = df["players"].apply(lambda x: x[i]["account_id"])
#     df["hero{}".format(i+1)] = df["players"].apply(lambda x: x[i]["hero_id"])
# try:
# 	for i in range(10):
# 		df["hero{}".format(i+1)] = df["hero{}".format(i+1)].apply(lambda x: heroes[heroes["id"]==x].localized_name.values[0])
# except Exception as e:
# 	ErrorOccurred = True #### global
# 	app.layout = html.H4("Data Acquiring, picking stage for a top spectating game! Please check back in a minute.")


# df["game_time_min"] = df["game_time"].apply(lambda x: int((datetime(1,1,1) + timedelta(seconds=x)).minute) if x>0 else 0)
# df["game_time_sec"] = df["game_time"].apply(lambda x: int((datetime(1,1,1) + timedelta(seconds=x)).second) if x>0 else x)
# # df["game_time"] = df.apply(lambda x: str(x.game_time_min) + ":" + str(x.game_time_sec), axis=1)
# df["game_time"] = df.apply(lambda x: "{:02}:{:02}".format(x.game_time_min,x.game_time_sec) if x.game_time_sec>0 else str(x.game_time_sec), axis=1)

# game_attributes = df.iloc[:,[1,17,5,14,7]]
# # game_players = df.iloc[:,18:38]


mapping = {
	'average_mmr': 'Average MMR',
	'spectators': 'Spectators',
	'dire_score': 'Dire Score',
 	'radiant_score': 'Radiant Score',
 	'game_time': 'Game Time'
}


app.layout = html.Div(className="container", children=[
	dcc.Markdown("""
# Dota2 Data Exploration
### Top live matchmaking results
These are the top stack Dota2 matches that are currently in progress
"""),
	# html.P("Last updated: {}".format(last_updated), style = { "float": "right"}),
	html.Div(id="recent-matches", className="docs-example"),
	dcc.Interval(id="recent-matches-update", interval="1*1000")
])

def generate_table(df, max_rows=10):
	return html.Table(className="u-full-width", children=[
			html.Thead(
				html.Tr(children=[
					html.Th(col.title().replace("_"," ")) for col in df.columns.values
				], style = {"color":"#004c70"})), 
			html.Tbody([
				html.Tr(children = [
					html.Td(data) for data in row
				], style = {"color":"#292f33"})
				for row in df.values.tolist()
			])
		])

@app.callback(
	dash.dependencies.Output("recent-matches", "children"),
	events = [dash.dependencies.Event("recent-matches-update", "interval")]
)
def update_recent_matches_table():

	try:

		livegames = api.get_top_live_games()
		df = pd.DataFrame(livegames["game_list"])
		last_updated = df["last_update_time"][0].astype("datetime64[s]").astype(str).replace("T"," ")
		df["game_time_min"] = df["game_time"].apply(lambda x: int((datetime(1,1,1) + timedelta(seconds=x)).minute) if x>0 else 0)
		df["game_time_sec"] = df["game_time"].apply(lambda x: int((datetime(1,1,1) + timedelta(seconds=x)).second) if x>0 else x)
		df["game_time"] = df.apply(lambda x: "{:02}:{:02}".format(x.game_time_min,x.game_time_sec) if x.game_time_sec>0 else str(x.game_time_sec), axis=1)
		game_attributes = df.iloc[:,[1,17,5,14,7]]

	except Exception as e:
		with open("errors.txt","a") as f:
			f.write(str(e))
			f.write("\n")		

	return generate_table(game_attributes, max_rows=10)


# div className = "container"
# div className = "row" --> nested "one column", "eleven columns" ; "two columns", "ten columns" ; etc.
# div className = "docs-example"

# section className = "header",
# ## table,textarea, select .. className = "u-full-width"
# ul className = "popover-list"




css_url = "https://codepen.io/chriddyp/pen/bWLwgP.css"
app.css.append_css({
	"external_url": css_url
	})


if __name__ == "__main__":
	app.run_server(debug = True)
