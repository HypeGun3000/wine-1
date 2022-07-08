from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape

from collections import defaultdict

import argparse
import pandas


def calculate_year_title(winery_age):
    if winery_age[-1] == '0' or 5 <= int(winery_age[-2:]) <= 20:
        title = 'лет'
    elif winery_age[-1] in '234':
        title = 'года'
    elif winery_age[-1] == '1':
        title = 'год'
    return title


def main():
    from datetime import date

    parser = argparse.ArgumentParser(
        description='Какой аргумент нужно указать'
    )

    parser.add_argument('full_file_name', help='Название Excel файла, из которого нужно брать данные')
    args = parser.parse_args()

    date = date.today()
    year_of_winery_creating = 1920
    winery_age = str(date.year - year_of_winery_creating)

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    recycled_excel_file = pandas.read_excel(args.full_file_name)

    wines = recycled_excel_file.to_dict(orient='records')

    groped_wines = defaultdict(list)

    for wine in wines:
        groped_wines[wine['Категория']].append(wine)

    rendered_page = template.render(
        winery_age=winery_age,
        calculate_year_title=calculate_year_title(winery_age),
        groped_wines=groped_wines
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()
