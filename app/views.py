from django.shortcuts import render, HttpResponse
from .models import Stock
from django.contrib import messages
from .resources import StockResources
from tablib import Dataset
import csv    
from io import StringIO
import matplotlib.pyplot as plt
import io
import urllib, base64
import pandas as pd

# Create your views here.
def upload_file(request):
    if request.method == 'POST':
        # stocks_resources = StockResources()
        dataset = Dataset()
        new_stock = request.FILES["myfile"]

        if not new_stock.name.endswith('csv'):
            messages.info(request, 'wrong format')
            return render(request, 'upload.html')
        
        imported_data = StringIO(new_stock.read().decode('latin-1'))
        csv_reader = csv.reader(imported_data, delimiter=',')
        
        # csv_reader = dataset.load(new_stock.read(), format="csv")
        for data in csv_reader:
            value = Stock(
                data[0],
                data[1],
                data[2],
                data[3],
            )
            value.save()
    return render(request, 'upload.html')

def visualise(request):
    stock_data = Stock.objects.all()

    if not stock_data.exists():
        return render(request, 'visualise.html', {'message': 'No data available to visualize'})

    data = pd.DataFrame(list(stock_data.values()))

    print("Data inspection:")
    print(data.head())
    data['price'] = pd.to_numeric(data['price'], errors='coerce')

    data = data.dropna(subset=['price'])

    # Ensure the data is sorted by date
    data['date'] = pd.to_datetime(data['date'])
    data = data.sort_values(by=['symbol', 'date'])

    first_rows = data.head().to_html(classes='table table-striped')

    stats = data.groupby('symbol').apply(lambda x: pd.Series({
        'Mean': x['price'].mean(),
        'Median': x['price'].median(),
        'Std Dev': x['price'].std()
    })).reset_index()

    stats_html = stats.to_html(classes='table table-bordered')

    plt.figure(figsize=(14, 7))

    for symbol in data['symbol'].unique():
        subset = data[data['symbol'] == symbol]
        plt.plot(subset['date'], subset['price'], label=symbol)

    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title('Stock Prices Over Time')
    plt.legend()
    plt.grid(True)

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = 'data:image/png;base64,' + urllib.parse.quote(string)

    return render(request, 'visualise.html', {
        'data_uri': uri,
        'first_rows': first_rows,
        'stats_html': stats_html
    })
