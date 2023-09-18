import pandas as pd
import numpy as np


def process_issues(issues_updated, issues_author, updated_date_range=None, created_date_range=None):
    data_updated = []
    data_author = []

    for issue in issues_updated:
        custom_fields = issue.custom_fields
        custom_fields_data = {field.name: field.value for field in custom_fields}

        created_on = pd.to_datetime(issue.created_on)
        updated_on = pd.to_datetime(issue.updated_on)

        updated_date_filter_passed = updated_date_range is None or (
                updated_date_range[0] <= updated_on <= updated_date_range[1])

        if updated_date_filter_passed:
            days_open = np.busday_count(created_on.date(), updated_on.date())

            issue_data_updated = {
                'ID': issue.id,
                'Tipo': issue.tracker.name,
                'Author': issue.author.name,
                'Días abierto': days_open,
                'Actualizado': issue.updated_on,
                'Oficina': custom_fields_data.get('Oficina', None),
                'Canal de contacto': custom_fields_data.get('Canal de contacto', None),
                'Sistemas F': issue.custom_fields.get('Sistema') or issue.tracker.name,
                'Modulos F': ', '.join([custom_fields_data.get('Trámite', ''),
                                        custom_fields_data.get('Modulo Rcd', ''),
                                        custom_fields_data.get('Modulo Generales y Tramites', '')]).strip(', ')
            }

            data_updated.append(issue_data_updated)

    for issue in issues_author:
        custom_fields = issue.custom_fields
        custom_fields_data = {field.name: field.value for field in custom_fields}

        created_on = pd.to_datetime(issue.created_on)
        updated_on = pd.to_datetime(issue.updated_on)

        created_date_filter_passed = created_date_range is None or (
                created_date_range[0] <= created_on <= created_date_range[1])

        if created_date_filter_passed:
            days_open = np.busday_count(created_on.date(), updated_on.date())

            additional_issue_data_author = {
                'ID': issue.id,
                'Tipo': issue.tracker.name,
                'Author': issue.author.name,
                'Días abierto': days_open,
                'Creado': issue.created_on,
                'Actualizado': issue.updated_on,
                'Oficina': custom_fields_data.get('Oficina', None),
                'Canal de contacto': custom_fields_data.get('Canal de contacto', None),
                'Trámite': custom_fields_data.get('Trámite', None),
                'Modulo Rcd': custom_fields_data.get('Modulo Rcd', None),
                'Sistema': custom_fields_data.get('Sistema', custom_fields_data.get('Tipo', None)),
                'Modulo Generales y Tramites': custom_fields_data.get('Modulo Generales y Tramites', None),
                'Sistemas F': custom_fields_data.get('Sistema') or issue.tracker.name,
                'Modulos F': ', '.join([custom_fields_data.get('Trámite', ''),
                                        custom_fields_data.get('Modulo Rcd', ''),
                                        custom_fields_data.get('Modulo Generales y Tramites', '')]).strip(', ')
            }

            data_author.append(additional_issue_data_author)

    df_updated = pd.DataFrame(data_updated)
    df_author = pd.DataFrame(data_author)

    df_updated = df_updated.sort_values(by='ID')
    df_author = df_author.sort_values(by='ID')

    return df_updated, df_author
