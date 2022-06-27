import requests
import json
from datetime import datetime


class FindDate:
    def __init__(self):
        self.data = requests.get(
            'https://ct-mock-tech-assessment.herokuapp.com/').json()
        self.people = []
        for person in self.data['partners']:
            self.people.append({
                'name': f"{person['firstName']} {person['lastName']}",
                'availability': [date.replace("-", "/") for date in person['availableDates']],
                'country': person['country']
            })
        self.countries = []
        for person in self.data['partners']:
            self.countries.append(person['country'])
        self.countries = set(self.countries)
        self.chosen_dates = {}

    def determine_date(self, country):
        dates = []
        for person in self.people:
            if person['country'] == country:
                for date in person['availability']:
                    timestamp = datetime.timestamp(
                        datetime.strptime(date, "%Y/%m/%d"))
                    dates.append([date, timestamp])
        count_list = []
        for date in dates:
            count_list.append(dates.count(date))
        for date_index in range(len(dates)):
            dates[date_index].append(count_list[date_index])
            dates[date_index] = tuple(dates[date_index])
        dates = set(dates)
        dates = sorted(dates, key=lambda x: x[1])
        best_dates = ["day1", "day2"]
        date_sum = 0
        for date_index in range(len(dates)-1):
            potential_date_sum = dates[date_index][2] + \
                dates[date_index + 1][2]
            if date_sum < potential_date_sum:
                date_sum = potential_date_sum
                best_dates[0] = dates[date_index]
                best_dates[1] = dates[date_index + 1]
        self.chosen_dates[country] = [best_dates[0][0], best_dates[1][0]]

    def find_dates(self):
        for country in self.countries:
            self.determine_date(country)

    def display(self):
        for country in self.chosen_dates:
            print(country)
            print(
                f"Dates: {self.chosen_dates[country][0]} and {self.chosen_dates[country][1]}\n")
            print(f"Attendees:")
            attendee_count = 0
            for person in self.people:
                if (self.chosen_dates[country][0] in person['availability'] or self.chosen_dates[country][1] in person['availability']) and person['country'] == country:
                    print(person['name'])
                    attendee_count += 1
            print(f'\nAttendee Count: {attendee_count}')
            print('\n')

    @classmethod
    def run(self):
        solution = FindDate()
        solution.find_dates()
        solution.display()


start = FindDate()

start.run()
