import requests
from bs4 import BeautifulSoup

url = "https://hobbygames.ru/catalog-new?results_per_page=30&sort=date_added&order=DESC&new=1&parameter_type=0&page=1"
headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:99.0) Gecko/20100101 Firefox/99.0"} # my usr agent


def get_page(i):
        tst_url = url[:-1] + str(i)
        page = requests.get(tst_url, headers=headers)
        # print(page)
        return page


def get_prod_table(page):
    soup = BeautifulSoup(page.text, 'html.parser')
    prod_table = []
    it = 1
    products = soup.find(class_='products').find_all(class_="name")
    for prod in products:
        prod_table.append([it, prod.text.strip(), prod['href']])
        it += 1
        # print(prod_table)
    return prod_table


def get_item_info(prod_table, item_id):
    item_id = max(min(item_id, len(prod_table) - 1), 0)
    print(len(prod_table))
    item_page = requests.get(prod_table[item_id][2], headers=headers)
    item_soup = BeautifulSoup(item_page.text, 'html.parser')
    price = item_soup.find(class_='price').text
    description = item_soup.find(class_='desc-text').text.replace('. ', '.\n')
    return price, description


