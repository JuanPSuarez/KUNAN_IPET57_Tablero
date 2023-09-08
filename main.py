from redmine_api import connect_to_redmine, get_issues
from data_processing import process_issues
from excel_export import export_to_excel
import pandas as pd
import os

redmine_url = 'https://mesaregistrocivil.cba.gov.ar/redmine/'
redmine_key = '5d6cec506b5b22ec8930ad02da88ceb8aa8955dc'
project_id = 1

redmine = connect_to_redmine(redmine_url, redmine_key)

issues = get_issues(redmine, project_id)

author_ids_to_filter = [117, 69, 143, 131, 113, 46, 145, 54, 135]

updated_date_range = [pd.to_datetime('2023-01-01'), pd.to_datetime('2023-12-31')]

created_date_range = [pd.to_datetime('2023-01-01'), pd.to_datetime('2023-12-31')]

df, additional_df = process_issues(issues, author_ids=author_ids_to_filter, updated_date_range=updated_date_range,
                                   created_date_range=created_date_range)

excel_file = 'problemas_redmine.xlsx'

export_to_excel(df, additional_df, excel_file)

os.system('start excel.exe "{}"'.format(excel_file))
