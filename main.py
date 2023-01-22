# import requests
# from bs4 import BeautifulSoup
#
# def exchange_rate():
#
#     URL = 'https://www.nbrb.by/statistics/rates/ratesdaily.asp'
#
#     source = requests.get(URL)
#     soup = BeautifulSoup(source.text, 'html.parser')
#     table = soup.find('table')
#     list_info =[]
#
#     for tr in table.findAll('tr'):
#         for td in tr.findAll('td', {'class': 'curAmount'}):
#             if td.text == '1 USD' or td.text == '1 EUR':
#                 list_info.append(tr)
#                 if len(list_info) == 2:
#                     break
#
#     dollar = list_info[0]
#     euro = list_info[1]
#
#     dollar = dollar.find('td', {'class': 'curCours'})
#     dollar = float(dollar.text.strip().replace(',', '.'))
#
#     euro = euro.find('td', {'class': 'curCours'})
#     euro = float(euro.text.strip().replace(',', '.'))
#
#     return {'USD': dollar, 'EUR': euro}
#
#
# print(exchange_rate())




