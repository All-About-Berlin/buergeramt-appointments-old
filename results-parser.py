from bs4 import BeautifulSoup, SoupStrainer
from datetime import date, datetime
from pathlib import Path
import csv
import json
from multiprocessing import Pool

pages_dir = Path('./output/')
page_paths = sorted(list(pages_dir.glob('*.html')))  # HTML pages saved by curl/wget

appointment_strainer = SoupStrainer('a', title='An diesem Tag einen Termin buchen')

appointments = {}
page_errors = {}


def get_appointment_dates(page_path):
    date_checked = datetime.strptime(page_path.stem.split('+')[0], "%Y-%m-%d,%H.%M")
    with page_path.open('r') as page_file:
        bookable_cells = BeautifulSoup(page_file, 'lxml', parse_only=appointment_strainer, from_encoding='utf-8').find_all('a')

    appointment_dates = []
    for bookable_cell in bookable_cells:
        timestamp = int(bookable_cell['href'].rstrip('/').split('/')[-1])
        appointment_dates.append(date.fromtimestamp(timestamp))

    return (date_checked, appointment_dates)


if __name__ == '__main__':
    print("Parsing pages")
    with Pool(4) as pool:
        results = pool.map(get_appointment_dates, page_paths)

    print("Merging results")
    for result in results:
        date_checked, appointment_dates = result
        date_checked_str = date_checked.strftime("%Y-%m-%dT%H:%M:%S")
        appointments.setdefault(date_checked_str, []).extend(appointment_dates)

    output = []
    for date_checked_str, appointment_dates in appointments.items():
        date_checked = datetime.strptime(date_checked_str, "%Y-%m-%dT%H:%M:%S")
        appointments_for_date = appointments.get(date_checked_str, [])
        earliest_date = min(appointments_for_date) if appointments_for_date else None
        earliest_date_str = earliest_date.strftime("%Y-%m-%dT%H:%M:%S") if earliest_date else None
        earliest_delta = (earliest_date - date_checked.date()).days if earliest_date else None

        output.append({
            'dateChecked': date_checked_str,
            'dateCheckedHour': date_checked.time().hour,
            'dateCheckedMinute': date_checked.time().minute,
            'dateCheckedDayOfWeek': date_checked.weekday(),
            'dateCheckedDayOfMonth': date_checked.day,
            'appointmentDaysFound': len(appointments_for_date),
            'earliestAppointmentDate': earliest_date_str,
            'earliestAppointmentDelta': earliest_delta,
        })

    print("Dumping to output.json")
    with open('output.json', 'w') as output_file:
        json.dump(output, output_file)

    print("Dumping to output.csv")

    fields = [
        'dateChecked', 'dateCheckedHour', 'dateCheckedMinute',
        'dateCheckedDayOfWeek', 'dateCheckedDayOfMonth', 'appointmentDaysFound',
        'earliestAppointmentDate', 'earliestAppointmentDelta'
    ]
    with open('output.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(output)
