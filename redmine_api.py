from redminelib import Redmine
import urllib3


def connect_to_redmine(redmine_url, redmine_key):
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    return Redmine(redmine_url, key=redmine_key, requests={'verify': False})


def get_issues(redmine, project_id):
    return redmine.issue.filter(project_id=project_id)
