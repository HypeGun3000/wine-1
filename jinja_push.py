from http.server import HTTPServer, SimpleHTTPRequestHandler

from jinja2 import Environment, FileSystemLoader, select_autoescape

from datetime import date
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

rendered_page = template.render(
    current_year=current_year,
    let_god_goda=current_title
)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
