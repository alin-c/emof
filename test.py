import requests, re, datetime

number = ''
year = ''
initial_year = 2017
current_year = datetime.datetime.now().year


file_location = 'C:/Users/Alin/Desktop/'

#check the input and continue only if it is valid
def issueInput():
	global number
	global year
	issue = input("Scrie numărul și anul Monitorului Oficial (număr/an): ")
	pattern = r'([\dbis]*?)/(\d{4})'
	result = re.match(pattern, issue)
	while (result == None): # or initial_year < int(year) > current_year): #test a regex pattern [\dbis]*?/\d{4}
		print("Numărul sau anul nu sunt scrise corect. Mai încearcă o dată.")
		number = ''
		year = ''
		issueInput()
	#if the issue is valid separate number from year and return the two values as a list [number, year]
	number = result.groups()[0].zfill(4)
	year = result.groups()[1]
	return [number, year]

issue = issueInput()
url = 'http://www.monitoruloficial.ro/emonitornew/services/view.php'
user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
referer = 'http://www.monitoruloficial.ro/emonitornew/emonviewmof.php?fid=MS43OTE4MjUwMTU5ODI2RSszMA=='
			
headers = {'User-Agent': user_agent,
			'Referer': referer,
			'Accept': 'application/json, text/javascript, */*; q=0.01',
			'Accept-Language': 'en-US,en;q=0.5',
			'X-Requested-With': 'XMLHttpRequest'}
			
params = {'doc': '01' + year + number,
			'format': 'json', #'jpg',
			'page': '1' }
			
session = requests.Session()
response = session.get(referer, headers = headers, params = params)
print(response.cookies)
response = session.get(url, headers = headers, params = params, cookies = response.cookies)
result = ''
#print('content: ' + response.raw.json())
for chunk in response.iter_content(chunk_size=128):
	result += chunk
print(result)

"""for i in range(1,2000):
	params['page'] = str(i)
	response = session.get(url, headers = headers, params = params)
	if (str(response).startswith('Error')):
		break
	file_name = file_location + number + '-' + params['page'] + '.jpg'
	with open(file_name, 'wb') as fd:
		for chunk in response.iter_content(chunk_size=128):
			fd.write(chunk)
"""
print('Done!')
