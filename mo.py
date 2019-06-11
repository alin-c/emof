"""
mo.py
0.0.3
Script for saving Monitorul Oficial files as pdf

* prerequisites:
- pip install requests
- pip install fpdf
"""
import requests, re, sys, os
from fpdf import FPDF

pdf = FPDF('P', 'mm', 'A4')
pdf.set_display_mode('real', 'continuous')

file_location = os.environ['temp'] + "\\" #%temp% is used in Windows, for other OS this variable needs to be changed
pdf_location = os.environ['userprofile'] + "\\Desktop\\" #for easy finding

#check the input and continue only if it is valid
while True:
	issue = input("Monitorul Oficial ([parte/]număr/an): ").replace(' ', '').lower()
	pattern = r"(?:(\d)/)*?([\dbis ]+?)/(\d{4})$"
	part = '01'
	result = re.match(pattern, issue, re.IGNORECASE)
	if result == None: #test a regex pattern [\dbis]*?/\d{4}
		print("\nNumărul sau anul nu sunt scrise corect. Mai încearcă o dată.")
		continue
	else:
		#if the part is specified, use it, else consider it to be part 01
		#part numbers above 1 are mapped in fact to index + 1
		#Hungarian language version of part 01 is mapped to 02 - currently not supported
		if result.groups()[0] != None:
			index = result.groups()[0].replace("/", "")
			if int(index) > 1: 
				index = str(int(index) + 1)
			part = "0" + index
		#if the issue is valid separate number from year and return the two values
		number = result.groups()[1] #remove spaces and make the string lowercase
		if number.find('bis') >= 0: #check if bis is present
			number = number.replace('b', 'B').zfill(7)
		else:
			number = number.zfill(4)
		year = result.groups()[2]
		break

#prepare and make the HTTP request to retrieve the images
url = 'http://www.monitoruloficial.ro/emonitornew/services/view.php'
user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
referer = 'http://www.monitoruloficial.ro/emonitornew/emonviewmof.php'
headers = {'User-Agent': user_agent,
			'Referer': referer,
			'X-Requested-With': 'XMLHttpRequest'}
params = {'doc': part + year + number,
			'format': 'jpg',
			'page': '1'}
session = requests.Session()
file_list = []

print("\nSe încearcă descărcarea imaginilor.\n")
for i in range(1, 2500): #2500 is arbitrary, but probably wouldn't be reached in realistic scenarios
	params['page'] = str(i)
	response = session.get(url, headers = headers, params = params)
	
	if str(response.content).find('Error') >= 0: #exit the loop if 'error' is detected in the response
		break
	
	file_name = file_location + number + '-' + params['page'] + '.jpg'
	with open(file_name, 'wb') as fd:
		for chunk in response.iter_content(chunk_size=128):
			fd.write(chunk)
	print(str(i), end=' ') #display some progress
	sys.stdout.flush()
	file_list.append(file_name) #add image location to the list

#iterate through the list of downloaded images and generate a pdf
def make_pdf(image_list):
	print("\nSe generează PDF din imaginile descărcate.")
	for image in image_list:
		pdf.add_page()
		pdf.image(image, 0, 0, 210, 297)
	pdf.output(pdf_location + number + ".pdf", "F")

#iterate through the list of downloaded images and delete them
def cleanup(image_list):
	print("\nSunt șterse imaginile descărcate.")
	for image in image_list:
		if os.path.exists(image):
			os.remove(image)
		else:
			print("\nNu există imaginea de la adresa: " + image)

#do the document generation and then cleanup
make_pdf(file_list)
cleanup(file_list)

print('\nGata! Documentul este salvat aici: ' + pdf_location + number + ".pdf")
os.system("pause")