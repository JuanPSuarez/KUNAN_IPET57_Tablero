from redminelib import Redmine
import urllib3


def connect_to_redmine(redmine_url, redmine_key):
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    return Redmine(redmine_url, key=redmine_key, requests={'verify': False})

def get_issues_by_create(redmine, project_id, created_date_range):
    filters = {'project_id': project_id, 'status_id': 5}
    if created_date_range:
        created_start_date, created_end_date = created_date_range
        filters['created_on'] = f'><{created_start_date}|{created_end_date}'
    return redmine.issue.filter(**filters)

def get_issues_by_update(redmine, project_id, updated_date_range):
    filters = {'project_id': project_id, 'status_id': 5}
    if updated_date_range:
        updated_start_date, updated_end_date = updated_date_range
        filters['updated_on'] = f'><{updated_start_date}|{updated_end_date}'
    return redmine.issue.filter(**filters)
