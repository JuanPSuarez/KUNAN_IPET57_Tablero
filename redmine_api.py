from redminelib import Redmine
import urllib3


def connect_to_redmine(redmine_url, redmine_key):
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    return Redmine(redmine_url, key=redmine_key, requests={'verify': False})


def get_issues(redmine, project_id, updated_date_range):
    filters = {'project_id': project_id, 
               'status_id': 5,
               'updated_on':f'><{updated_date_range[0]}|{updated_date_range[1]}'}
    
    #print('Filtrado 1')
    
    return redmine.issue.filter(**filters)

def get_issues2(redmine, project_id, created_range):
    filters = {'project_id': project_id, 
               'status_id': 5, 
               'created_on': f'><{created_range[0]}|{created_range[1]}'}

    #print('Filtrado 2')

    return redmine.issue.filter(**filters)