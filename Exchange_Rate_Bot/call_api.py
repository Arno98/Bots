import requests

def call_api(url, params=None, headerss=False):
	headers = {
		'x-rapidapi-key': "api_key",
		'x-rapidapi-host': "currency-converter5.p.rapidapi.com"
		}
	if headerss == True:
		response = requests.request("GET", url, headers=headers, params=params)
	else:
		response = requests.request("GET", url)
	return response.json()

