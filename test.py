import requests

url = 'http://www.monitoruloficial.ro/emonitornew/services/view.php?doc=0120190435&format=json&page=1' #
user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
referer = 'http://www.monitoruloficial.ro/emonitornew/emonviewmof.php?fid=MS43OTEzNzc4NjUyNTc1RSszMA==' #

params = {'doc': '0120190435',
			'format': 'json',
			'page': '1' }
			
headers = {'User-Agent': user_agent,
			'Referer': referer,
			'X-Requested-With': 'XMLHttpRequest',
			'Accept': 'Accept: application/json, text/javascript, */*; q=0.01'}

response = requests.get(url, headers = headers, params = params)
#response = requests.request('GET', url, headers = headers, params = params)

print(response.text)