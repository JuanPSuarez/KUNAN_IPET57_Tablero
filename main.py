import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QDateEdit, QPushButton, QLabel
from PyQt5.QtCore import QDate
from redmine_api import connect_to_redmine, get_issues_by_update, get_issues_by_create
from data_processing import process_issues
from excel_export import export_to_excel
import os
from datetime import datetime, timedelta

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

    def generate_report(self):
        updated_start_date = self.start_date_updated.date().toString("yyyy-MM-dd") + "T00:00:00Z"
        updated_end_date = self.end_date_updated.date().toString("yyyy-MM-dd") + "T23:59:59Z"

        created_start_date = self.start_date_created.date().toString("yyyy-MM-dd") + "T00:00:00Z"
        created_end_date = self.end_date_created.date().toString("yyyy-MM-dd") + "T23:59:59Z"

        updated_start_date = datetime.strptime(updated_start_date, "%Y-%m-%dT%H:%M:%SZ") + timedelta(hours=3)
        updated_end_date = datetime.strptime(updated_end_date, "%Y-%m-%dT%H:%M:%SZ") + timedelta(hours=3)
        created_start_date = datetime.strptime(created_start_date, "%Y-%m-%dT%H:%M:%SZ") + timedelta(hours=3)
        created_end_date = datetime.strptime(created_end_date, "%Y-%m-%dT%H:%M:%SZ") + timedelta(hours=3)

        updated_start_date = updated_start_date.strftime("%Y-%m-%dT%H:%M:%SZ")
        updated_end_date = updated_end_date.strftime("%Y-%m-%dT%H:%M:%SZ")
        created_start_date = created_start_date.strftime("%Y-%m-%dT%H:%M:%SZ")
        created_end_date = created_end_date.strftime("%Y-%m-%dT%H:%M:%SZ")

        updated_date_range = [updated_start_date, updated_end_date]
        created_date_range = [created_start_date, created_end_date]

        redmine_url = 'https://mesaregistrocivil.cba.gov.ar/redmine/'
        redmine_key = '5d6cec506b5b22ec8930ad02da88ceb8aa8955dc'
        project_id = 1

        redmine = connect_to_redmine(redmine_url, redmine_key)

        issues_updated = get_issues_by_update(redmine, project_id, updated_date_range=updated_date_range)

        issues_created = get_issues_by_create(redmine, project_id, created_date_range=created_date_range)

        df_updated, df_created = process_issues(issues_updated, issues_created,
                                               updated_date_range=updated_date_range,
                                               created_date_range=created_date_range)

        excel_file = 'problemas_redmine.xlsx'

        export_to_excel(df_updated, df_created, excel_file)

        os.system('start excel.exe "{}"'.format(excel_file))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = RedmineReportApp()
    window.show()
    sys.exit(app.exec_())
