from tda import auth, client
import config
import time
import datetime
# authenticate


def run():
    try:
        c = auth.client_from_token_file(config.token_path, config.api_key)
    except FileNotFoundError:
        from selenium import webdriver
        with webdriver.Chrome(executable_path=config.chromedriver_path) as driver:
            c = auth.client_from_login_flow(
                driver, config.api_key, config.redirect_uri, config.token_path)

    # tickersearch = 'amc'.upper()
    # response = c.get_quote(tickersearch).json().get(tickersearch)
    # print(response)
    # response = c.get_hours_for_single_market(c.Markets('EQUITY'), datetime.date.today()).json()
    AvailableFunds = c.get_account(config.account_id, fields=None).json()
    Watchlsit = c.get_watchlists_for_single_account(config.account_id).json()
    # for a in AvailableFunds:
    #     print(a)
        # .get('securitiesAccount').get('projectedBalances').get('cashAvailableForTrading')
        # .get('cashAvailableForTrading').get('cashAvailableForTrading')

    ListToGet = 'Weekly'
    Tickerlist = []
    for x in Watchlsit:
        if x.get('name') == ListToGet:
            watchlist = x.get('watchlistItems')
            for stocks in watchlist:
                Tickerlist.append(stocks.get('instrument').get('symbol'))
    for tickers in Tickerlist:
        open = c.get_quote(tickers).json().get(tickers).get('openPrice')
        current = c.get_quote(tickers).json().get(tickers).get('lastPrice')
        percentchange = str(round((1-(float(open)/float(current)))*100,2))
        if float(percentchange) > 0:
            color = (0,255,0)
        else:
            color = (255,0,0)
        text = '| '+tickers +' $ '+str(current)+' '+percentchange +'%'
        print(text)

if __name__ == '__main__':
    run()
