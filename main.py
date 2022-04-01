import requests
from bs4 import BeautifulSoup

def filter_input(link, data_is_empty):
    should_ret = False
    if link == "err" or "skroutz.gr/s/" not in link:
        print('-' * 45)
        print('Error loading requested URL: No URL was given\nor given URL is not a valid skroutz.gr/s/ URL')
        print('-' * 45)
        should_ret = True
    if data_is_empty:
        print('-' * 55)
        print('An error occured while trying to fulfill your request.\nData flag was initialized, but no flags were given.')
        print('-' * 55)
        should_ret = True
    return should_ret

def call(link="err", **kwargs):
    kwarg_dict = dict()
    for key,value in kwargs.items():
        kwarg_dict[key] = value

    data_length = None
    filter_returns = False
    show = False
    if len(kwarg_dict.keys()) > 0:
        if 'data' in kwarg_dict.keys():
            filter_returns = 'all' not in kwarg_dict['data']
            data_length = len(kwarg_dict['data']) == 0 
        if 'show_all' in kwarg_dict.keys():
            show = kwarg_dict['show_all']

    if filter_input(link, data_length):
        return
    
    page = requests.get(link, headers={"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'})
    soup = BeautifulSoup(page.content, 'html.parser')
    
    title = soup.select_one('.page-title').get_text() if not filter_returns or filter_returns and 'product_name' in kwarg_dict['data'] else None
    price = None
    if not show:
        if not filter_returns or filter_returns and 'base_price' in kwarg_dict['data']:
            price = soup.find("strong", {"class": "dominant-price"}).get_text()
            price = price.replace(' ', '')
            price = price.replace('€', '')
            prices = price.split(",")
            price = int(prices[0]) + float(prices[1]) / 100
    else:
        lim = 64 if 'limit' not in kwarg_dict.keys() else kwargs['limit']
        divs = soup.findAll("li", {"class": "js-product-card"}, limit=lim)
        
        prices_no_fees = None
        titles = None
        if not filter_returns or filter_returns and 'store_names' in kwarg_dict['data']:
            titles = []
            for i in range(len(divs)):
                titles.append(divs[i].findChildren("a", {"class": "js-product-link"})[0].get_text())
        
        if not filter_returns or filter_returns and 'base_price' in kwarg_dict['data']:
            prices_no_fees = []
            for i in range(len(divs)):
                to_append = divs[i].findChildren("strong", {"class": "dominant-price"})[0].get_text()
                to_append = to_append[:len(to_append)-2].split(",")
                euros = float(to_append[0])
                cents = int(to_append[1])
                final = euros + cents / 100
                prices_no_fees.append(final)

    rating_count = None
    if not filter_returns or filter_returns and 'rating_count' in kwarg_dict['data']:
        rating_count = soup.find("div", {"class": "actual-rating"}).get_text()
    
    rating_score = None
    if not filter_returns or filter_returns and 'rating_score' in kwarg_dict['data']:
        rating_score_scrape = soup.find("a", {"class": ["rating", "big_stars"]})['title'][0:3].split(",") # Future to-do: make this work with child properties for fuck's shake.
        rating_score = int(rating_score_scrape[0]) + int(rating_score_scrape[1]) / 100

    discussion_count = None
    if not filter_returns or filter_returns and 'discussion_count' in kwarg_dict['data']:
        discussion_count = soup.find("a", {"href": "#qna"}).find("span").get_text()
        discussion_count = discussion_count.replace('(', '')
        discussion_count = discussion_count.replace(')', '')

    is_on_sale = None
    if not filter_returns or filter_returns and 'is_on_sale' in kwarg_dict['data']:
        sale_badge = soup.find("span", {"class": ["badge", "pricedrop"]})
        is_on_sale = sale_badge is not None

    store_count = None
    if not filter_returns or filter_returns and 'store_count' in kwarg_dict['data']:
        store_count = soup.find("a", {"href": "#shops"}).findChildren("span")[0].get_text()
        store_count = store_count.replace('(', '')
        store_count = store_count.replace(')', '')

    lowest_base_price = max_base_price = None
    if not filter_returns or filter_returns and 'lowest_price' in kwarg_dict['data']:
        if price is None:
            price = soup.find("strong", {"class": "dominant-price"}).get_text()
            price = price.replace(' ', '')
            price = price.replace('€', '')
            prices = price.split(",")
            price = int(prices[0]) + float(prices[1]) / 100
        lowest_base_price = price
    if not filter_returns or filter_returns and 'max_price' in kwarg_dict['data']:
        if not show:
            price = soup.find("strong", {"class": "dominant-price"}).get_text()
            price = price.replace(' ', '')
            price = price.replace('€', '')
            prices = price.split(",")
            price = int(prices[0]) + float(prices[1]) / 100
            max_base_price = price
        else:
            prices_no_fees = []
            for i in range(len(divs)):
                to_append = divs[i].findChildren("strong", {"class": "dominant-price"})[0].get_text()
                to_append = to_append[:len(to_append)-2].split(",")
                euros = float(to_append[0])
                cents = int(to_append[1])
                final = euros + cents / 100
                prices_no_fees.append(final)
            max_base_price = prices_no_fees[-1]
        
    return_dict = {
        "product_name": title,
        "base_price": price if not show else prices_no_fees, #returns a list of all base prices of product from all stores if show_all is True, else returns first price found (cheapest)
        "store_names": titles if show else None, #returns only if show_all is True
        "store_count": int(store_count) if store_count is not None else None,
        "rating_count": int(rating_count) if rating_count is not None else None,
        "rating_score": rating_score,
        "discussion_count": int(discussion_count) if discussion_count is not None else None,
        "lowest_price": lowest_base_price,
        "max_price": max_base_price,
        "is_on_sale": is_on_sale
    }
    return return_dict
