from redminelib import Redmine
import urllib3
import pandas as pd
import os

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

redmine_url = 'https://mesaregistrocivil.cba.gov.ar/redmine/'
redmine_key = '5d6cec506b5b22ec8930ad02da88ceb8aa8955dc'
redmine_params = {'verify': False}

redmine = Redmine(redmine_url, key=redmine_key, requests=redmine_params)
project = redmine.project.get('tktra-registro-civil-digital')

project_id = 1
issues = redmine.issue.filter(project_id=project_id)

data = []
additional_fields_data = []
custom_fields_dict = {}

for issue in issues:
    custom_fields = issue.custom_fields
    custom_fields_data = {field.name: field.value for field in custom_fields}
    custom_fields_dict[issue.id] = custom_fields_data

    issue_data = {
        'ID': issue.id,
        'Tipo': issue.tracker.name,
        'Author': issue.author.name,
        'Días abierto': (pd.to_datetime(issue.updated_on) - pd.to_datetime(issue.created_on)).days,
        'Oficina': custom_fields_data.get('Oficina', None),
        'Canal de contacto': custom_fields_data.get('Canal de contacto', None),
    }

    data.append(issue_data)

    additional_issue_data = {
        'ID': issue.id,
        'Tipo': issue.tracker.name,
        'Author': issue.author.name,
        'Días abierto': (pd.to_datetime(issue.updated_on) - pd.to_datetime(issue.created_on)).days,
        'Creado': issue.created_on,
        'Actualizado': issue.updated_on,
        'Oficina': custom_fields_data.get('Oficina', None),
        'Canal de contacto': custom_fields_data.get('Canal de contacto', None),
        'Trámite': custom_fields_data.get('Trámite', None),
        'Modulo Rcd': custom_fields_data.get('Modulo Rcd', None),
        'Sistema': custom_fields_data.get('Sistema', None),
        'Modulo Generales y Tramites': custom_fields_data.get('Modulo Generales y Tramites', None),
    }

    additional_fields_data.append(additional_issue_data)

df = pd.DataFrame(data)
additional_df = pd.DataFrame(additional_fields_data)

df = df.sort_values(by='ID')
additional_df = additional_df.sort_values(by='ID')

excel_file = 'problemas_redmine.xlsx'

if os.path.exists(excel_file):
    os.remove(excel_file)

with pd.ExcelWriter(excel_file, engine='xlsxwriter') as writer:
    header_format = writer.book.add_format({'bg_color': '#006400', 'font_color': 'white'})

    df.to_excel(writer, sheet_name='Sis&Mod-Ofi-Res-Rec', index=False)
    worksheet1 = writer.sheets['Sis&Mod-Ofi-Res-Rec']
    for col_num, value in enumerate(df.columns.values):
        worksheet1.write(0, col_num, value, header_format)

    additional_df.to_excel(writer, sheet_name='Operador y Ticket por dia', index=False)
    worksheet2 = writer.sheets['Operador y Ticket por dia']
    for col_num, value in enumerate(additional_df.columns.values):
        worksheet2.write(0, col_num, value, header_format)

os.system('start excel.exe "{}"'.format(excel_file))

print("Problemas y campos adicionales guardados en el archivo Excel 'problemas_redmine.xlsx'.")
