from flask import Flask, render_template, request, send_file
from redmine_api import connect_to_redmine, get_issues_by_update, get_issues_by_create
from data_processing import process_issues
from excel_export import export_to_excel
from datetime import datetime, timedelta

app=Flask(__name__)
app.config['TEMPLATES_FOLDER']='templates'

@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/reporter', methods=['GET', 'POST'])
def reporter():
    if request.method == 'POST':
        start_date_updated = request.form['start_date_updated']
        end_date_updated = request.form['end_date_updated']
        start_date_created = request.form['start_date_created']
        end_date_created = request.form['end_date_created']

        updated_start_date = datetime.strptime(start_date_updated, "%Y-%m-%d")
        updated_end_date = datetime.strptime(end_date_updated, "%Y-%m-%d")
        created_start_date = datetime.strptime(start_date_created, "%Y-%m-%d")
        created_end_date = datetime.strptime(end_date_created, "%Y-%m-%d")

        updated_date_range = [updated_start_date, updated_end_date]
        created_date_range = [created_start_date, created_end_date]

        redmine_url = 'https://mesaregistrocivil.cba.gov.ar/redmine/'
        redmine_key = '5d6cec506b5b22ec8930ad02da88ceb8aa8955dc'
        project_id = 1

        redmine = connect_to_redmine(redmine_url, redmine_key)

        issues_updated = get_issues_by_update(redmine, project_id, updated_date_range=updated_date_range)

        issues_created = get_issues_by_create(redmine, project_id, created_date_range=created_date_range)

        df_updated, df_created = process_issues(issues_updated, issues_created)

        excel_file = 'problemas_redmine.xlsx'

        export_to_excel(df_updated, df_created, excel_file)

        return send_file(excel_file, as_attachment=True, download_name='problemas_redmine.xlsx')

    return render_template('reporter.html')

if __name__ == '__main__':
    app.run()