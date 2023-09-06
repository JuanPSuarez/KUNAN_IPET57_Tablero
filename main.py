from redminelib import Redmine
import urllib3
import pandas as pd
import os

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

redmine = Redmine('https://mesaregistrocivil.cba.gov.ar/redmine/',
                  key='5d6cec506b5b22ec8930ad02da88ceb8aa8955dc',
                  requests={'verify': False})
project = redmine.project.get('tktra-registro-civil-digital')

project_id = 1
issues = redmine.issue.filter(project_id=project_id)

data = []
for issue in issues:
    custom_fields = issue.custom_fields
    custom_field_data = {}

    for custom_field in custom_fields:
        custom_field_data[custom_field.name] = custom_field.value

    data.append({
        'ID': issue.id,
        'Asunto': issue.subject,
        'Descripción': issue.description,
        'Tracker': issue.tracker.name,
        'Prioridad': issue.priority.name,
        'Estado': issue.status.name,
        'Fecha de inicio': issue.start_date,
        'Fecha de finalización': issue.due_date,
        'Fecha de creación': issue.created_on,
        'Última actualización': issue.updated_on,
        'Estimación de tiempo': issue.estimated_hours,
        **custom_field_data,
    })

df = pd.DataFrame(data)

df = df.sort_values(by='ID')

excel_file = 'problemas_redmine.xlsx'

if os.path.exists(excel_file):
    os.remove(excel_file)

df.to_excel(excel_file, index=False)

print("Problemas ordenados y guardados en el archivo Excel 'problemas_redmine.xlsx'.") 
