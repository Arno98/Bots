import requests

def call_api(url, params=None, headerss=False):
	headers = {
		'x-rapidapi-key': "fba481570emsh5cac1f6f37eb44cp1cfc82jsnc77f26030c2d",
		'x-rapidapi-host': "currency-converter5.p.rapidapi.com"
		}
	if headerss == True:
		response = requests.request("GET", url, headers=headers, params=params)
	else:
		response = requests.request("GET", url)
	return response.json()

