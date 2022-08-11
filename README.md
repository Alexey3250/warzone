
# Warzone data website

A final project for Harward's CS50x course.

Warzone data website that shows your gaming prfrormance in Call of Duty Warzone.

Developed in Python using Flask framework. + SQL, HTML, CSS, JavaScript

API used for data: 



## Features

- Login/Logout
- Save your profile
- Analyze your performance
- Show history of matches
- Compare 2 players
- A meme error generator


## Optimizations

Actions related to queries in the database that will not be used in the rendering of a page are parallel processed for faster speed.


## Screenshots

![App Screenshot](https://via.placeholder.com/468x300?text=App+Screenshot+Here)


## Lessons Learned

### Strange python error

There was a wierd error calling "matches(tag, profile)" function. For some reason it stopped working and was giving me and error: "You are trying to pass 2 positional arguments while the function takes 0".
It took me 2 days to figure this out. It was solved by copyiing "matches()" function in helpers.py to "matches2()" and without any other changes it started to work. I'm still wondering till this day what was the issue there.
[What did we learn?](https://www.youtube.com/watch?v=J6VjPM5CeWs&ab_channel=UltraMiraculous)

### Chart.js documentation is a mess
Chart.js library looks very simple at first. It's qiute simple to draw very basic charts. However, when you try to customize the charts it becomes a headache. For some reason sometimes you change 1 thing and chart dissapears. It takes time just to render chart on the page again. When you look at the docmentation everything is scattered around the place. It probably needs a whole course and learning it takes time.

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

