import csv
import os
from datetime import datetime

class Employee:
    def __init__(self, id, username, password, name, role):
        self.id = id
        self.username = username
        self.password = password
        self.name = name
        self.role = role
#Name Splitter
    def split_name(self, name):
        parts = name.split(" ", 1)
        if len(parts) == 2:
            return parts[0], parts[1]
        else:
            return parts[0], "Not Provided"

#Clock in method to track employee time
    def clock_in(self):
        """Clock in the employee and log into employee_time.csv."""
        if not os.path.exists('data'):
            os.makedirs('data')

        time_file_path = os.path.join('data', 'employee_time.csv')
        time_fieldnames = ['id', 'username', 'clock_in_time', 'clock_out_time', 'date']
        time_file_exists = os.path.isfile(time_file_path)

        now = datetime.now()
        date_str = now.strftime('%Y-%m-%d')
        time_str = now.strftime('%H:%M:%S')

        with open(time_file_path, mode='a', newline='') as time_csv:
            writer = csv.DictWriter(time_csv, fieldnames=time_fieldnames)
            if not time_file_exists:
                writer.writeheader()

            writer.writerow({
                'id': self.id,
                'username': self.username,
                'clock_in_time': time_str,
                'clock_out_time': '',
                'date': date_str
            })

        print(f"{self.username} clocked in at {time_str} on {date_str}.")

#Clock Method To add employee clockout
    def clock_out(self):
        """Clock out the employee and update the employee_time.csv."""
        time_file_path = os.path.join('data', 'employee_time.csv')

        if not os.path.isfile(time_file_path):
            print("No time tracking file found.")
            return

        now = datetime.now()
        date_str = now.strftime('%Y-%m-%d')
        time_str = now.strftime('%H:%M:%S')

        rows = []
        updated = False

        with open(time_file_path, mode='r', newline='') as time_csv:
            reader = csv.DictReader(time_csv)
            for row in reader:
                if row['username'] == self.username and row['clock_out_time'] == '' and row['date'] == date_str:
                    row['clock_out_time'] = time_str
                    updated = True
                rows.append(row)

        if updated:
            with open(time_file_path, mode='w', newline='') as time_csv:
                fieldnames = ['id', 'username', 'clock_in_time', 'clock_out_time', 'date']
                writer = csv.DictWriter(time_csv, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rows)
            print(f"{self.username} clocked out at {time_str} on {date_str}.")
        else:
            print(f"No open clock-in record found for {self.username} today.")