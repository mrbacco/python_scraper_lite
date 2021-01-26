##############################################
# Project: basic web application for scraping          
# Author: mrbacco                                      
# email: mrbacco@yahoo.com                             
# Date: H1 2021                                        
# main file: app.py                                    
##############################################

from flask import Flask, render_template, url_for, session, request, redirect, logging, flash  # modules from flask for web server
import cgi, cgitb
import pymongo # driver for mongdb connectivity
import pandas as pd
import scrapy as scrapy
from wtforms import Form, StringField, TextAreaField, PasswordField, validators # FOR THE WEBFORMS
# from flask_wtf import URLField
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



app = Flask(__name__) # creating an instalnce of the Flask class for thsi app as web server
app.secret_key="mrbacco_millenovecentosettantaquattro"

# readtime = time.strftime("%d-%b-%Y (%H:%M:%S.%f)")


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
        # creation of a date&time object to be used to store data
        now01 = str(datetime.now().replace(microsecond=0)) 

        
        result = requests.get(url) # getting the url from the webform
        print("\n", "the requested url is: ", url) # printing the url to make sure the variable contains it
        print("\n", "the response code is: ", result.status_code)            
        print("\n", result.headers)
        print("\n", "scraping taken place at: ", now01)
        
        # now I can apply the BS4 class to the content of the page
        payload = result.content # defining a new variable that takes the content of the web page
        soup = BeautifulSoup(payload, "html.parser") # created "soup": the beautiful soup object to use for scraping

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
            print("\n", "the following are the hypelinks available: ", www.get('href'))

        for para in soup.find_all('p'): # looping to find all the "paragraphs" of the page and printing the results
            par.append(para)
            # print("\n", "the paragraphs are: ", str(para.text))
            # print(links,"\n")
            # value = [a.text for a in soup.find_all("links")] #looping to find all the links in the page references
            # values.append(value)
        # tot = values.count("...")
        # pprint.pprint(values) #using .text allows to extract only the text on the webpage and not the tags
        
        # print("\n", "the requested title name is  :", soup.title.name)
        print("\n", "the requested title is  :", soup.title)
        # print("\n", "the requested title parent name is  :", soup.title.parent.name)
        now = str(datetime.now().replace(microsecond=0))
       
        # defining a new variable taking as input the values from the init form to populate the DB
        mymsg={
                "date": now01,
                "url": url,
                "response code": result.status_code,
                # "header" : result.headers,
                # "email" : email,
                # "title name" : str(soup.title),
                "title" : str(soup.title),
                # "title parent name" : str(soup.title.parent.name),
                "paragraphs" : str(par),
                "hypelinks" : str(web)
              }
        
        res_1w = json.dumps(mymsg, indent=4) # serializing the object mymsg

        # writing the content mymsg into a local JSON file
        with open("message.json", "w") as out_file:
            json.dump(res_1w, out_file, ensure_ascii=False, indent=4)
        # print ("\n", " this is the serialized json: ", "\n", res_1w)
       

        # x = mycol.insert_many(mymsg), # print("\n", "inserting this item: ", mymsg) # insert the list into the mongo db
    flash("Thanks, please click on the results page now","success")
    return render_template('home.html', form=form), print("you are under the home page now, mrbacco")


#route for the dashboard page 
@app.route("/dashboard", methods = ['GET'])

def dashboard():

    try:

        with codecs.open("message.json", "r", encoding='utf-8', errors='ignore') as r_file:
            input = json.load(r_file)

        formatted_table = json2html.convert(json = input)

        your_file = codecs.open("results.html", "w", encoding='utf-8', errors='ignore')
        your_file.write(formatted_table)
        your_file.close()
        shutil.copy2(r"C:\__CODE__\PYTHON\ROCKONNECT\results.html", r"C:\__CODE__\PYTHON\ROCKONNECT\templates")

             
        return render_template('dashboard.html')
        print("\n", "this is the results: ", formatted_table), 
        print("\n", "this is the type of res_2: ", type(formatted_table))

    except:
        flash("No Data, please try to scrape again","danger")
    
    print("\n", "you are under the dashboard page now")
    return render_template('dashboard.html')



'''

def dashboard():
    try:
        # print(url)
        # print(time)
        res_1 = mycol.find({ "url": url })
        # res_1 = mycol.find({'$and': [{'url': { url }},{'date': time}]})
        # res_1 = mycol.find({"$and": [{"url": url}, {"date": time}]})

        # reading the content from the JSON file
        with open("message.json", "r") as r_file:
            data_processed = json.load(r_file)


        formatted_table = json2html.convert(json = data_processed)
        
        print("\n", "this is the results: ", formatted_table)
        print("\n", "this is the type of table: ", type(formatted_table))
        
        your_file = open("result.html", "w")
        your_file.write(formatted_table)
        your_file.close()

        return render_template('dashboard.html', tasks=res_1)

    except:
        flash("No Data, please try to scrape again","danger")
    
    print("\n", "you are under the dashboard page now")
    return render_template('dashboard.html')





def dashboard():
    try:
        res_1 = mycol.find({ "url": url })
        print("this is the results: ")
        return render_template('dashboard.html',tasks=res_1)
    except:
        flash("No Data, please try to scrape again","danger")
    
    print("you are under the dashboard page now")
    return render_template('dashboard.html')



'''


############## defining the routes for the different web pages END ##############



####################################################################################################
# running app in debug mode so that I can update the app.py without the need of manual restart
if __name__ == "__main__":
    app.secret_key="mrbacco_millenovecentosettantaquattro"
    app.run(debug=True)