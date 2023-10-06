import pandas as pd
import numpy as np

def process_issues(issues_updated=None, issues_created=None, selected_operators=None):
    data_updated = []
    data_created = []
    author_ids_to_filter = selected_operators

    if issues_updated:
        for issue in issues_updated:
            custom_fields = issue.custom_fields
            custom_fields_data = {field.name: field.value for field in custom_fields}

            created_on = pd.to_datetime(issue.created_on)
            updated_on = pd.to_datetime(issue.updated_on)

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

    if issues_created:
        for issue in issues_created:
            if issue.author.id in author_ids_to_filter:
                custom_fields = issue.custom_fields
                custom_fields_data = {field.name: field.value for field in custom_fields}

                created_on = pd.to_datetime(issue.created_on)
                updated_on = pd.to_datetime(issue.updated_on)

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

                data_created.append(additional_issue_data_author)

    df_updated = pd.DataFrame(data_updated)
    df_created = pd.DataFrame(data_created)

    return df_updated, df_created

