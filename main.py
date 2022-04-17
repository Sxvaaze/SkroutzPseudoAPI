import requests
from bs4 import BeautifulSoup

def filter_input(link, data_is_empty, store_data_is_empty):
    should_ret = False
    if link == "err" or "skroutz.gr/s/" not in link and "skroutz.gr/shop/" not in link:
        print('-' * 50)
        print('Error loading requested URL: No URL was given.\nOr given URL is not a valid product or store URL')
        print('-' * 50)
        should_ret = True
    if data_is_empty:
        print('-' * 55)
        print('An error occured while trying to fulfill your request.\nData flag was initialized, but no flags were given.')
        print('-' * 55)
        should_ret = True
    if store_data_is_empty:
        print('-' * 60)
        print('An error occured while trying to fulfill your request.\nStore Data flag was initialized, but no flags were given.')
        print('-' * 60)
        should_ret = True
    return should_ret

def store_handler(url, sdata):
    page = requests.get(url, headers={"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'})
    soup = BeautifulSoup(page.content, 'html.parser')
    if sdata is None:
        show_all = True
    else:
        show_all = 'all' in sdata
    store_name = soup.find("h1", {"class": "page-title"}).findChildren("strong")[0].get_text() if show_all or 'name' in sdata else None
    
    if show_all or 'tags' in sdata:
        tags = soup.find("main", {"class": "shop"}).findChildren("div", {"class": "shop-info"})[0].findChildren("div", {"class": "content"})[0].findChildren("p")[0].get_text().split(",")

        for i in range(len(tags)):
            tags[i] = tags[i].strip()
    else:
        tags = None

    if show_all or 'identifiers' in sdata:
        type_query = soup.find("main", {"class": "shop"}).findChildren("div", {"class": "shop-info"})[0].findChildren("div", {"class": "content"})[0].findChildren("p")[1]
        identifiers = []
        for child in type_query.findChildren("span"):
            identifiers.append(child.get_text().strip("\n").strip())
    else:
        identifiers = None

    if show_all or 'shop_links' in sdata:
        shop_links_quer = soup.find("div", {"class": "shop-links"})
        telephone = shop_links_quer.findChildren("a", {"itemprop": "telephone"})[0].get_text()
        web_quer = shop_links_quer.findChildren("a", {"rel": "nofollow"})
        has_website = web_quer is not None

        if has_website:
            website = web_quer[0]['href']

        skroutz_prod_quer = shop_links_quer.findChildren("a", {"id": "shop-products"})
        has_skroutz_products = skroutz_prod_quer is not None

        if has_skroutz_products:
            skroutz_page = skroutz_prod_quer[0]['href']
    else:
        telephone = has_website = website = has_skroutz_products = skroutz_page = None
    
    if show_all or 'rating_score' in sdata:
        rating_score_quer = soup.find("div", {"class": "rating-average"}).findChildren("b")[0].get_text().replace(" ", "").replace("\n", "")[0:3].split(",")
        rating_score = float(rating_score_quer[0]) + float(rating_score_quer[1]) / 100
    else:
        rating_score = None

    if show_all or 'rating_count' in sdata:
        pos_rating_count = int(soup.find_all("span", {"class": "review_no"})[0].get_text().replace(" ", "").replace("\n", ""))
        neg_rating_count = int(soup.find_all("span", {"class": "review_no"})[1].get_text().replace(" ", "").replace("\n", ""))
        total_rating_count = pos_rating_count + neg_rating_count
    else:
        pos_rating_count = neg_rating_count = total_rating_count = None

    address = soup.find("b", {"itemprop": "address"}).get_text() if show_all or 'address' in sdata else None
    
    if show_all or 'payment_methods' in sdata:
        payment_methods_quer = soup.find("div", {"class": "payment-list"}).findChildren("ul")[0]
        payment_methods = []
        for li in payment_methods_quer.findChildren("li"):
            payment_methods.append(li.get_text().replace(" ", "").replace("\n", ""))
    else:
        payment_methods = None

    gemh_num = soup.find("div", {"id": "suppliers-register"}).findChildren("ul")[0].findChildren("li")[0].get_text().replace(" ", "").replace("\n", "") if show_all or "gemh_num" in sdata else None

    return_dict = {
        'store_name': store_name,
        'tags': tags,
        'identifiers': identifiers,
        'identifier_booleans': {
            'online_only': 'Το κατάστημα λειτουργεί μόνο διαδικτυακά' in identifiers,
            'has_area': 'Το κατάστημα λειτουργεί μόνο διαδικτυακά' not in identifiers,
            'has_physical_store': 'Κατάστημα & Σημείο παραλαβής.' in identifiers,
            'is_verified_reseller': 'Επίσημος μεταπωλητής' in identifiers,
            'has_greca_trustmark': 'GRECA Trustmark' in identifiers
        } if identifiers is not None else {
            'online_only': None,
            'has_area': None,
            'has_physical_store': None,
            'is_verified_reseller': None,
            'has_greca_trustmark': None,
        },
        'rating_count': {
            'total': total_rating_count,
            'positive': pos_rating_count,
            'negative': neg_rating_count,
        },
        'rating_score': rating_score,
        'tel': telephone,
        'has_website': has_website,
        'website_url': None if not has_website else website,
        'has_skroutz_products': has_skroutz_products,
        'skroutz_products_page': None if not has_skroutz_products else skroutz_page,
        'store_address': address, 
        'payment_methods': payment_methods,
        'gemh_number': gemh_num,
    }

    return return_dict

def call(link="err", **kwargs):
    kwarg_dict = dict()
    for key,value in kwargs.items():
        kwarg_dict[key] = value

    # kwarg flag lengths
    data_length = None
    store_data_length = None

    filter_returns = False

    # show = product flags
    # store_data = store flags
    show = False
    store_data = None
    
    if len(kwarg_dict.keys()) > 0:
        if 'data' in kwarg_dict.keys():
            filter_returns = 'all' not in kwarg_dict['data']
            data_length = len(kwarg_dict['data']) == 0 
        if 'store_data' in kwarg_dict.keys():
            store_data = kwarg_dict['store_data']
            store_data_length = len(kwarg_dict['store_data']) == 0
        if 'show_all' in kwarg_dict.keys():
            show = kwarg_dict['show_all']

    if filter_input(link, data_length, store_data_length):
        return

    if "skroutz.gr/shop/" in link:
        return store_handler(link, store_data)
        
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
            price = int(prices[0]) + float(prices[1]) / 10
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
                final = euros + cents / 10
                prices_no_fees.append(final)

    rating_count = None
    if not filter_returns or filter_returns and 'rating_count' in kwarg_dict['data']:
        rating_count = soup.find("div", {"class": "actual-rating"}).get_text()
    
    rating_score = None
    if not filter_returns or filter_returns and 'rating_score' in kwarg_dict['data']:
        rating_score_scrape = soup.find("a", {"class": ["rating", "big_stars"]})['title'][0:3].split(",") # Future to-do: make this work with child properties for fuck's shake.
        rating_score = int(rating_score_scrape[0]) + int(rating_score_scrape[1]) / 10

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
            price = int(prices[0]) + float(prices[1]) / 10
        lowest_base_price = price
    if not filter_returns or filter_returns and 'max_price' in kwarg_dict['data']:
        if not show:
            price = soup.find("strong", {"class": "dominant-price"}).get_text()
            price = price.replace(' ', '')
            price = price.replace('€', '')
            prices = price.split(",")
            price = int(prices[0]) + float(prices[1]) / 10
            max_base_price = price
        else:
            prices_no_fees = []
            for i in range(len(divs)):
                to_append = divs[i].findChildren("strong", {"class": "dominant-price"})[0].get_text()
                to_append = to_append[:len(to_append)-2].split(",")
                euros = float(to_append[0])
                cents = int(to_append[1])
                final = euros + cents / 10
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