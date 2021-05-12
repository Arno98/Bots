import string
import random
import matplotlib.pyplot as plt

def history_data_chart(response, data_list, command=False):
	dates = []
	hist_rates = []
	for key, val in response['price'].items():
		dates.append(key)
		for v in val.values():
			hist_rates.append(v)
							
	plt.style.use('seaborn')
	fig, ax = plt.subplots()
	ax.plot(dates, hist_rates, alpha=0.7)
	ax.scatter(dates, hist_rates, s=15)
	fig.autofmt_xdate()
	if command == False:
		plt.title(data_list[0] + " / " + data_list[2] + " (за последние 7 дней)", fontsize=15)
	if command == True:
		plt.title(data_list[1] + " / " + data_list[3] + " (за последние 7 дней)", fontsize=15)
	rand_name = ''.join(random.choice(string.ascii_lowercase) for i in range(10))
	plt.savefig(rand_name + ".png")
	
	return rand_name
