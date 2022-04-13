import requests
from bs4 import BeautifulSoup

url = "https://hobbygames.ru/catalog-new?results_per_page=30&sort=date_added&order=DESC&new=1&parameter_type=0&page=1"

#headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}
headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:99.0) Gecko/20100101 Firefox/99.0"} # my usr agent

status_code = 404
page = None
soup = None
users_page_num = 0

print('HobbyGames -> catalog-new')
print("Print number of page\n")
while(status_code != 200):
    users_page_num = input()
    try:
        int(users_page_num)
        tst_url = url[:-1] + users_page_num
        page = requests.get(tst_url, headers=headers)
        status_code = page.status_code
        if (status_code != 200):
            print('[WARNING] this page does not exist, try another number!\n')
    except ValueError:
        print("[WARNING] This is not a number! Try again.")

print('[OK] This page exists!\n')
soup = BeautifulSoup(page.text, 'html.parser')
page_num = soup.find(class_='current selected').a.text
if(int(users_page_num) <= 0 or int(users_page_num) > int(page_num)):
    print('[WARNING] Written number is out of bounds! ' + 'page ' + page_num + ' is shown.\n')

prod_table = []
it = 1
products = soup.find(class_='products').find_all(class_="name")
for prod in products:
    prod_table.append([it, prod.text.strip(), prod['href']])
    it += 1

for i in prod_table:
    print(i[0], end=' ')
    print(i[1], end='\n')
ch = ''
while(ch != 'n' and ch != 'N'):
    print("want to check item price and description? [Y/n]\n")
    while (ch != 'y' and ch != 'Y' and ch != 'n' and ch != 'N'):
        ch = input()

    if(ch == 'Y' or ch == 'y'):
        print("Print item's id here: ")
        item_id = -1
        while (item_id == -1):
            try:
                item_id = int(input())
                if (item_id < 0 or item_id > prod_table[-1][0]):
                    print("[WARNING] This number is out of bounds! Please try again.")
                    item_id = -1
            except ValueError:
                print("[WARNING] It's not a number! Try again.")
        item_page = requests.get(prod_table[item_id][2], headers=headers)
        item_soup = BeautifulSoup(item_page.text, 'html.parser')
        price = item_soup.find(class_='price').text
        description = item_soup.find(class_='desc-text').text.replace('. ', '.\n')
        print(price, end='\n')
        print(description, end='\n\n')

print("Thank you for using this app! Good bye!")




