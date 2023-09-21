from redminelib import Redmine
import urllib3
from datetime import datetime, timedelta

def connect_to_redmine(redmine_url, redmine_key):
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    return Redmine(redmine_url, key=redmine_key, requests={'verify': False})

def get_issues(redmine, project_id, start_date_updated=None, end_date_updated=None, start_date_created=None, end_date_created=None):
    filters = {'project_id': project_id, 'status_id': 5}

    if start_date_updated and end_date_updated:
        filters['updated_on'] = '><{}|{}'.format(start_date_updated.strftime('%Y-%m-%d'), end_date_updated.strftime('%Y-%m-%d'))

    if start_date_created and end_date_created:
        filters['created_on'] = '><{}|{}'.format(start_date_created.strftime('%Y-%m-%d'), end_date_created.strftime('%Y-%m-%d'))

    redmine_url = 'https://mesaregistrocivil.cba.gov.ar/redmine/'
    redmine_key = '5d6cec506b5b22ec8930ad02da88ceb8aa8955dc'
    project_id = 1

    redmine = connect_to_redmine(redmine_url, redmine_key)

    start_date_updated = datetime(2023, 8, 1)
    end_date_updated = datetime(2023, 9, 1)
    start_date_created = datetime(2023, 8, 1)
    end_date_created = datetime(2023, 9, 1)

    issues = get_issues(redmine, project_id, start_date_updated, end_date_updated, start_date_created, end_date_created)

    return redmine.issue.filter(**filters)