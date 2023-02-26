# Nairobi-Spaces# By FeverCode

## Nairobi-Spaces

## Table of Content

+ [Description](#description)
+ [Requirements](#requirements)
+ [Installation](#installation)
+ [Running Project](#running-project)
+ [Running Tests](#running-tests)
+ [Api Endpoints](#api-endpoints)
+ [Project Objectives](#project-objectives)
+ [BDD](#bdd)
+ [Technologies Used](#technologies-used)
+ [Licence](#licence)
+ [Authors Info](#authors-info)

## Description

 Nairobi Spaces is a community building webapp which gives people the opportunity to organise groups and host in-person events for people with similar interest at budget friendly rates.

Live link to the project
[Nairobi Spaces](https://nairobi-spaces.up.railway.app)

## Requirements

+ A computer running on either Windows, MacOS or Ubuntu operating system installed with the following:

```-Python version 3.8
    -Django
    -Pip
    -virtualenv
```

## Installation

+ Open Terminal {Ctrl+Alt+T} on ubuntu
+ git clone `https://github.com/FeverCode/Nairobi-Spaces`
+ cd Nairobi-Spaces
+ code . or atom . based on prefered text editor

## Running Project

+ On terminal where you have opened the cloned project
  + `sudo pip3 install virtualenv` - To install virtual enviroment
  + `virtualenv venv` - To create virtual enviroment
  + `source venv/bin/activate` - To activate virtual enviroment
  + `pip install -r requirements.txt` - To install requirements
  + Setup your database User, Password, Host, Port and Database Name.
  + `make makemigrations` - To create migrations
  + `make migrate` - To migrate database  
  + `make` - to start the server

## Running Tests

+ To run test for the project
  + `$ make test`

## Api Endpoints

## Project Objectives

+ The project has a functioning authentication system
+ The project contains migration files for the different model structure
+ The project has a user model
+ The project has a profile page
+ The project has a User Dasboard
+ Users can edit and delete reservations
+ Users can make reservations
+ Users can view their reservations
+ Users can view all reservations

## BDD

## Behaviour Driven Development (BDD)

| Behaviour | Input | Output |
| :---------------- | :---------------: | ------------------: |
| Load the page | **On page load** | Get to the landing page, View Deals, Select between signup and login|
|Select View Deals | **Our Deals**| Get to page with curated MeetUp Mtaani Deals|
| Select SignUp| **Email**,**Username**,**Password** | Redirect to login|
| Select Login | **Username** and **password** | Redirect to page with dashboards and view of the landing page|
| Select reserve button | **Reserve** | Form that you input your MeetUp Mtaani deal and reserve details|
| Click on reserve | **Add Reservation** | Saves selected choices to dashboard|
|Select Dasboard | **Active Reservations**| Get reserved spots|
|Click delete icon | **Delete Icon**| Deletes reservation from view|
|Click Edit Button | **Edit Icon**| Get to add reserve form to edit|

## Technologies Used

+ python3.8
+ django 3.2
+ Cloudninary (for hosting images)
+ Heroku (for hosting the project)
+ Rest framework (for API)

## Licence

MIT License

Copyright (c) [2022] [FeverCode]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Authors Info

LinkedIn - [https://www.linkedin.com/in/gedion-onsongo-112543210/]
