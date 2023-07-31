from flask import Flask, render_template, flash, redirect, url_for, request
import csv

app = Flask(__name__)
app.secret_key = 'your_secret_key'


def readData(fileName):
    stocks = []
    with open(fileName, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            symbol, marketCap, price, volume = row
            stocks.append((symbol, float(marketCap), float(price), float(volume)))
    return stocks


def filterStocks(stocks, marketCapMin, marketCapMax, priceMin, priceMax, volumeMin, volumeMax):
    filtered = []
    for symbol, marketCap, price, volume in stocks:
        if marketCapMin <= marketCap <= marketCapMax and \
           priceMin <= price <= priceMax and \
           volumeMin <= volume <= volumeMax:
            filtered.append((symbol, marketCap, price, volume))
    return filtered


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/help')
def help():
    return render_template('help.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        marketCapMin = float(request.form['marketCapMin'])
        marketCapMax = float(request.form['marketCapMax'])
        priceMin = float(request.form['priceMin'])
        priceMax = float(request.form['priceMax'])
        volumeMin = float(request.form['volumeMin'])
        volumeMax = float(request.form['volumeMax'])

        fileName = 'stocks.csv'  # Hardcoded CSV file name
        try:
            stocks = readData(fileName)
            filtered = filterStocks(stocks, marketCapMin, marketCapMax,
                                            priceMin, priceMax, volumeMin, volumeMax)

            if len(filtered) == 0:
                flash("No stocks match the given filters.")
            else:
                flash("Stocks that match the given filters:")
                for symbol, marketCap, price, volume in filtered:
                    flash(f"Symbol: {symbol}, Market Cap: {marketCap}, Price: {price}, Volume: {volume}")

            return redirect(url_for('search'))

        except FileNotFoundError:
            flash("Stock file not found.")

    return render_template('search.html', stocks=None)


if __name__ == '__main__':
    app.run(debug=True)
