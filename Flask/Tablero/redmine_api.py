from redminelib import Redmine
import urllib3

def connect_to_redmine(redmine_url, redmine_key):
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    return Redmine(redmine_url, key=redmine_key, requests={'verify': False})

redmine_url = 'https://mesaregistrocivil.cba.gov.ar/redmine/'
redmine_key = '5d6cec506b5b22ec8930ad02da88ceb8aa8955dc'

redmine = connect_to_redmine(redmine_url, redmine_key)

def get_issues_by_create(redmine, created_date_range):
    filters = {'status_id': 5}
    if created_date_range:
        created_start_date, created_end_date = created_date_range
        filters['created_on'] = f'><{created_start_date}|{created_end_date}'
    return redmine.issue.filter(**filters)

def get_issues_by_update(redmine, updated_date_range):
    filters = {'status_id': 5}
    if updated_date_range:
        updated_start_date, updated_end_date = updated_date_range
        filters['updated_on'] = f'><{updated_start_date}|{updated_end_date}'
    return redmine.issue.filter(**filters)

author_ids_list = []
author_ids_name = []
group_names = ["T1 Mesa de ayuda Oficinas de RC", "T1.5 - Analistas - MDA RC", "T2 Soporte RCD/SiSol/MiRC"]

def get_author(redmine, group_name, author_ids_list=author_ids_list, author_ids_name=author_ids_name):
    group = None
    for g in redmine.group.all():
        if g.name == group_name:
            group = g
            break

    if group:
        members = group.users
        author_ids = [member.id for member in members]
        author_names = [member.name for member in members]

        author_ids_list.extend(author_ids)
        author_ids_name.extend(author_names)

for group_name in group_names:
    get_author(redmine, group_name)

author_data = zip(author_ids_list, author_ids_name)