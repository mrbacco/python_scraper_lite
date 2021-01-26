# -*- coding: utf-8 -*-
"""
Created on Mon Jan  4 2021

@author: mrbacco 2021
"""

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
