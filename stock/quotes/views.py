from django.shortcuts import render, redirect
from .models import Stock
from .forms import StockForm
from django.contrib import messages

# Browser request for home page, pass in dict
def home(request):
	import requests
	import json

	api_key = "pk_e52fce48c64f424c9c62a572e2e003df"

	if request.method == 'POST':
		ticker = request.POST['ticker']
		# pass in url that calls the api
		# api_request = requests.get("https://cloud.iexapis.com/stable/stock/" + ticker + "/quote?token=</pk_e52fce48c64f424c9c62a572e2e003df>")
		api_request = requests.get(
			f"https://cloud.iexapis.com/stable/stock/{ticker}/quote?token={api_key}")
		# api_request = requests.get("https://cloud.iexapis.com/stable/stock/" + ticker + "</pk_e52fce48c64f424c9c62a572e2e003df>")
		api_request = requests.get(
			f"https://cloud.iexapis.com/stable/stock/{ticker}/quote?token={api_key}")

		try:
			api = json.loads(api_request.content)
		except Exception as e:
			api = "Error..."

		return render(request, 'home.html', {'api': api, 
			'error':"Could not access the api"})
	
	else:
	
		return render(request, 'home.html', {'ticker': "Enter a Ticker Symbol Above..."})



def about(request):
	return render(request, 'about.html', {})


def add_stock(request):
	api_key = "pk_e52fce48c64f424c9c62a572e2e003df"
	import requests
	import json

	if request.method == 'POST':
		form = StockForm(request.POST or None)
	
		if form.is_valid():
			form.save()
			messages.success(request, ("Stock has been added to your portfolio!"))				
			return redirect('add_stock')

	else:	
		ticker = Stock.objects.all()
		# save ticker info from api output into python list ('output list')
		output = []
		# modify to pull multiple stock tickers at the same time
		for ticker_item in ticker:
			# api_request = requests.get("https://cloud.iexapis.com/stable/stock/" + str(
			# 	ticker_item) + "/quote?token=</pk_e52fce48c64f424c9c62a572e2e003df>")
			api_request = requests.get(
				f"https://cloud.iexapis.com/stable/stock/{ticker_item}/quote?token={api_key}")
			try:
				api = json.loads(api_request.content)
				output.append(api)
			except Exception as e:
				api = "Error..."	

		return render(request, 'add_stock.html', {'ticker': ticker, 'output':  output})

def delete(request, stock_id):
	item = Stock.objects.get(pk=stock_id) # call database by primary key for id #
	item.delete()
	messages.success(request, ("Stock Has Been Deleted From Portfolio!"))
	return redirect(add_stock)
	
def news(request):
	import requests
	import json
	
	# News API
	api_request = requests.get(
		'https://newsapi.org/v2/everything?q=bitcoin&apiKey=a33f8a09ec5c4984895d6887146b4358')

	
	# BASIC - Stock News API
	#api_request = requests.get('https://stocknewsapi.com/api/v1/category?section=general&items=50&token=</your_api_key>')
	
	# PREMIUM - Stock News API
	# api_request = requests.get('https://stocknewsapi.com/api/v1/category?section=alltickers&items=50&token=</your_api_key>')
	api = json.loads(api_request.content)
	return render(request, 'news.html', {'api': api}) 
	messages.success(request, ("Stock Has Been Deleted"))
	return redirect(add_stock)





