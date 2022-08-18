
# Warzone data website

A final project for Harward's CS50x course.

Warzone data website that shows your gaming prfrormance in Call of Duty Warzone.

Developed in Python using Flask framework. + SQL, HTML, CSS, JavaScript

## Features

- Show your gaming performance
- Watch history of matches
- Compare to other players
- login/logout
- save your profile

## Backend

When you fill the form with your username and platform, you will be redirected to the page with your data. Meanwhile on the background the backend calls API and gets your data. Data is received in json format and then parsed to flat structure and saved to the SQL database. After this page is calling the backend again and getting the data from the database.

API receives 2 inputs: username and platform:

```
MAD%25239849741, type: <class 'str'>; acti, type: <class 'str'>
```
Before making a call the backend checks for user imput and if it is valid, it calls the API and gets the data. "#" symbol in the nickname is converted to "%2523".

### API
API used for data: https://rapidapi.com/elreco/api/call-of-duty-modern-warfare

#### Advantages of this API:
+ easy to use and authenticate
+ freemium

#### Disadvantages of this API:
+ limited to 500 requests per day
+ often produces errors
+ gets limited data to 20 matches only (not all matches)
+ last time updated 1 year ago. So this 
+ lacks data on the attachements for the guns
+ lacks data on teammates

### Graphs
Chart.js is used for the graphs.
<a href="https://ibb.co/pKC09r7"><img src="https://i.ibb.co/pKC09r7/Screenshot-2022-08-18-133548.png" alt="Screenshot-2022-08-18-133548" border="0"></a> <a href="https://ibb.co/q1cmspp"><img src="https://i.ibb.co/q1cmspp/Screenshot-2022-08-18-133603.png" alt="Screenshot-2022-08-18-133603" border="0"></a> <a href="https://ibb.co/4sn5Y98"><img src="https://i.ibb.co/4sn5Y98/Screenshot-2022-08-18-133823.png" alt="Screenshot-2022-08-18-133823" border="0"></a> <a href="https://ibb.co/k3rMQQY"><img src="https://i.ibb.co/k3rMQQY/Screenshot-2022-08-18-133928.png" alt="Screenshot-2022-08-18-133928" border="0"></a>


## Features

- Login/Logout
- Save your profile
- Analyze your performance
- Show history of matches
- Compare 2 players
- A meme error generator 
  <a href="http://memegen.link/custom/400/404----Not-found.-Incorrect-username-or-platform~q-Misconfigured-privacy-settings~q.jpg?alt=https://stickerly.pstatic.net/sticker_pack/tldPp6gNqYovolcIcaYEg/NV385B/2/efd6d682-da26-4cf0-b5e5-9ad8b7b20bb7.png&width=400"><img src="http://memegen.link/custom/400/404----Not-found.-Incorrect-username-or-platform~q-Misconfigured-privacy-settings~q.jpg?alt=https://stickerly.pstatic.net/sticker_pack/tldPp6gNqYovolcIcaYEg/NV385B/2/efd6d682-da26-4cf0-b5e5-9ad8b7b20bb7.png&width=400" alt="Screenshot-2022-08-18-133006" border="0"></a>

## Style

Base for css stylyes is used from Bootstrap css library. Website is using tiled css structure for the contend and is scalable for different screen sizes.

## Optimizations

Actions related to queries in the database that will not be used in the rendering of a page are parallel processed for faster speed.


## Screenshots
<a href="https://ibb.co/y4QcK7N"><img src="https://i.ibb.co/hYmJrwg/screencapture-127-0-0-1-5000-2022-08-18-13-31-41.png" alt="screencapture-127-0-0-1-5000-2022-08-18-13-31-41" border="0"></a>
<a href="https://ibb.co/99K1qhf"><img src="https://i.ibb.co/LzjcCrq/screencapture-127-0-0-1-5000-2022-08-18-13-34-05.png" alt="screencapture-127-0-0-1-5000-2022-08-18-13-34-05" border="0"></a>
<a href="https://ibb.co/MpBqsk0"><img src="https://i.ibb.co/k0mYx2C/screencapture-127-0-0-1-5000-compare-2022-08-18-13-35-28.png" alt="screencapture-127-0-0-1-5000-compare-2022-08-18-13-35-28" border="0"></a>

## Lessons Learned

### Strange python error

There was a wierd error calling "matches(tag, profile)" function. For some reason it stopped working and was giving me and error: "You are trying to pass 2 positional arguments while the function takes 0".
It took me 2 days to figure this out. It was solved by copyiing "matches()" function in helpers.py to "matches2()" and without any other changes it started to work. I'm still wondering till this day what was the issue there.
[What did we learn?](https://www.youtube.com/watch?v=J6VjPM5CeWs&ab_channel=UltraMiraculous)

### Chart.js documentation is a mess
Chart.js library looks very simple at first. It's qiute simple to draw very basic charts. However, when you try to customize the charts it becomes a headache. For some reason sometimes you change 1 thing and chart dissapears. It takes time just to render chart on the page again. When you look at the docmentation everything is scattered around the place. Sometimes even copypasted code from the documentation does not work. It probably needs a whole course. It takes time.

## Roadmap

- Finish more courses on web developement
- Rewrite a website for better speed and use a different API to get complete data

## Acknowledgements

 - [CS50x](https://cs50.harvard.edu/x/2022/psets/0/)


## Authors

- [Alexey Efimik](https://github.com/Alexey3250)

