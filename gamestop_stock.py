import matplotlib.pyplot as plt
import pandas as pd
from bs4 import BeautifulSoup
import requests as rq
from sqlite3.dbapi2 import Date
import yfinance as yf

GameStop = yf.Ticker("GME")
gme_data = GameStop.history(period = "max")
gme_data.reset_index(inplace=True)


def make_graph(stock_data, revenue_data, stock):
    stock_data_specific = stock_data[stock_data.Date <= '2021-06-14']
    revenue_data_specific = revenue_data[revenue_data.Date <= '2021-04-30']

    fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

    axes[0].plot(pd.to_datetime(stock_data_specific.Date), stock_data_specific.Close.astype("float"), label="Share Price", color="blue")
    axes[0].set_ylabel("Price ($US)")
    axes[0].set_title(f"{stock} - Historical Share Price")

    axes[1].plot(pd.to_datetime(revenue_data_specific.Date), revenue_data_specific.Revenue.astype("float"), label="Revenue", color="green")
    axes[1].set_ylabel("Revenue ($US Millions)")
    axes[1].set_xlabel("Date")
    axes[1].set_title(f"{stock} - Historical Revenue")

    plt.tight_layout()
    plt.show()

url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html"
html_data = rq.get(url)
html_data2 = html_data.text
soup = BeautifulSoup(html_data2, "html.parser")
table = soup.find("table")
rows = []
for tr in table.find_all("tr")[1:]:
    cols = [td.get_text(strip=True) for td in tr.find_all("td")]
    rows.append(cols)
gme_revenue = pd.DataFrame(rows, columns=["Date", "Revenue"])
gme_revenue["Revenue"] = (
    gme_revenue["Revenue"]
    .str.replace("$", "", regex=False)
    .str.replace(",", "", regex=False)
)
gme_revenue = gme_revenue.dropna(subset=["Revenue"])
gme_revenue["Revenue"] = pd.to_numeric(gme_revenue["Revenue"], errors="coerce")
gme_revenue.dropna(inplace=True)
gme_revenue = gme_revenue[gme_revenue['Revenue'] != ""]
make_graph(gme_data, gme_revenue, 'GME')


