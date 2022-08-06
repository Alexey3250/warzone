import os
import requests
import urllib.parse
import json
import datetime
import re

from flask import redirect, render_template, request, session
from functools import wraps
from cs50 import SQL

# Connect database
db_wz = SQL("sqlite:///warzone.db")
# Define season for the database entries
season = "Vanguard_4"

# TODO: add a timed update to the database

def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def search(tag, platform):
    """ Requests matches data from API and returns it. """
    print("function search initiated")
    # Contact API
    try:
        url = ('https://call-of-duty-modern-warfare.p.rapidapi.com/warzone/' + tag + '/' + platform)

        # this is the api key that we put before starting the flask
        api_key = os.environ.get("API_KEY")
        headers = {
            "X-RapidAPI-Key": api_key,
            "X-RapidAPI-Host": "call-of-duty-modern-warfare.p.rapidapi.com"
        }

        response = requests.request("GET", url, headers=headers)
    except requests.RequestException:
        return None

    # Parse response
    try:
        warzone_data = json.loads(response.text)
        message = response.json()
        # Check if we received an error
        try:
            if message["error"]:
                return message["message"]

        except:

            # Calculation of deaths for br_all
            br_all_kills = int(json.dumps(warzone_data['br_all']['kills']))
            br_all_kdRatio = float(json.dumps(warzone_data['br_all']['kdRatio']))
            br_all_deaths = int(br_all_kills / br_all_kdRatio)
            # Calculation of deaths for br
            br_kills = int(json.dumps(warzone_data['br']['kills']))
            br_kdRatio = float(json.dumps(warzone_data['br']['kdRatio']))
            br_deaths = int(br_kills / br_kdRatio)
            # Calculating the kills for br_dmz
            br_dmz_kills = int(json.dumps(warzone_data['br_dmz']['kills']))
            br_dmz_kdRatio = float(json.dumps(warzone_data['br_dmz']['kdRatio']))
            br_dmz_deaths = int(br_dmz_kills / br_dmz_kdRatio)

            # this is the data that we want to return
            warezone_data_dict = {
                "br_all_wins": int(json.dumps(warzone_data['br_all']['wins'])),
                "br_all_kills": int(json.dumps(warzone_data['br_all']['kills'])),
                "br_all_kdRatio": float(json.dumps(warzone_data['br_all']['kdRatio'])),
                "br_all_deaths": br_all_deaths,
                "br_all_downs": int(json.dumps(warzone_data['br_all']['downs'])),
                "br_all_topTwentyFive": int(json.dumps(warzone_data['br_all']['topTwentyFive'])),
                "br_all_topTen": int(json.dumps(warzone_data['br_all']['topTen'])),
                "br_all_topFive": int(json.dumps(warzone_data['br_all']['topFive'])),
                "br_all_contracts": int(json.dumps(warzone_data['br_all']['contracts'])),
                "br_all_revives": int(json.dumps(warzone_data['br_all']['revives'])),
                "br_all_score": int(json.dumps(warzone_data['br_all']['score'])),
                "br_all_scorePerMinute": float(json.dumps(warzone_data['br_all']['scorePerMinute'])),
                "br_all_timePlayed": int(json.dumps(warzone_data['br_all']['timePlayed'])),
                "br_all_cash": int(json.dumps(warzone_data['br_all']['cash'])),

                # br BR only values are saved to variables
                "br_wins": int(json.dumps(warzone_data['br']['wins'])),
                "br_kills": int(json.dumps(warzone_data['br']['kills'])),
                "br_kdRatio": float(json.dumps(warzone_data['br']['kdRatio'])),
                "br_deaths": br_deaths,
                "br_downs": int(json.dumps(warzone_data['br']['downs'])),
                "br_topTwentyFive": int(json.dumps(warzone_data['br']['topTwentyFive'])),
                "br_topTen": int(json.dumps(warzone_data['br']['topTen'])),
                "br_topFive": int(json.dumps(warzone_data['br']['topFive'])),
                "br_contracts": int(json.dumps(warzone_data['br']['contracts'])),
                "br_revives": int(json.dumps(warzone_data['br']['revives'])),
                "br_score": int(json.dumps(warzone_data['br']['score'])),
                "br_scorePerMinute": float(json.dumps(warzone_data['br']['scorePerMinute'])),
                "br_timePlayed": int(json.dumps(warzone_data['br']['timePlayed'])),
                "br_cash": int(json.dumps(warzone_data['br']['cash'])),

                # br_dmz Rebirth values are saved to variables
                "br_dmz_wins": int(json.dumps(warzone_data['br_dmz']['wins'])),
                "br_dmz_kills": int(json.dumps(warzone_data['br_dmz']['kills'])),
                "br_dmz_kdRatio": float(json.dumps(warzone_data['br_dmz']['kdRatio'])),
                "br_dmz_deaths": br_dmz_deaths,
                "br_dmz_downs": int(json.dumps(warzone_data['br_dmz']['downs'])),
                "br_dmz_topTwentyFive": int(json.dumps(warzone_data['br_dmz']['topTwentyFive'])),
                "br_dmz_topTen": int(json.dumps(warzone_data['br_dmz']['topTen'])),
                "br_dmz_topFive": int(json.dumps(warzone_data['br_dmz']['topFive'])),
                "br_dmz_contracts": int(json.dumps(warzone_data['br_dmz']['contracts'])),
                "br_dmz_revives": int(json.dumps(warzone_data['br_dmz']['revives'])),
                "br_dmz_score": int(json.dumps(warzone_data['br_dmz']['score'])),
                "br_dmz_scorePerMinute": float(json.dumps(warzone_data['br_dmz']['scorePerMinute'])),
                "br_dmz_timePlayed": int(json.dumps(warzone_data['br_dmz']['timePlayed'])),
                "br_dmz_cash": int(json.dumps(warzone_data['br_dmz']['cash']))

            }

            # Filling the rest of the values to complete the table

            # Checking if we received some data back from the API
            if not warezone_data_dict["br_all_kills"]:
                return apology("couldn't find the data")

            else:
                # TODO: Implement login logic here
                user_id = 2 # not implemented yet

                # Defining some values to add to a database
                timestamp = datetime.datetime.now()
                id_db = db_wz.execute("SELECT MAX(entry_id) FROM br_all")
                entry_id = id_db[0]["MAX(entry_id)"] + 1

                # TODO: make this threaded
                # Inserting the data into the br_all database
                db_wz.execute("INSERT INTO br_all(entry_id, timestamp, platform, wins, kills, kdRatio, deaths, downs, topTwentyFive, topTen, topFive, contracts, revives, score, scorePerMinute, timePlayed, cash, tag) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        entry_id, timestamp, platform,
                        warezone_data_dict["br_all_wins"],
                        warezone_data_dict["br_all_kills"],
                        warezone_data_dict["br_all_kdRatio"],
                        warezone_data_dict["br_all_deaths"],
                        warezone_data_dict["br_all_downs"],
                        warezone_data_dict["br_all_topTwentyFive"],
                        warezone_data_dict["br_all_topTen"],
                        warezone_data_dict["br_all_topFive"],
                        warezone_data_dict["br_all_contracts"],
                        warezone_data_dict["br_all_revives"],
                        warezone_data_dict["br_all_score"],
                        warezone_data_dict["br_all_scorePerMinute"],
                        warezone_data_dict["br_all_timePlayed"],
                        warezone_data_dict["br_all_cash"],
                        tag
                    )
                # Inserting the data into the br database
                db_wz.execute("INSERT INTO br(timestamp, platform, wins, kills, kdRatio, deaths, downs, topTwentyFive, topTen, topFive, contracts, revives, score, scorePerMinute, timePlayed, cash, tag) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        timestamp, platform,
                        warezone_data_dict["br_wins"],
                        warezone_data_dict["br_kills"],
                        warezone_data_dict["br_kdRatio"],
                        warezone_data_dict["br_deaths"],
                        warezone_data_dict["br_downs"],
                        warezone_data_dict["br_topTwentyFive"],
                        warezone_data_dict["br_topTen"],
                        warezone_data_dict["br_topFive"],
                        warezone_data_dict["br_contracts"],
                        warezone_data_dict["br_revives"],
                        warezone_data_dict["br_score"],
                        warezone_data_dict["br_scorePerMinute"],
                        warezone_data_dict["br_timePlayed"],
                        warezone_data_dict["br_cash"],
                        tag
                    )
                # Inserting the data into the br_dmz database
                db_wz.execute("INSERT INTO br_dmz(timestamp, platform, wins, kills, kdRatio, deaths, downs, topTwentyFive, topTen, topFive, contracts, revives, score, scorePerMinute, timePlayed, cash, tag) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        timestamp, platform,
                        warezone_data_dict["br_dmz_wins"],
                        warezone_data_dict["br_dmz_kills"],
                        warezone_data_dict["br_dmz_kdRatio"],
                        warezone_data_dict["br_dmz_deaths"],
                        warezone_data_dict["br_dmz_downs"],
                        warezone_data_dict["br_dmz_topTwentyFive"],
                        warezone_data_dict["br_dmz_topTen"],
                        warezone_data_dict["br_dmz_topFive"],
                        warezone_data_dict["br_dmz_contracts"],
                        warezone_data_dict["br_dmz_revives"],
                        warezone_data_dict["br_dmz_score"],
                        warezone_data_dict["br_dmz_scorePerMinute"],
                        warezone_data_dict["br_dmz_timePlayed"],
                        warezone_data_dict["br_dmz_cash"],
                        tag
                    )
                message = "ok"
                print(message)
                return (message)


    except (KeyError, TypeError, ValueError):
        return None

def matches2(tag, platform):
    """
    Returns the matches of a player
    """
    print("matches")
    try:
        # Getting the data from the API
        url = ('https://call-of-duty-modern-warfare.p.rapidapi.com/warzone-matches/' + tag + '/' + platform)
        api_key = os.environ.get("API_KEY")
        headers = {
            "X-RapidAPI-Key": api_key,
            "X-RapidAPI-Host": "call-of-duty-modern-warfare.p.rapidapi.com"
        }

        response = requests.request("GET", url, headers=headers)

    except (KeyError, TypeError, ValueError):
        return None

    # Checking if we received some data back from the API
    if not response.json():
        return apology("couldn't find the data")
    # TODO: add some more checks

    # Parsing the response
    try:
        matches_data = response.json()

        # Looping through the matches
        # TODO: make this threaded
        for x in range(0, 19):

            # Match information
            matchID = str(matches_data["matches"][x]["matchID"])
            map = matches_data["matches"][x]["map"]
            mode = matches_data["matches"][x]["mode"]
            gameType = matches_data["matches"][x]["gameType"]
            utcStartSeconds = matches_data["matches"][x]["utcStartSeconds"]
            utcEndSeconds = matches_data["matches"][x]["utcEndSeconds"]
            duration = matches_data["matches"][x]["duration"]
            playerCount = matches_data["matches"][x]["playerCount"]
            teamCount = matches_data["matches"][x]["teamCount"]

            # Player stats
            kills = matches_data["matches"][x]["playerStats"]["kills"]
            medalXp = matches_data["matches"][x]["playerStats"]["medalXp"]
            matchXp = matches_data["matches"][x]["playerStats"]["matchXp"]
            scoreXp = matches_data["matches"][x]["playerStats"]["scoreXp"]
            wallBangs = matches_data["matches"][x]["playerStats"]["wallBangs"]
            score = matches_data["matches"][x]["playerStats"]["score"]
            totalXp = matches_data["matches"][x]["playerStats"]["totalXp"]
            headshots = matches_data["matches"][x]["playerStats"]["headshots"]
            assists = matches_data["matches"][x]["playerStats"]["assists"]
            challengeXp = matches_data["matches"][x]["playerStats"]["challengeXp"]
            scorePerMinute = matches_data["matches"][x]["playerStats"]["scorePerMinute"]
            distanceTraveled = matches_data["matches"][x]["playerStats"]["distanceTraveled"]
            teamSurvivalTime = matches_data["matches"][x]["playerStats"]["teamSurvivalTime"]
            deaths = matches_data["matches"][x]["playerStats"]["deaths"]
            kdRatio = matches_data["matches"][x]["playerStats"]["kdRatio"]
            bonusXp = matches_data["matches"][x]["playerStats"]["bonusXp"]
            gulagDeaths = matches_data["matches"][x]["playerStats"]["gulagDeaths"]
            timePlayed = matches_data["matches"][x]["playerStats"]["timePlayed"]
            executions = matches_data["matches"][x]["playerStats"]["executions"]
            gulagKills = matches_data["matches"][x]["playerStats"]["gulagKills"]
            nearmisses = matches_data["matches"][x]["playerStats"]["nearmisses"]
            percentTimeMoving = matches_data["matches"][x]["playerStats"]["percentTimeMoving"]
            longestStreak = matches_data["matches"][x]["playerStats"]["longestStreak"]
            teamPlacement = matches_data["matches"][x]["playerStats"]["teamPlacement"]
            damageDone = matches_data["matches"][x]["playerStats"]["damageDone"]
            damageTaken = matches_data["matches"][x]["playerStats"]["damageTaken"]

            # Player information
            team = matches_data["matches"][x]["player"]["team"]
            rank = matches_data["matches"][x]["player"]["rank"]
            username = matches_data["matches"][x]["player"]["username"]
            uno = str(matches_data["matches"][x]["player"]["uno"])

            # Check if the player with uno tag does not exist in a particular match
            if not db_wz.execute("SELECT entry_id FROM matches WHERE uno = ? AND matchID = ?", uno, matchID):
                # Inserting the data into the database
                db_wz.execute("INSERT INTO matches(tag, platform, matchID, map, mode, gameType, utcStartSeconds, utcEndSeconds, duration, playerCount, teamCount, kills, medalXp, matchXp, scoreXp, wallBangs, score, totalXp, headshots, assists, challengeXp, scorePerMinute, distanceTraveled, teamSurvivalTime, deaths, kdRatio, bonusXp, gulagDeaths, timePlayed, executions, gulagKills, nearmisses, percentTimeMoving, longestStreak, teamPlacement, damageDone, damageTaken, team, rank, username, uno, season) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    tag, platform, matchID, map, mode, gameType, utcStartSeconds, utcEndSeconds, duration,
                    playerCount, teamCount, kills, medalXp, matchXp, scoreXp, wallBangs, score, totalXp,
                    headshots, assists, challengeXp, scorePerMinute, distanceTraveled, teamSurvivalTime,
                    deaths, kdRatio, bonusXp, gulagDeaths, timePlayed, executions, gulagKills, nearmisses,
                    percentTimeMoving, longestStreak, teamPlacement, damageDone, damageTaken, team, rank,
                    username, uno, season
                )
            else:
                break



        return (matches_data)

    except (KeyError, TypeError, ValueError):
        return None

def matches(tag, platform):
    """
    Returns the matches of a player
    """
    print("matches")
    try:
        # Getting the data from the API
        url = ('https://call-of-duty-modern-warfare.p.rapidapi.com/warzone-matches/' + tag + '/' + platform)
        api_key = os.environ.get("API_KEY")
        headers = {
            "X-RapidAPI-Key": api_key,
            "X-RapidAPI-Host": "call-of-duty-modern-warfare.p.rapidapi.com"
        }

        response = requests.request("GET", url, headers=headers)

    except (KeyError, TypeError, ValueError):
        return None

    # Checking if we received some data back from the API
    if not response.json():
        return apology("couldn't find the data")
    # TODO: add some more checks

    # Parsing the response
    try:
        matches_data = response.json()

        # Looping through the matches
        # TODO: make this threaded
        for x in range(0, 19):

            # Match information
            matchID = str(matches_data["matches"][x]["matchID"])
            map = matches_data["matches"][x]["map"]
            mode = matches_data["matches"][x]["mode"]
            gameType = matches_data["matches"][x]["gameType"]
            utcStartSeconds = matches_data["matches"][x]["utcStartSeconds"]
            utcEndSeconds = matches_data["matches"][x]["utcEndSeconds"]
            duration = matches_data["matches"][x]["duration"]
            playerCount = matches_data["matches"][x]["playerCount"]
            teamCount = matches_data["matches"][x]["teamCount"]

            # Player stats
            kills = matches_data["matches"][x]["playerStats"]["kills"]
            medalXp = matches_data["matches"][x]["playerStats"]["medalXp"]
            matchXp = matches_data["matches"][x]["playerStats"]["matchXp"]
            scoreXp = matches_data["matches"][x]["playerStats"]["scoreXp"]
            wallBangs = matches_data["matches"][x]["playerStats"]["wallBangs"]
            score = matches_data["matches"][x]["playerStats"]["score"]
            totalXp = matches_data["matches"][x]["playerStats"]["totalXp"]
            headshots = matches_data["matches"][x]["playerStats"]["headshots"]
            assists = matches_data["matches"][x]["playerStats"]["assists"]
            challengeXp = matches_data["matches"][x]["playerStats"]["challengeXp"]
            scorePerMinute = matches_data["matches"][x]["playerStats"]["scorePerMinute"]
            distanceTraveled = matches_data["matches"][x]["playerStats"]["distanceTraveled"]
            teamSurvivalTime = matches_data["matches"][x]["playerStats"]["teamSurvivalTime"]
            deaths = matches_data["matches"][x]["playerStats"]["deaths"]
            kdRatio = matches_data["matches"][x]["playerStats"]["kdRatio"]
            bonusXp = matches_data["matches"][x]["playerStats"]["bonusXp"]
            gulagDeaths = matches_data["matches"][x]["playerStats"]["gulagDeaths"]
            timePlayed = matches_data["matches"][x]["playerStats"]["timePlayed"]
            executions = matches_data["matches"][x]["playerStats"]["executions"]
            gulagKills = matches_data["matches"][x]["playerStats"]["gulagKills"]
            nearmisses = matches_data["matches"][x]["playerStats"]["nearmisses"]
            percentTimeMoving = matches_data["matches"][x]["playerStats"]["percentTimeMoving"]
            longestStreak = matches_data["matches"][x]["playerStats"]["longestStreak"]
            teamPlacement = matches_data["matches"][x]["playerStats"]["teamPlacement"]
            damageDone = matches_data["matches"][x]["playerStats"]["damageDone"]
            damageTaken = matches_data["matches"][x]["playerStats"]["damageTaken"]

            # Player information
            team = matches_data["matches"][x]["player"]["team"]
            rank = matches_data["matches"][x]["player"]["rank"]
            username = matches_data["matches"][x]["player"]["username"]
            uno = str(matches_data["matches"][x]["player"]["uno"])

            # Check if the player with uno tag does not exist in a particular match
            if not db_wz.execute("SELECT entry_id FROM matches WHERE uno = ? AND matchID = ?", uno, matchID):
                # Inserting the data into the database
                db_wz.execute("INSERT INTO matches(tag, platform, matchID, map, mode, gameType, utcStartSeconds, utcEndSeconds, duration, playerCount, teamCount, kills, medalXp, matchXp, scoreXp, wallBangs, score, totalXp, headshots, assists, challengeXp, scorePerMinute, distanceTraveled, teamSurvivalTime, deaths, kdRatio, bonusXp, gulagDeaths, timePlayed, executions, gulagKills, nearmisses, percentTimeMoving, longestStreak, teamPlacement, damageDone, damageTaken, team, rank, username, uno, season) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    tag, platform, matchID, map, mode, gameType, utcStartSeconds, utcEndSeconds, duration,
                    playerCount, teamCount, kills, medalXp, matchXp, scoreXp, wallBangs, score, totalXp,
                    headshots, assists, challengeXp, scorePerMinute, distanceTraveled, teamSurvivalTime,
                    deaths, kdRatio, bonusXp, gulagDeaths, timePlayed, executions, gulagKills, nearmisses,
                    percentTimeMoving, longestStreak, teamPlacement, damageDone, damageTaken, team, rank,
                    username, uno, season
                )
            else:
                break



        return (matches_data)

    except (KeyError, TypeError, ValueError):
        return None


def usd(value):
    """Format value as USD."""
    return f"${value:,.2f}"

def zap(value):
    """Format value as USD."""
    return f"{value:,.0f}"

def check_username(username):
    """ Checks username for illegal characters."""
    regex = re.compile('[@_!$%^&*()<>?/\|}{~:]')

    if(regex.search(username) == None):
        print("username verified")
        return True
    else:
        print("illegal characters in username.")
        return False

def check_nick(nick):
    """ Checks a nickname for illegal characters. """

    if not nick:
        return apology("Please enter a nickname", 400)
    elif not check_username(nick):
        return apology("Please enter a valid nickname", 400)
    elif not "#" in nick:
        return apology("Please enter a valid nickname", 400)
    else:
        return None

def tag_not_assigned(tag, platform):
    """ Checks if the user has this tag in the database as his profile. """

    if not db_wz.execute("SELECT id FROM users WHERE tag = ? AND platform = ?", tag, platform):
        return True
    else:
        return False

def user_has_tag(username):
    """ Checks if the user has a tag in the database as his profile. """

    if db_wz.execute("SELECT id FROM users WHERE username = ?", username):
        return True
    else:
        return False

def users_tag(username):
    """ Returns the tag and platform of the user. """
    # if user has a tag in the database, assign tag and platfor to global variables
    if db_wz.execute("SELECT tag, platform FROM users WHERE username = ?", username):
        global user_tag
        global user_platform
        user_tag, user_platform = db_wz.fetchone()

        print("global user_tag, user_platform: ", user_tag, user_platform)
        return user_tag, user_platform
    else:
        return None

