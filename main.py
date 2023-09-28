import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QDateEdit, QPushButton, QLabel
from PyQt5.QtCore import QDate
from redmine_api import connect_to_redmine, get_issues, get_issues2
from data_processing import process_issues
from excel_export import export_to_excel
from datetime import datetime, timedelta
import os

class RedmineReportApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Redmine Report Generator")
        self.setGeometry(100, 100, 400, 200)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout()

        self.start_date_updated = QDateEdit()
        self.start_date_updated.setDate(QDate(2023, 8, 1))
        self.start_date_updated.setCalendarPopup(True)
        layout.addWidget(QLabel("Start Date (Updated):"))
        layout.addWidget(self.start_date_updated)

        self.end_date_updated = QDateEdit()
        self.end_date_updated.setDate(QDate(2023, 9, 1))
        self.end_date_updated.setCalendarPopup(True)
        layout.addWidget(QLabel("End Date (Updated):"))
        layout.addWidget(self.end_date_updated)

        self.start_date_created = QDateEdit()
        self.start_date_created.setDate(QDate(2023, 8, 1))
        self.start_date_created.setCalendarPopup(True)
        layout.addWidget(QLabel("Start Date (Created):"))
        layout.addWidget(self.start_date_created)

        self.end_date_created = QDateEdit()
        self.end_date_created.setDate(QDate(2023, 9, 1))
        self.end_date_created.setCalendarPopup(True)
        layout.addWidget(QLabel("End Date (Created):"))
        layout.addWidget(self.end_date_created)

        self.generate_button = QPushButton("Generate Report")
        layout.addWidget(self.generate_button)

        self.generate_button.clicked.connect(self.generate_report)

        self.central_widget.setLayout(layout)

    def format_fecha(self, fecha_a_formatear):
        # Fecha y hora en formato ISO 8601 con 'Z'
        fecha_iso8601 = f'{fecha_a_formatear}'

        # Extraer la parte de la fecha y hora sin 'Z'
        fecha_sin_z = fecha_iso8601[:-1]

        # Convertir a objeto datetime
        fecha_datetime = datetime.fromisoformat(fecha_sin_z)

        # Sumar 3 horas
        nueva_fecha = fecha_datetime + timedelta(hours=3)

        # Convertir la nueva fecha a formato ISO 8601 con 'Z'
        nueva_fecha_iso8601 = nueva_fecha.isoformat() + 'Z'
     
        return nueva_fecha_iso8601

    def generate_report(self):
        updated_start_date = self.start_date_updated.date().toString("yyyy-MM-dd") + "T00:00:00Z"
        updated_end_date = self.end_date_updated.date().toString("yyyy-MM-dd") + "T23:59:59Z"

        created_start_date = self.start_date_created.date().toString("yyyy-MM-dd") + "T00:00:00Z"
        created_end_date = self.end_date_created.date().toString("yyyy-MM-dd") + "T23:59:59Z"

        updated_date_range = [self.format_fecha(updated_start_date), self.format_fecha(updated_end_date)]
        created_date_range = [self.format_fecha(created_start_date), self.format_fecha(created_end_date)]

        #print(updated_date_range)
        #print(created_date_range)

        redmine_url = 'https://mesaregistrocivil.cba.gov.ar/redmine/'
        redmine_key = '5d6cec506b5b22ec8930ad02da88ceb8aa8955dc'
        project_id = 1

        redmine = connect_to_redmine(redmine_url, redmine_key)

        #print('Conectado')

        issues_updated = get_issues(redmine, project_id, updated_date_range)
        issues_created = get_issues2(redmine, project_id, created_date_range)

        #print('Issues filtradas')
        #print(len(issues_created))

        df_updated, df_author = process_issues(issues_updated, issues_created)

        excel_file = 'problemas_redmine.xlsx'

        export_to_excel(df_updated, df_author, excel_file)

        #print('Exportando excel')

        os.system('start excel.exe "{}"'.format(excel_file))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = RedmineReportApp()
    window.show()
    sys.exit(app.exec_())