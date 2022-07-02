from http.server import HTTPServer, SimpleHTTPRequestHandler

from jinja2 import Environment, FileSystemLoader, select_autoescape

from datetime import date
from collections import defaultdict

import pandas
env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')

date = date.today()
current_year = int(date.year) - 1920

if str(current_year)[-1] == '0' or 5 <= int(str(current_year)[-2:]) <= 20:
    current_title = 'лет'
elif str(current_year)[-1] in '234':
    current_title = 'года'
elif str(current_year)[-1] == '1':
    current_title = 'год'

excel_file = pandas.read_excel('wine.xlsx')
excel_file2 = pandas.read_excel('wine2.xlsx')
excel_file3 = pandas.read_excel('wine3.xlsx')

types_whole_wines = excel_file.to_dict(orient='records')
types_whole_wines2 = excel_file2.to_dict(orient='records')
types_whole_wines3 = excel_file3.to_dict(orient='records')

new_dict = defaultdict(list)

for wine in types_whole_wines3:
    new_dict[wine['Категория']].append(wine)

rendered_page = template.render(
    current_year=current_year,
    let_god_goda=current_title,
    types_whole_wines=types_whole_wines,
    new_dict=new_dict
)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
