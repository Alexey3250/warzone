
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

## API
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



## Features

- Login/Logout
- Save your profile
- Analyze your performance
- Show history of matches
- Compare 2 players
- A meme error generator

## Style

Base for css stylyes is used from Bootstrap css library. Website is using tiled css structure for the contend and is scalable for different screen sizes.

## Optimizations

Actions related to queries in the database that will not be used in the rendering of a page are parallel processed for faster speed.


## Screenshots

![Error meme generator](http://memegen.link/custom/400/404----Not-found.-Incorrect-username-or-platform~q-Misconfigured-privacy-settings~q.jpg?alt=https://stickerly.pstatic.net/sticker_pack/tldPp6gNqYovolcIcaYEg/NV385B/2/efd6d682-da26-4cf0-b5e5-9ad8b7b20bb7.png&width=400)


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

## Color Reference

| Color             | Hex                                                                |
| ----------------- | ------------------------------------------------------------------ |
| Example Color | ![#0a192f](https://via.placeholder.com/10/0a192f?text=+) #0a192f |
| Example Color | ![#f8f8f8](https://via.placeholder.com/10/f8f8f8?text=+) #f8f8f8 |
| Example Color | ![#00b48a](https://via.placeholder.com/10/00b48a?text=+) #00b48a |
| Example Color | ![#00d1a0](https://via.placeholder.com/10/00b48a?text=+) #00d1a0 |


## Acknowledgements

 - [CS50x](https://cs50.harvard.edu/x/2022/psets/0/)


## Authors

- [Alexey Efimik](https://github.com/Alexey3250)

