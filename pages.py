import parser as pr


local_port = 8800
local_ip = [127, 0, 0, 1]
item_table = []
item_price = None
item_info = ''


style = """
<style type="text/css">
   DIV {
    width: 300px; /* Ширина слоя */
    margin: 7px; /* Значение отступов */
    padding: 10px; /* Поля вокруг текста */
    border: 4px solid black; /* Параметры границы */
    background: #fc0; /* Цвет фона */
   }
  </style>
"""

pages = {
    '/hobby_home':
        f"""
        <!DOCTYPE html>
<html>
  <head>
  <meta charset="utf-8">
    <title>HobbyGames_NewCatalog_Checker</title>
  </head>
  <body>
  <h1 align="center">Welcome to HobbyGames New Catalog! <h2>
  </br>
  
 <form name="test" method="post" action="get_page">
  <p align="center"><b>Put page id here:</b><br>
   <input type="number" size="40" name="num_page">
   <input type="submit" value="View items list">
  </p>
 </form>
 
  </body>
</html>
    """,
    '/default':
        f"""
        <!DOCTYPE html>
<html>
  <head>
  <meta charset="utf-8">
    <title></title>
  </head>
  <body>
  <h1 align="center"> Something went wrong... <h2>



  </body>
</html>
    """
}

left_half = f""" 
<!DOCTYPE html> 
<html>  
<head> <meta charset="utf-8"> 
<title>HobbyGames_NewCatalog_Checker</title>
  </head>
   <body align="center"> """

right_half = """ </body> </html> """

back_to_page_choose_button = """<button onclick="window.location.href = '/hobby_home';">Choose_other_page</button>"""

get_info_button = """<form name="test" method="post" action="get_page">
  <p><b>Put item id here:</b><br>
   <input type="number" size="40" name="item_id">
   <input type="submit" value="View item description and price">
  </p>
 </form>"""

get_back_button = """<input type="button" onclick="history.back();" value="Back"/>"""
def get_page(req: str, method):
    url = req.split(" ")
    print(url)
    print(method)
    if method == "GET":
        url = url[1]
        if(url == "/hobby_home" or url == '/'):
            return pages["/hobby_home"]

    if(method == "POST"):
        if(url[-1].find("num_page=") > 0):
            num = 1
            try:
                num = max(int(url[-1].split('=')[1]), 0)
            except ValueError:
                print("it's not a number\n")
                num = 1
            table = pr.get_prod_table((pr.get_page(num)))
            item_table.clear()
            item_table.extend(table)

            text = ""
            for i in table:
                text += str(i[0]) + " " + str(i[1]) + "<br>"
            ret_text = left_half \
                       + """<p align="left">""" \
                       + text \
                       + "</p>"\
                       + get_info_button \
                       + "<br>" \
                       + back_to_page_choose_button \
                       + right_half


            return ret_text

        elif (url[-1].find("item_id=") > 0):
            id = 1
            try:
                id = min(max(int(url[-1].split("item_id=")[1]), 1), len(item_table))
            except ValueError:
                print("it's not a number\n")
                id = 1
            id -= 1
            item_price, item_info = pr.get_item_info(item_table, id)
            about = item_table[id][1]
            ret_text = left_half + about + "<br>" + item_price + "<br>" + item_info + "<br>" + get_back_button + right_half
            return ret_text

    return pages["/default"]


