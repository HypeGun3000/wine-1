def year_title(year_from_creation):
    if year_from_creation[-1] == '0' or 5 <= int(year_from_creation[-2:]) <= 20:
        current_title = 'лет'
    elif year_from_creation[-1] in '234':
        current_title = 'года'
    elif year_from_creation[-1] == '1':
        current_title = 'год'
    return current_title


def main():
    from http.server import HTTPServer, SimpleHTTPRequestHandler
    from jinja2 import Environment, FileSystemLoader, select_autoescape

    from collections import defaultdict
    from datetime import date

    import pandas

    date = date.today()
    year_of_wine_creating = 1920
    year_from_creation = str(date.year - year_of_wine_creating)

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    recycled_excel_file = pandas.read_excel('wine3.xlsx')

    whole_wines = recycled_excel_file.to_dict(orient='records')

    formated_wines = defaultdict(list)

    for wine in whole_wines:
        formated_wines[wine['Категория']].append(wine)

    rendered_page = template.render(
        year_from_creation=year_from_creation,
        year_word_format=year_title(year_from_creation),
        formated_wines=formated_wines
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()

if __name__ == '__main__':
    main()