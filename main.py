import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QDateEdit, QPushButton, QLabel
from PyQt5.QtCore import QDate
import pandas as pd
from redmine_api import connect_to_redmine, get_issues
from data_processing import process_issues
from excel_export import export_to_excel
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

    def generate_report(self):
        updated_date_range = [
            pd.to_datetime(self.start_date_updated.date().toString("yyyy-MM-dd")),
            pd.to_datetime(self.end_date_updated.date().toString("yyyy-MM-dd")),
        ]

        created_date_range = [
            pd.to_datetime(self.start_date_created.date().toString("yyyy-MM-dd")),
            pd.to_datetime(self.end_date_created.date().toString("yyyy-MM-dd")),
        ]

        redmine_url = 'https://mesaregistrocivil.cba.gov.ar/redmine/'
        redmine_key = '5d6cec506b5b22ec8930ad02da88ceb8aa8955dc'
        project_id = 1

        redmine = connect_to_redmine(redmine_url, redmine_key)

        issues = get_issues(redmine, project_id)

        author_ids_to_filter = [117, 69, 143, 131, 113, 46, 145, 54, 135]

        df, additional_df = process_issues(
            issues, author_ids=author_ids_to_filter, updated_date_range=updated_date_range, created_date_range=created_date_range)

        excel_file = 'problemas_redmine.xlsx'

        export_to_excel(df, additional_df, excel_file)

        os.system('start excel.exe "{}"'.format(excel_file))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = RedmineReportApp()
    window.show()
    sys.exit(app.exec_())
