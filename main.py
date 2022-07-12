from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape

from collections import defaultdict
from datetime import date

import argparse
import pandas
import os


def calculate_year_title(winery_age):
    if winery_age[-1] == '0' or 5 <= int(winery_age[-2:]) <= 20:
        title = 'лет'
    elif winery_age[-1] in '234':
        title = 'года'
    elif winery_age[-1] == '1':
        title = 'год'
    return title


def main():
    parser = argparse.ArgumentParser(
        description='Программа по переносу данных из Excel файла на сайт. Укажите аргументом - файл,'
                    ' из которого нужно брать данные (Полное название файла)'
    )

    parser.add_argument('filepath', help='Путь к Excel файлу, в котором хранятся данные.',
                        nargs='?', default='complete_wine_table.xlsx')
    args = parser.parse_args()

    date_today = date.today()
    year_of_winery_creating = 1920
    winery_age = str(date_today.year - year_of_winery_creating)

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    recycled_excel_file = pandas.read_excel(args.filepath)

    wines = recycled_excel_file.to_dict(orient='records')

    groped_wines = defaultdict(list)

    for wine in wines:
        groped_wines[wine['Категория']].append(wine)

    rendered_page = template.render(
        winery_age=winery_age,
        year_title=calculate_year_title(winery_age),
        groped_wines=groped_wines
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()
