from flask import Flask, render_template, request, send_file
from redmine_api import get_issues_by_update, get_issues_by_create, redmine, author_data, author_ids_list
from data_processing import process_issues
from excel_export import export_to_excel
from datetime import datetime

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

        updated_start_date = datetime.strptime(start_date_updated, "%Y-%m-%d").replace(hour=0, minute=0, second=0).strftime("%Y-%m-%dT%H:%M:%SZ")
        updated_end_date = datetime.strptime(end_date_updated, "%Y-%m-%d").replace(hour=23, minute=0, second=0).strftime("%Y-%m-%dT%H:%M:%SZ")
        created_start_date = datetime.strptime(start_date_created, "%Y-%m-%d").replace(hour=0, minute=0, second=0).strftime("%Y-%m-%dT%H:%M:%SZ")
        created_end_date = datetime.strptime(end_date_created, "%Y-%m-%d").replace(hour=23, minute=0, second=0).strftime("%Y-%m-%dT%H:%M:%SZ")

        updated_date_range = [updated_start_date, updated_end_date]
        created_date_range = [created_start_date, created_end_date]

        issues_updated = get_issues_by_update(redmine, updated_date_range=updated_date_range)

        issues_created = get_issues_by_create(redmine, created_date_range=created_date_range)

        selected_operators = request.form.getlist('selected_operators[]')

        selected_author_ids_list = [author_id for author_id in author_ids_list if author_id in selected_operators]

        df_updated, df_created = process_issues(issues_updated, issues_created, selected_author_ids_list)

        excel_file = 'problemas_redmine.xlsx'

        export_to_excel(df_updated, df_created, excel_file)

        return send_file(excel_file, as_attachment=True, download_name='problemas_redmine.xlsx')

    return render_template('reporter.html', author_data=author_data)

if __name__ == '__main__':
    app.run()
