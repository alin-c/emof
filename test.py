import requests

file_location = 'C:/Users/Alin/Desktop/'

session = requests.Session()
print(session.cookies.get_dict())
url = 'http://www.monitoruloficial.ro/emonitornew/services/view.php' #?doc=0120190435&format=json&page=1
host = 'www.monitoruloficial.ro'
user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
referer = 'http://www.monitoruloficial.ro/emonitornew/emonviewmof.php' #?fid=MS43OTEzNzc4NjUyNTc1RSszMA==

params = {'doc': '0120190441',
			'format': 'jpg',
			'page': '1' }
			
headers = {'Host': host,
			'User-Agent': user_agent,
			'Referer': referer,
			'X-Requested-With': 'XMLHttpRequest',
			'Accept': 'image/webp,*/*', #'Accept: application/json, text/javascript, */*; q=0.01',
			'Accept-Language': 'en-US,en;q=0.5',
			'Accept-Encoding': 'gzip, deflate',
			'Connection': 'keep-alive'}

response = session.get(url, headers = headers, params = params)
file = open(file_location + str(params['page']) + '.jpg', 'w')
file.write(response.text)
file.close()

'''while response.status_code == 200:
	params['page'] = int(params['page']) + 1
	response = session.get(url, headers = headers, params = params)
	#print(params['page'] + ': ')
	file = open(file_location + str(params['page']) + '.jpg', 'w')
	file.write(response.text)
	file.close()'''
