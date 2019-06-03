"""
mo.py
0.0.1
Script for saving Monitorul Oficial files as pdf

Steps:
1. get input from user: number/year
2. get json to find number of pages
	GET http://www.monitoruloficial.ro/emonitornew/services/view.php?doc=0120190435&format=json&page=10
	doc=0120190435
	format=json
	page=10
	
	Host: www.monitoruloficial.ro
	User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0
	Accept: application/json, text/javascript, */*; q=0.01
	Accept-Language: en-US,en;q=0.5
	Accept-Encoding: gzip, deflate
	Referer: http://www.monitoruloficial.ro/emonitornew/emonviewmof.php?fid=MS43OTEzNzc4NjUyNTc1RSszMA==
	X-Requested-With: XMLHttpRequest
	DNT: 1
	Connection: keep-alive
	Cookie: PHPSESSID=uh7u2m2cstv1p2a8s5jeqepcb0; cookieconsent_dismissed=yes
	
	response:
	[{"number":1,"pages":16,...}]
	
3. loop to get each image from 1 to total number of pages

	GET http://www.monitoruloficial.ro/emonitornew/services/view.php?doc=0120190435&format=jpg&page=1
	Referer: http://www.monitoruloficial.ro/emonitornew/emonviewmof.php?fid=MS43OTEzNzc4NjUyNTc1RSszMA==
	
	Transfer-Encoding: chunked
	Content-Type: image/jpeg

	
4. combine images into a pdf and save it

Requirements:
1. Python 3.7.2
2. pip install fpdf

"""

import re, os, traceback, urllib.request
from fpdf import FPDF
from PIL import Image

#1. get input from user: number/year

#check the input and continue only if it is valid
def issueInput():
	issue = input("Scrie numărul și anul Monitorului Oficial (număr/an): ")
	if (issue != "a"): #test a regex pattern [\dbis]*?/\d{4}
		issueInput()
	#if the issue is valid separate number from year and return the two values as a list [number, year]
	return [number, year]

issue = issueInput()

#2. get json to find number of pages
#build the URL
#build the query
#run the query with format=json param and return the page count from JSON

#3. get each page from 1 to total number of pages
#run the same query with format=jpg param for each page from 1 to numPages and store the resulting image to a \tmp folder and a list

#4. combine pages into a pdf and save it
#loop through the image list and generate PDF

def makePdf(pdfFileName, listPages, dir = ''):
    if (dir):
        dir += "/"

    cover = Image.open(dir + str(listPages[0]) + ".jpg")
    width, height = cover.size

    pdf = FPDF(unit = "pt", format = [width, height])

    for page in listPages:
        pdf.add_page()
        pdf.image(dir + str(page) + ".jpg", 0, 0)

    pdf.output(dir + pdfFileName + ".pdf", "F")