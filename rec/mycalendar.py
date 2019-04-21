import datetime

class Day:
    def __init__(self, date, form, name):
        self.date = date
        self.form = form
        self.name = name

class Calendar:
    months_names = {
        1: 'January', 2: 'Feburary', 3: 'March', 4: 'April',
        5: 'May', 6: 'June', 7: 'July', 8: 'August',
        9: 'September', 10: 'October', 11: 'November', 12: 'December'
    }

    def __init__(self):
        pass

    @staticmethod
    def get_month(day):
        month = [
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0]
        ]
        month_day_count = 28
        if day.date.month in [1, 3, 5, 7, 8, 10, 12]:
            month_day_count = 31
        if day.date.month in [4, 6, 9, 11]:
            month_day_count = 30
        if day.date.month == 2 and day.date.year % 4 == 0:
            month_day_count = 29
        date: int = 1
        for i in range(6):
            for j in range(7):
                if i == 0 and j >= datetime.date(day.date.year,
                                                 day.date.month,
                                                 1).weekday():
                    if datetime.date(day.date.year,
                                     day.date.month,
                                     date).weekday() in [5, 6]:
                        month[i][j] = Day(date, 'Vacancy', 'Day')
                    else:
                        month[i][j] = Day(date, 'Work', 'Day')
                    date += 1
                else:
                    if i > 0 and date <= month_day_count:
                        if datetime.date(day.date.year,
                                         day.date.month,
                                         date).weekday() in [5, 6]:
                            month[i][j] = Day(date, 'Vacancy', 'Day')
                        else:
                            month[i][j] = Day(date, 'Work', 'Day')
                        date += 1
        return month





