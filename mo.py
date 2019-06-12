manifest = """mo.py
0.0.5
*********************************************************************************************
Script pentru generarea de documente .pdf pe baza imaginilor publicate de M.O.
Documentul .pdf va fi salvat pe Desktop.

Funcționează numai pentru numerele publicate din 06.06.2017 (de la Partea I, nr. 414/2017)
până în prezent.
Nu funcționează pentru Partea I în limba maghiară și nici pentru numere non-standard (ex. 
17c), cu excepția celor cu "bis".

Formatul de input este:
[parte/]număr/an, indicarea părții este opțională doar dacă se caută un număr din Partea I

Exemple de utilizare:
1. 1/414/2017 echivalent cu 414/2017 => Partea I, nr. 414 din 2017
2. 4/2378/2019 => Partea a IV-a, nr. 2378 din 2019
*********************************************************************************************
"""
print(manifest) #comment this line to supress the manifest

import requests, re, sys, os
from fpdf import FPDF

pdf = FPDF('P', 'mm', 'A4')
pdf.set_display_mode('real', 'continuous')

file_location = os.environ['temp'] + "\\" #%temp% is used in Windows, for other OS this variable needs to be changed
pdf_location = os.environ['userprofile'] + "\\Desktop\\" #for easy finding

#the input loop: check the input and continue only if it is valid
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
		#Hungarian language version of part 01 is mapped internally to 02 - currently not supported
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

#prepare the HTTP request to retrieve the images
url = 'http://www.monitoruloficial.ro/emonitornew/services/view.php'
user_agent = 'Mozilla/5.0 (Windows NT 6.2; rv:63.0) Gecko/20100101 Firefox/63.0' #this could be randomized
referer = 'http://www.monitoruloficial.ro/emonitornew/emonviewmof.php'
headers = {'User-Agent': user_agent,
			'Referer': referer,
			'X-Requested-With': 'XMLHttpRequest'}
params = {'doc': part + year + number,
			'format': 'jpg',
			'page': '1'}
session = requests.Session()
file_list = [] #a list containing full paths of downloaded files; later used for .pdf generation and then cleanup

#the HTTP request loop, using given criteria
print("\nSe încearcă descărcarea imaginilor.\n")
for i in range(1, 2500): #2500 is arbitrary, but probably wouldn't be reached in realistic scenarios
	params['page'] = str(i)
	response = session.get(url, headers = headers, params = params)
	
	if str(response.content).find('Error') >= 0: #exit the loop if 'Error' is detected in the response
		break
	
	file_name = file_location + number + '-' + params['page'] + '.jpg'
	with open(file_name, 'wb') as fd:
		for chunk in response.iter_content(chunk_size=128):
			fd.write(chunk)
	print(str(i), end=' ') #display the progress
	sys.stdout.flush()
	file_list.append(file_name) #add image location to the list

#iterate through the list of downloaded images and generate a .pdf
def make_pdf(image_list):
	if (not image_list):
		print("\nNu s-a găsit niciun document!")
		return 0
	print("\nSe generează PDF din imaginile descărcate.")
	for image in image_list:
		pdf.add_page()
		pdf.image(image, 0, 0, 210, 297)
	pdf.output(pdf_location + number + ".pdf", "F")

#iterate through the list of downloaded images and delete them
def cleanup(image_list):
	if (not image_list):
		return 0
	print("\nSunt șterse imaginile descărcate.")
	for image in image_list:
		if os.path.exists(image):
			os.remove(image)
		else:
			print("\nNu există imaginea de la adresa: " + image)

#do the document generation and then cleanup, but only if there were images found
if make_pdf(file_list) != 0:
	cleanup(file_list)
	print('\nGata! Documentul este salvat aici: ' + pdf_location + number + ".pdf")
	
os.system("<nul set /p \"=Apasă orice tastă pentru a ieși din aplicație...\"") #localized pause message
os.system("pause >nul")