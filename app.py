import os
import datetime
import json
import threading
import concurrent.futures

from cs50 import SQL
from flask import Flask, flash, redirect, url_for, render_template, request, session, jsonify
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, matches2, users_tag, login_required, usd, search, matches, matches2, zap, check_username, check_nick, tag_not_assigned, user_has_tag, radar_compare

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")
db_wz = SQL("sqlite:///warzone.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")

# TODO: Adding a timer to unpade the database for tag and platform in successfeul_searches
# Use a parallel process for a countdown timer and an update to the datamase using matches() for each tag and platform
# This will be done in a separate thread




@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/", methods=["GET", "POST"])
def index2():
    """Search warzone stats."""
    if request.method == "GET":
        return render_template("index.html")
    else:
        nick = request.form.get("nick")
        if nick != None:
            tag = nick.replace("#","%2523")

        # Assign a platform from session
        platform = session.get("platform")
        platform = request.form.get("platform")
        print(f"Imput received: {tag}, type: {type(tag)}; {platform}, type: {type(platform)}")

        # Check if nick is correct
        check_nick(nick)

        # Check if the platform is correct
        if not platform:
            return apology("Input the platform")

        else:
            # search and save to a database
            message = search(tag, platform)

            # Check if we received an error
            if message != "ok":
                return apology("%s" % message)

            ##!! Error: TypeError: takes 0 positional arguments but 2 was given
            matches2(tag, platform)
            
            # Get data from matches table for this tag and platform, ordered by newest
            matches = db_wz.execute("SELECT * FROM matches WHERE platform = :platform AND tag = :tag ORDER BY entry_id DESC LIMIT 25", platform=platform, tag=tag)

            # Add a tag and platform to the table of successful_searches if it doesn't exist
            if not db_wz.execute("SELECT * FROM successful_searches WHERE tag = ? AND platform = ?", tag, platform):
                db_wz.execute("INSERT INTO successful_searches (tag, platform) VALUES (?, ?)", tag, platform)

            # Setting the values
            warzone_values = 0
            # Select values from the database
            warzone_values = db_wz.execute("SELECT * FROM br_all WHERE tag= ? ORDER BY entry_id DESC LIMIT 1", tag)

            # TODO: add a debug if we cant find an entry
            if not warzone_values:
                return apology("couldn't find")

            wins = warzone_values[0]["wins"]
            kills = warzone_values[0]["kills"]
            deaths = warzone_values[0]["deaths"]
            timePlayed = round(warzone_values[0]["timePlayed"] / 3600)
            kd = round(warzone_values[0]["kdRatio"], 2)
            top25 = warzone_values[0]["topTwentyFive"]
            top10 = warzone_values[0]["topTen"]
            top5 = warzone_values[0]["topFive"]
            top1 = warzone_values[0]["wins"]
            # Create a list of top25, top10, top5, top1
            top = [top25, top10, top5, top1]

            ## Creating a kills/deaths chart

            # Query to a database to get the kills, deaths, timestamp, teamPlacement from matches tables
            # Make each query in a separate thread

            kills_timeline = db_wz.execute("SELECT kills FROM matches WHERE tag= ? ORDER BY entry_id", tag)
            deaths_timeline = db_wz.execute("SELECT deaths FROM matches WHERE tag= ? ORDER BY entry_id", tag)
            timestamp_timeline = db_wz.execute("SELECT timestamp FROM matches WHERE tag= ? ORDER BY entry_id", tag)
            teamPlacement_timeline = db_wz.execute("SELECT teamPlacement FROM matches WHERE tag= ? ORDER BY entry_id", tag)

            # Query for running average kdRatio
            kd_timeline = db_wz.execute("SELECT kdRatio FROM matches WHERE tag= ? ORDER BY entry_id", tag)


            # Convert to a list of numbers
            kills_timeline = [int(i["kills"]) for i in kills_timeline]
            deaths_timeline = [-int(i["deaths"]) for i in deaths_timeline]
            teamPlacement_timeline = [int(i["teamPlacement"]) for i in teamPlacement_timeline]
            kd_timeline = [round(i["kdRatio"], 2) for i in kd_timeline]

            # Calculate the running average
            kd_timeline = [sum(kd_timeline[:i+1])/len(kd_timeline[:i+1]) for i in range(len(kd_timeline))]

            # Convert timestamp_timeline to a list of strings
            timestamp_timeline = [i["timestamp"] for i in timestamp_timeline]

            ## Logic for the buttons

            # Check if we have this profile saved in users table
            tag_check = tag_not_assigned(tag, platform)
            print(f" {tag} is not assignet to a user: {tag_check}")
            # Check if the user has his tag in the users table

            if tag_check:
                can_add = True
            else:
                can_add = False


            # Check if we are logged in
            if session.get("user_id"):
                login_status = True
                
                # Parallel processing to request for assigned tag and platform in users table for current user
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    print("Starting threads")
                    future_to_tag = {executor.submit(users_tag(session["user_id"]))}
                    # clear the thread pool
                    executor.shutdown(wait=True)
                    print("Threads finished")
            else:
                login_status = False



            # adding the tag and platform to session
            session["tag"] = tag
            session["platform"] = platform

            # printing session data
            print(f"session: {session}")

            if request.form.get('set_profile') == 'set_profile':
                print("set_profile")
                 # Add the tag and platform to the user in users table
                db_wz.execute("UPDATE users SET tag = ?, platform = ? WHERE id = ?", tag, platform, session["user_id"])
                print(f"{tag} has been added to the users table")



            return render_template("searched.html", nick=nick, platform=platform,
                kills=zap(kills), wins=zap(wins), timePlayed=zap(timePlayed), kd=kd,
                kills_timeline=kills_timeline, deaths=zap(deaths), deaths_timeline=deaths_timeline,
                timestamp_timeline=timestamp_timeline, teamPlacement_timeline=teamPlacement_timeline,
                kd_timeline=kd_timeline, tag_check=tag_check, login_status=login_status,
                can_add=can_add, top25=top25, top10=top10, top5=top5, top1=top1, top=top, matches=matches)

@app.route("/compared", methods=["GET", "POST"])
def compared():
    """For charts"""
    if request.method == "GET":
        return render_template("compared.html")
    else:
        return render_template("compared.html")

@app.route("/compare", methods=["GET", "POST"])
def compare():
    """Compare two profiles."""
    if request.method == "GET":
        return render_template("compare.html")
    else:
        # Recieve the nicknames from the form
        nick1 = request.form.get("nick1")
        nick2 = request.form.get("nick2")
        if nick1 != None and nick2 != None:
            tag1 = nick1.replace("#","%2523")
            tag2 = nick2.replace("#","%2523")

        # Assign a platform from session and from the form
        platform1 = session.get("platform1")
        platform1 = request.form.get("platform1")
        platform2 = request.form.get("platform2")
        print(f"Tag1: {tag1}; Platform1: {platform1};   Tag2: {tag2}; Platform2: {platform2}")

        # Check if nick is correct
        check_nick(nick1)
        check_nick(nick2)
        # Check if the platform is correct
        if not platform1 or not platform2:
            return apology("Input the platform")

        else:
            # Add a tag and platform to the table of successful_searches if it doesn't exist
            if not db_wz.execute("SELECT * FROM successful_searches WHERE tag= ? AND platform= ?", tag1, platform1):
                message = search(tag1, platform1)

            if not db_wz.execute("SELECT * FROM successful_searches WHERE tag= ? AND platform= ?", tag2, platform2):
                message2 = search(tag2, platform2)
            
            # Open a second thread to use matches2 function. Just to update the database for the users on the background
            with concurrent.futures.ThreadPoolExecutor() as executor:
                print("Starting threads")
                future_to_tag = {executor.submit(matches2(tag1, platform1), matches2(tag2, platform2))}
                # clear the thread pool
                executor.shutdown(wait=True)
                print("Threads finished")
            
            # Add a tag and platform to the table of successful_searches if it doesn't exist
            if not db_wz.execute("SELECT * FROM successful_searches WHERE tag = ? AND platform = ?", tag1, platform1):
                db_wz.execute("INSERT INTO successful_searches (tag, platform) VALUES (?, ?)", tag1, platform1)
            if not db_wz.execute("SELECT * FROM successful_searches WHERE tag = ? AND platform = ?", tag2, platform2):
                db_wz.execute("INSERT INTO successful_searches (tag, platform) VALUES (?, ?)", tag2, platform2)
            # Query for the matches data
            player1_data = db_wz.execute("SELECT * FROM matches WHERE tag = ? AND platform = ?", tag1, platform1)
            player2_data = db_wz.execute("SELECT * FROM matches WHERE tag = ? AND platform = ?", tag2, platform2)
            
            # Query for the last data entry in br table for each player and saving to list class variables
            player1_br = db_wz.execute("SELECT * FROM br WHERE tag = ? AND platform = ? ORDER BY timestamp DESC LIMIT 1", tag1, platform1)
            player2_br = db_wz.execute("SELECT * FROM br WHERE tag = ? AND platform = ? ORDER BY timestamp DESC LIMIT 1", tag2, platform2)
            player1_br_all = db_wz.execute("SELECT * FROM br_all WHERE tag = ? AND platform = ? ORDER BY timestamp DESC LIMIT 1", tag1, platform1)
            player2_br_all = db_wz.execute("SELECT * FROM br_all WHERE tag = ? AND platform = ? ORDER BY timestamp DESC LIMIT 1", tag2, platform2)
            player1_br_dmz = db_wz.execute("SELECT * FROM br_dmz WHERE tag = ? AND platform = ? ORDER BY timestamp DESC LIMIT 1", tag1, platform1)
            player2_br_dmz = db_wz.execute("SELECT * FROM br_dmz WHERE tag = ? AND platform = ? ORDER BY timestamp DESC LIMIT 1", tag2, platform2)
            print(f"player1_br: {player1_br}, {type(player1_br)}")
            print(f"player2_br: {player2_br}, {type(player2_br)}")
            
            # Converting lists to individual variables
            player1_br_wins = player1_br[0]["wins"]
            player1_br_kills = player1_br[0]["kills"]
            player1_br_kdRatio = player1_br[0]["kdRatio"]
            player1_br_deaths = player1_br[0]["deaths"]
            player1_br_downs = player1_br[0]["downs"]
            player1_br_topTwentyFive = player1_br[0]["topTwentyFive"]
            player1_br_topTen = player1_br[0]["topTen"]
            player1_br_topFive = player1_br[0]["topFive"]
            player1_br_contracts = player1_br[0]["contracts"]
            player1_br_revives = player1_br[0]["revives"]
            player1_br_score = player1_br[0]["score"]
            player1_br_scorePerMinute = player1_br[0]["scorePerMinute"]
            player1_br_timePlayed = player1_br[0]["timePlayed"]
            
            player2_br_wins = player2_br[0]["wins"]
            player2_br_kills = player2_br[0]["kills"]
            player2_br_kdRatio = player2_br[0]["kdRatio"]
            player2_br_deaths = player2_br[0]["deaths"]
            player2_br_downs = player2_br[0]["downs"]
            player2_br_topTwentyFive = player2_br[0]["topTwentyFive"]
            player2_br_topTen = player2_br[0]["topTen"]
            player2_br_topFive = player2_br[0]["topFive"]
            player2_br_contracts = player2_br[0]["contracts"]
            player2_br_revives = player2_br[0]["revives"]
            player2_br_score = player2_br[0]["score"]
            player2_br_scorePerMinute = player2_br[0]["scorePerMinute"]
            player2_br_timePlayed = player2_br[0]["timePlayed"]
            
            ## Creating numbers for the radar chart - BR only
                
            # Calling the radar_compare function to compare the 2 players

            br_Rwins = radar_compare(player1_br[0]["wins"], player2_br[0]["wins"])
            br_RkdRatio = radar_compare(player1_br[0]["kdRatio"], player2_br[0]["kdRatio"])
            br_RtimePlayed = radar_compare(player1_br[0]["timePlayed"], player2_br[0]["timePlayed"])
            br_RscorePerMinute = radar_compare(player1_br[0]["scorePerMinute"], player2_br[0]["scorePerMinute"])
            br_Rkills = radar_compare(player1_br[0]["kills"], player2_br[0]["kills"])
            br_Rdeaths = radar_compare(player1_br[0]["deaths"], player2_br[0]["deaths"])
            
            # make a list for each player radar chart data
            player1_br_radar = (br_Rwins[0], br_RkdRatio[0], br_RtimePlayed[0], br_RscorePerMinute[0], br_Rkills[0], br_Rdeaths[0])
            player2_br_radar = (br_Rwins[1], br_RkdRatio[1], br_RtimePlayed[1], br_RscorePerMinute[1], br_Rkills[1], br_Rdeaths[1])
            player1_br_radar = list(player1_br_radar)
            player2_br_radar = list(player2_br_radar)

            
            ## DATA FOR THE KD GRAPHS
            # Load kd over last matches from matches table
            kd_timeline1 = db_wz.execute("SELECT kdRatio FROM matches WHERE tag = ? AND platform = ? ORDER BY entry_id DESC", tag1, platform1)
            kd_timelime2 = db_wz.execute("SELECT kdRAtio FROM matches WHERE tag = ? AND platform = ? ORDER BY entry_id DESC", tag2, platform2)
            # Conversion from nested list to a list of values
            kd_timeline1 = [kd_timeline1[i]["kdRatio"] for i in range(len(kd_timeline1))]
            kd_timeline2 = [kd_timelime2[i]["kdRatio"] for i in range(len(kd_timelime2))]

            # Check which list is longer kd_timeline1 or kd_timeline2 and assgn a minimun length of the list to a value
            if len(kd_timeline1) > len(kd_timeline2):
                kd_timeline_min = len(kd_timeline2)
                # if kd_timeline1 is longer, cut the rest of the values in kd_timeline1
                kd_timeline1 = kd_timeline1[:kd_timeline_min]
            else:
                kd_timeline_min = len(kd_timeline1)
                # if kd_timeline2 is longer, cut the rest of the values in kd_timeline2
                kd_timeline2 = kd_timeline2[:kd_timeline_min]
            
            print(f"kd_timeline1: {kd_timeline1}, {type(kd_timeline1)}, len: {len(kd_timeline1)}")
            print(f"kd_timeline2: {kd_timeline2}, {type(kd_timeline2)}, len: {len(kd_timeline2)}")
            
            print(player1_br_radar)

                
            
                
            
            
            return render_template("compared.html", player1_data=player1_data, player2_data=player2_data, nick1=nick1, nick2=nick2, player1_br_radar=player1_br_radar, player2_br_radar=player2_br_radar, kd_timeline1=kd_timeline1, kd_timeline2=kd_timeline2)

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    """ Dashboard shows your stats like in search.html """
    if request.method == "GET":
        print("/dashboard: GET")
        # TODO: add a check if the user is logged in
        return render_template("searched.html")

    else:
        print("/dashboard: POST")
        # Check if the user is logged in
        if not session.get("user_id"):
            return apology("You must be logged in")

        # Get the tag and platform from session
        tag = session["tag"]
        platform = session["platform"]
        nick = tag.replace("%2523", "#")


        return render_template("dashboard.html", tag=tag, platform=platform, nick=nick)

@app.route("/squad", methods=["GET", "POST"])
def squad():
    """ Squad stats """
    if request.method == "GET":
        return render_template("squad.html")
    else:
        return render_template("squad.html")

@app.route("/history", methods=["GET", "POST"])
def history():
    """ Matches stats """
    if request.method == "GET":
        return render_template("matches.html")
    else:
        return render_template("matches.html")

@app.route("/matches", methods=["GET", "POST"])
def matches():
    """ Matches stats """
    if request.method == "GET":
        print("/matches: GET")
        
        # Get user and platform from session
        user = session["user_id"]
        platform = "acti"
        tag = "MAD%25239849741"
        
        # Get data from matches table for this tag and platform, ordered by newest
        matches = db_wz.execute("SELECT * FROM matches WHERE platform = :platform AND tag = :tag ORDER BY entry_id DESC", platform=platform, tag=tag)
        
        
        return render_template("matches.html", matches=matches)
    else:
        print("/matches: POST")
        return render_template("matches.html")

@app.route("/searched", methods=["GET", "POST"])
def searched():
    """Manipulations with the searched profile"""
    if request.method == "POST":
        print("executing /searched 'POST'")

        if request.form.get("set_profile"):
            # Check if the user is logged in
            if not session.get("user_id"):
                return apology("You must be logged in")

            # Get the tag and platform from session
            tag = session["tag"]
            platform = session["platform"]
            nick = tag.replace("%2523", "#")

            # Check if the user has his tag in the users table
            tag_check = tag_not_assigned(tag, platform)
            print(f" {tag} is not assignet to a user: {tag_check}")
            if tag_check:
                can_add = True
            else:
                can_add = False


            if request.form.get('set_profile') == 'set_profile':
                 # Add the tag and platform to the user in users table
                db_wz.execute("UPDATE users SET tag = ?, platform = ? WHERE id = ?", tag, platform, session["user_id"])
                print(f"{tag} has been added to the users table")

            return render_template("searched.html", tag=tag, platform=platform, nick=nick, can_add=can_add)

    else:
        return render_template("searched.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db_wz.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")

    else:
        # if POST, get the input
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Checks for correct input
        if not username:
            return apology("Username is blank")
        if not check_username(username):
            return apology("Username is invalid")
        if not password:
            return apology("Where is your password?")
        if password != confirmation:
            return apology("Passwords do not match")

        # Generating secure hash password
        hash = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)

        # If everything is fine, check and store the password
        try:
            if check_password_hash(hash, password):
                # insert into database /line 26
                new_user = db_wz.execute("INSERT INTO users(username, hash) VALUES(?, ?)", username, hash)
            else:
                return apology("Password is not secure")
        except:
            return apology("Username already exists")

        # Create a new session
        session["user_id"] = new_user

        return redirect("/")

@app.route("/test", methods=["GET", "POST"])
def test():
    """Test page"""
    if request.method == "GET":
        return render_template("test.html")
    else:
        # if POST, get the input
        username = request.form.get("username")
        # If user pressed on assigned button
        if request.form['assigned'] == "assigned":
            # get the tag and platform from session
            tag = session["tag"]
            platform = session["platform"]
            # get the user_id from session
            user_id = session["user_id"]
            # add the tag and platform to the table of users
            db_wz.execute("INSERT INTO users (user_id, tag, platform) VALUES (?, ?, ?)", user_id, tag, platform)
            return redirect("/dashboard")
        return render_template("test.html")

@app.route("/about", methods=["GET", "POST"])
@login_required
def about():
    """About me."""
    if request.method == "GET":
        return render_template("about.html")
    else:
        return redirect("/")

