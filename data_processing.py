import pandas as pd
import numpy as np

def process_issues(issues_updated=None, issues_author=None, updated_date_range=None, created_date_range=None):
    data_updated = []
    data_author = []
    author_ids_to_filter = [117, 69, 143, 131, 113, 46, 145, 54, 135]

    if updated_date_range:
        updated_start_date = pd.to_datetime(updated_date_range[0]).replace(tzinfo=None)
        updated_end_date = pd.to_datetime(updated_date_range[1]).replace(tzinfo=None)
        created_start_date = pd.to_datetime(created_date_range[0]).replace(tzinfo=None)
        created_end_date = pd.to_datetime(created_date_range[1]).replace(tzinfo=None)
    else:
        updated_start_date = None
        updated_end_date = None
        created_start_date = None
        created_end_date = None

    if issues_updated:
        for issue in issues_updated:
            custom_fields = issue.custom_fields
            custom_fields_data = {field.name: field.value for field in custom_fields}

            created_on = pd.to_datetime(issue.created_on).replace(tzinfo=None)
            updated_on = pd.to_datetime(issue.updated_on).replace(tzinfo=None)

            if updated_date_range:
                updated_date_filter_passed = (
                    (updated_start_date is None or updated_start_date <= updated_on) and
                    (updated_end_date is None or updated_on <= updated_end_date)
                )
            else:
                updated_date_filter_passed = True

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

    if issues_author:
        for issue in issues_author:
            if issue.author.id in author_ids_to_filter:
                custom_fields = issue.custom_fields
                custom_fields_data = {field.name: field.value for field in custom_fields}

                created_on = pd.to_datetime(issue.created_on).replace(tzinfo=None)
                updated_on = pd.to_datetime(issue.updated_on).replace(tzinfo=None)

                if created_date_range:
                    created_date_filter_passed = (
                            (created_start_date is None or created_start_date <= created_on) and
                            (created_end_date is None or created_on <= created_end_date)
                    )
                else:
                    created_date_filter_passed = True

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

    return df_updated, df_author

