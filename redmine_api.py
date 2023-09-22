from redminelib import Redmine
import urllib3
from datetime import datetime


def connect_to_redmine(redmine_url, redmine_key):
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    return Redmine(redmine_url, key=redmine_key, requests={'verify': False})


def get_issues(redmine, project_id, author_ids=None, updated_date_range=None):
    filters = {'project_id': project_id, 'status_id': 5}

    if author_ids:
        filters['author_id'] = author_ids

    if updated_date_range:
        updated_start_date, updated_end_date = updated_date_range
        filters['updated_on'] = f'><{updated_start_date}|{updated_end_date}'

    return redmine.issue.filter(**filters)