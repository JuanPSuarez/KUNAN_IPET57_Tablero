import pandas as pd
import numpy as np


def process_issues(issues, author_ids=None, updated_date_range=None, created_date_range=None):
    data = []
    additional_fields_data = []

    for issue in issues:
        custom_fields = issue.custom_fields
        custom_fields_data = {field.name: field.value for field in custom_fields}
        author_id = issue.author.id

        created_on = pd.to_datetime(issue.created_on)
        updated_on = pd.to_datetime(issue.updated_on)

        author_filter_passed = author_ids is None or author_id in author_ids
        updated_date_filter_passed = updated_date_range is None or (
                updated_date_range[0] <= updated_on <= updated_date_range[1])
        created_date_filter_passed = created_date_range is None or (
                created_date_range[0] <= created_on <= created_date_range[1])

        if updated_date_filter_passed:
            days_open = np.busday_count(created_on.date(), updated_on.date())

            issue_data = {
                'ID': issue.id,
                'Tipo': issue.tracker.name,
                'Author': issue.author.name,
                'Días abierto': days_open,
                'Oficina': custom_fields_data.get('Oficina', None),
                'Canal de contacto': custom_fields_data.get('Canal de contacto', None),
                'Sistemas F': issue.custom_fields.get('Sistema') or issue.tracker.name,
                'Modulos F': ', '.join([custom_fields_data.get('Trámite', ''),
                                        custom_fields_data.get('Modulo Rcd', ''),
                                        custom_fields_data.get('Modulo Generales y Tramites', '')]).strip(', ')
            }

            data.append(issue_data)

        if author_filter_passed and created_date_filter_passed:
            additional_issue_data = {
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

            additional_fields_data.append(additional_issue_data)

    df = pd.DataFrame(data)
    additional_df = pd.DataFrame(additional_fields_data)

    df = df.sort_values(by='ID')
    additional_df = additional_df.sort_values(by='ID')

    return df, additional_df
