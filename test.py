import requests, re

number = ''
year = ''

#check the input and continue only if it is valid
def issueInput():
	global number
	global year
	issue = input("Scrie numărul și anul Monitorului Oficial (număr/an): ")
	pattern = r'([\dbis]*?)/(\d{4})'
	result = re.match(pattern, issue)
	while (result == None): #test a regex pattern [\dbis]*?/\d{4}
		print("Numărul sau anul nu sunt scrise corect. Mai încearcă o dată.")
		issueInput()
	#if the issue is valid separate number from year and return the two values as a list [number, year]
	number = result.groups()[0].zfill(4)
	year = result.groups()[1]
	return [number, year]

issue = issueInput()
url = 'http://www.monitoruloficial.ro/emonitornew/services/view.php' #doc=0120190435&format=json&page=1
user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
referer = 'http://www.monitoruloficial.ro/emonitornew/emonviewmof.php' #?fid=MS43OTEzNzc4NjUyNTc1RSszMA==
			
headers = {'User-Agent': user_agent,
			'Referer': referer,
			'X-Requested-With': 'XMLHttpRequest'}
			
params = {'doc': '01' + year + number,
			'format': 'jpg',
			'page': '1' }
			
session = requests.Session()

for i in range(1, 5):
	params['page'] = str(i)
	response = session.get(url, headers = headers, params = params)
	file_location = 'C:/Users/Alin/Desktop/'
	file_name = file_location + number + '-' + params['page'] + '.jpg'
	with open(file_name, 'wb') as fd:
		for chunk in response.iter_content(chunk_size=128):
			fd.write(chunk)

print('Done!')