#!/usr/bin/env python
import webapp2
import jinja2
import logging
import os
import urllib2
from bs4 import BeautifulSoup
import lxml
import html5lib
import re

jinja_environment = jinja2.Environment(loader=
    jinja2.FileSystemLoader(os.path.dirname(__file__)))

class MainHandler(webapp2.RequestHandler):
    def get(self):

    	#ERDMAN
        #The page
        erdpage = urllib2.urlopen('http://www.brynmawr.edu/dining/ErdmanWebMenu.html').read()
        erdsoup = BeautifulSoup(erdpage)

        #Dates!
        erddates = erdsoup.find_all('h3')
        #Dates: remove tags
        for date in erddates:
        	erddates[erddates.index(date)] = str(date).replace("<h3>","").replace("</h3>","")

        #Meal names!
        erdmeals = erdsoup.find_all('th')
        #Meal names: remove tags
        for meal in erdmeals:
        	erdmeals[erdmeals.index(meal)] = str(meal).replace("<th scope=\"row\">","").replace("</th>","").replace(" ","").replace("\n","").replace("\xc2\xa0","").replace("<p>","").replace("</p>","")
        erdtemp = []
        erdhold = []
        for meal in erdmeals:
        	erdhold.append(meal)
        	if "Dinner" in meal:
        		erdtemp.append(erdhold)
        		erdhold = []
        del erdmeals[:]
        erdmeals = erdtemp
        #Menus!
        erdmenus = erdsoup.find_all('td')
        #Menus: take away the tags
        for menu in erdmenus:
        	erdmenus[erdmenus.index(menu)] = str(menu).replace("<br/>",",").replace("<td>","").replace("</td>","").replace("<h6>","").replace("\n","").replace("\t","").replace("<p>","").replace("</p>","")
        	#insert spaces
        #Menus: make it a list
        for menu in erdmenus:
        	erdmenus[erdmenus.index(menu)] = menu.split(",")

        #HAFFNER
        #The page
        hafpage = urllib2.urlopen('http://www.brynmawr.edu/dining/HaffnerWebMenu.html').read()
        hafsoup = BeautifulSoup(hafpage)

        #Dates!
        hafdates = hafsoup.find_all('h3')
        #Dates: remove tags
        for date in hafdates:
        	hafdates[hafdates.index(date)] = str(date).replace("<h3>","").replace("</h3>","")

        #Meal names!
        hafmeals = hafsoup.find_all('th')
        #Meal names: remove tags
        for meal in hafmeals:
        	hafmeals[hafmeals.index(meal)] = str(meal).replace("<th scope=\"row\">","").replace("</th>","").replace(" ","").replace("\xc2\xa0","")
        haftemp = []
        hafhold = []
        for meal in hafmeals:
        	hafhold.append(meal)
        	if "Dinner" in meal:
        		haftemp.append(hafhold)
        		hafhold = []
        del hafmeals[:]
        hafmeals = haftemp
        #Menus!
        hafmenus = hafsoup.find_all('td')
        #Menus: take away the tags
        for menu in hafmenus:
        	hafmenus[hafmenus.index(menu)] = str(menu).replace("<br/>",",").replace("<td>","").replace("</td>","").replace("<h6>","").replace("\n","").replace("\t","").replace("<p>","").replace("</p>","").replace("\xc2\xa0","").replace("\xe2\x80\x99","")
        	#insert spaces
        #Menus: make it a list
        for menu in hafmenus:
        	hafmenus[hafmenus.index(menu)] = menu.split(",")

        template_values = {
        "erddates": erddates,
        "erdmeals": erdmeals,
        "erdmenus": erdmenus,

        "hafdates": hafdates,
        "hafmeals": hafmeals,
        "hafmenus": hafmenus,
        }

        template = jinja_environment.get_template('views/index.html')
        self.response.out.write(template.render(template_values))

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
