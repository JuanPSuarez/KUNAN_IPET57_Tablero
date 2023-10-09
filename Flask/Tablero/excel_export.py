import os
import pandas as pd


def export_to_excel(df, additional_df, excel_file):
    with pd.ExcelWriter(excel_file, engine='xlsxwriter') as writer:
        header_format = writer.book.add_format({'bg_color': '#006400', 'font_color': 'white'})

        df.to_excel(writer, sheet_name='Sis&Mod-Ofi-Res-Rec', index=False)
        worksheet1 = writer.sheets['Sis&Mod-Ofi-Res-Rec']
        for col_num, value in enumerate(df.columns.values):
            worksheet1.write(0, col_num, value, header_format)

        additional_df.to_excel(writer, sheet_name='Operador y Ticket por dia', index=False)
        worksheet2 = writer.sheets['Operador y Ticket por dia']
        for col_num, value in enumerate(additional_df.columns.values):
            worksheet2.write(0, col_num, value, header_format)

# CREADO POR https://www.instagram.com/s.ixtyn.ine/
# CREADO POR https://www.instagram.com/s.ixtyn.ine/
# CREADO POR https://www.instagram.com/s.ixtyn.ine/