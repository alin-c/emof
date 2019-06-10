import requests, re, sys

#check the input and continue only if it is valid
while True:
	issue = input("Scrie numărul și anul Monitorului Oficial (număr/an): ")
	pattern = r'([\d bis]*?)/(\d{4})'
	result = re.match(pattern, issue, re.IGNORECASE)
	if result == None: #test a regex pattern [\dbis]*?/\d{4}
		print("Numărul sau anul nu sunt scrise corect. Mai încearcă o dată.")
		continue
	else:
		#if the issue is valid separate number from year and return the two values
		#check if bis is present
		number = result.groups()[0].replace(' ', '').lower()
		if number.find('bis') >= 0:
			number = number.replace('b', 'B').zfill(7)
		else:
			number = number.zfill(4)
		year = result.groups()[1]
		break

url = 'http://www.monitoruloficial.ro/emonitornew/services/view.php'
user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
referer = 'http://www.monitoruloficial.ro/emonitornew/emonviewmof.php'
			
headers = {'User-Agent': user_agent,
			'Referer': referer,
			'X-Requested-With': 'XMLHttpRequest'}
			
params = {'doc': '01' + year + number,
			'format': 'jpg',
			'page': '1' }
			
session = requests.Session()

for i in range(1, 1000):
	params['page'] = str(i)
	response = session.get(url, headers = headers, params = params)
	if str(response.content).find('Error') >= 0:
		break
	file_location = 'C:/Users/Alin/Desktop/'
	file_name = file_location + number + '-' + params['page'] + '.jpg'
	with open(file_name, 'wb') as fd:
		for chunk in response.iter_content(chunk_size=128):
			fd.write(chunk)
	print(str(i), end=' ')
	sys.stdout.flush()
print('Gata!')