import pandas

excel_file = pandas.read_excel('wine.xlsx')

print(excel_file)
dict_of_all_columns = dict()
for index, col in enumerate(excel_file):
    print(f'{col} :', excel_file[col].tolist())
