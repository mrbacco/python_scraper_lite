#############################################
# Project: basic web application for scraping
# Author: mrbacco
# email: mrbacco@mrbacco.com
# Date: H1 2021
# main file: app.py
#############################################

############## import START ##############

from flask import Flask, render_template, url_for, session, request, redirect, logging, flash  # modules from flask for web server
import cgi, cgitb
import pymongo # driver for mongdb connectivity
import pandas as pd
import scrapy as scrapy
from wtforms import Form, StringField, TextAreaField, PasswordField, validators # FOR THE WEBFORMS
#from flask_wtf import URLField
from passlib.hash import sha512_crypt # password hashing
import logging
from functools import wraps
from flask_mail import Mail, Message
from datetime import datetime
from bs4 import BeautifulSoup
import requests
import pprint
import json
from json2html import *
from pathlib import Path
import shutil
import os.path
import codecs

############## import END ##############


app = Flask(__name__) # creating an instalnce of the Flask class for thsi app as web server
app.secret_key="supercalifragilistichespiralidoso74"

# creation of a date&time object to be used in the databse
time = datetime.now() 
readtime = time.strftime("%d-%b-%Y (%H:%M:%S.%f)")

############## email server SETUP START ##############


############## email server SETUP END ##############


############## defining the routes for the different web pages START ##############

# definition of a class for the form used in signup, login, and web scraping
class Init(Form): #this is for registering
    email = StringField('Email', [validators.DataRequired(),validators.Email()])
    name = StringField('Name', [validators.DataRequired(),validators.length(min=1, max=50)])
    username = StringField('Username', [validators.DataRequired(),validators.DataRequired(),validators.length(min=5, max=15)])
    password = PasswordField("Password", [validators.DataRequired(), validators.length(min=6, max=14)])

class Scrape(Form): #this is for scraping
    url = StringField('URL', [validators.DataRequired(),validators.URL()])

class Signin(Form): #this is for signing in
    username = StringField('Username', [validators.DataRequired(),validators.DataRequired(),validators.length(min=5, max=15)])
    password = PasswordField("Password", [validators.DataRequired()])

# route for the web scraping home page 
@app.route("/", methods = ['GET', 'POST']) # this is the route to the homepage for scraping
def index():
    #the commented code below is now under the dashboard route
    
    form = Scrape(request.form)
    if request.method == 'GET': # make sure the method used is define above
        return render_template('home.html', form = form), logging.warning("you are under the home page now using GET, well done mrbacco ")
    if request.method == 'POST' and form.validate():
        # the following are the data from the init form
        global url 
        url = form.url.data
        #email = form.email.data
        now01 = str(datetime.now().replace(microsecond=0))
        
        result = requests.get(url) # getting the url from the webform
        print("the requested url is: ", url) # printing the url to make sure the variable contains it
        print("the response code is: ", result.status_code)            
        print(result.headers)
        print("scraping taken place at: ", now01)
        
        # now I can apply the BS4 class to the content of the page
        payload = result.content # defining a new variable that takes the content of the web page
        soup = BeautifulSoup(payload, "lxml") # created "soup": the beautiful soup object to use for scraping

        # this is the actual block of code for the core web scraping
        '''
        for var in soup.find_all("div"): # looping to find all the "div" of the page
            a_tag = var.find_all("a")
            links.append(a_tag)
        '''

        # I'm creating empty lists that will be filled with the result of the scraping
        links = []
        web = []
        par = []

        for www in soup.find_all('a'): # looking for all the hyperlinks in the page and printing them
            web.append(www)
            print("the following are the hypelinks available: ", www.get('href'))
        

        for para in soup.find_all('p'): # looping to find all the "paragraphs" of the page and printing the results
            par.append(para)
            print("the paragraphs are: ", str(para.text))
            # print(links,"\n")
            # value = [a.text for a in soup.find_all("links")] #looping to find all the links in the page references
            # values.append(value)
        # tot = values.count("...")
        # pprint.pprint(values) #using .text allows to extract only the text on the webpage and not the tags
        
        print("the requested title name is  :", soup.title.name)
        print("the requested title is  :", soup.title)
        print("the requested title parent name is  :", soup.title.parent.name)
        now = str(datetime.now().replace(microsecond=0))

        # defining a new variable taking as input the values from the init form to populate the DB
        mymsg={
                "date":now01,
                "url": url,
                "responsecode": result.status_code,
                # "header" : result.headers,
                # "email" : email,
                "titlename" : str(soup.title.name),
                "title" : str(soup.title),
                # "title parent name" : str(soup.title.parent.name),
                "paragraphs" : str(par),
                "hypelinks" : str(web)
              }
        res_1w = json.dumps(mymsg, indent=4)

        with open("message.json", "w") as out_file:
            json.dump(res_1w, out_file, ensure_ascii=False, indent=4)

        # x = mycol.insert_many(mymsg), print("inserting this item: ", mymsg) # insert the list into the mongo db
    flash("Thanks, please click on the results page now","success")
    return render_template('home.html', form=form), print("you are under the home page now, mrbacco")

#route for the dashboard page 
@app.route("/dashboard", methods = ['GET', 'POST'])
def dashboard():
    try:
        with codecs.open("message.json", "r", encoding='utf-8', errors='ignore') as r_file:
            in_file = json.load(r_file)

        formatted_table = json2html.convert(json=in_file)

        your_file = codecs.open("results.html", "w", encoding='utf-8', errors='ignore')
        your_file.write(formatted_table)
        your_file.close()

        shutil.copy2("/home/mrbacco/Desktop/__PROGRAMMING__/PROJECTS/webapp_py/results.html",
                     "/home/mrbacco/Desktop/__PROGRAMMING__/PROJECTS/webapp_py/templates")

        return render_template('dashboard.html',tasks=your_file)
    except:
        flash("No Data, please try to scrape again","danger")
    
    print("\n", "you are under the dashboard page now")
    return render_template('dashboard.html')


############## defining the routes for the different web pages END ##############


####################################################################################################
# running the app and enabling debug mode so that I can update the app.py without the need of manual restart
if __name__ == "__main__":
    app.secret_key="supercalifragilistichespiralidoso74"
    app.run(debug=True)
