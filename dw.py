#!/usr/bin/python3
import argparse
from datetime import datetime
from art import tprint
from colorama import init
from colorama import Style, Fore


def find_day_week(line):
    week = gap(line, '%', '.')
    month = gap(line, '.', '"')
    carriage_day = 1
    while datetime(current_date.year, int(month), carriage_day).weekday() != directoryWeek[week]:
        carriage_day += 1
    need_day = gap(line, 3, '%')
    if need_day[0] == '!':
        need_day = gap(line, '!', '%')
        if int(month) == 2:
            many_days = 29 if is_leap(current_date.year) else 28
        else:
            many_days = 30 if int(month) % 2 == 0 else 31
        max_day_week = carriage_day + 28 if carriage_day + 28 < many_days else carriage_day + 21
        return max_day_week - 7 * (int(need_day) - 1)
    else:
        return carriage_day + 7 * (int(need_day) - 1)


def gap(line, begin='', end=''):
    if begin == '':
        return line[:line.index(end)] if not type(end) == int else line[:end]
    if end == '':
        return line[line.index(begin) + 1:] if not type(begin) == int else line[begin:]
    index_begin = line.index(begin) + 1 if not type(begin) == int else begin
    index_end = line.index(end) if not type(end) == int else end
    return line[index_begin:index_end]


def before_or_after(line, has_day=0):
    if line.find('~') > 0:
        day = gap(line, 3, '~') if not is_leap(current_date.year) else gap(line, '~', '.')
    if line.find('%') < 0 and line.find('~') < 0:
        day = gap(line, 3, '.')
    inf = delta(day, gap(line, '.', '"')) if has_day == 0 else delta(has_day, gap(line, '.', '"'))
    if inf > 0:
        inf = Fore.WHITE + str(inf) + Fore.CYAN + ' days left    \t|'
    else:
        inf = Fore.WHITE + str(inf * -1) + Fore.CYAN + ' days have passed\t|'
    return inf


def is_leap(year):
    return True if year % 4 == 0 else False


def convert_to_day(month_date):
    helper = int((month_date - 1) / 2)
    if helper == 0:
        helper += 1
    leap_year = 29 if is_leap(current_date.year) else 28
    if month_date <= 2:
        leap_year = 0
    coefficient = 1
    if month_date - 1 == 0:
        coefficient -= 1
    if (month_date - 1) % 2 == 0 or helper == 1:
        day_date = (helper - 1) * 30 + coefficient * (helper * 31) + leap_year
    else:
        day_date = (helper - 1) * 30 + (helper + 1) * 31 + leap_year
    return day_date


def delta(day_date, month_date):
    day_date = int(day_date)
    month_date = int(month_date)
    day_date += convert_to_day(month_date)
    day_current_date = current_date.day + convert_to_day(current_date.month)
    return day_date - day_current_date


def find_modifier(line, modifier):
    return True if line.find(modifier, 0, 3) == 1 else False


def print_line(line, day):
    if day:
        inf = before_or_after(line) if not find_modifier(line, 'w ') else before_or_after(line, day)
        print(inf, end='')
        print(Fore.WHITE + day, end='')
        print(' ' if len(str(day)) == 2 else '  ', end='')
        print(Fore.GREEN + listMonth[int(gap(line, '.', '"')) - 1], end='')
        if line.find('-b') > 0:
            birth = gap(line, 'b')
            age = current_date.year - int(birth)
            print(Fore.LIGHTBLUE_EX + ' turn ' + Fore.WHITE + str(age) + Fore.LIGHTBLUE_EX + ' |', end=' ')
        print(Fore.MAGENTA + gap(line, '"', line.index('-') - 1), end='\n+' + '-' * 78 + '+\n')


def find_modifiers(line):
    day = False
    if find_modifier(line, 'd '):
        day = gap(line, 3, '.')
    if find_modifier(line, 'v '):
        day = gap(line, 3, '~') if not is_leap(current_date.year) else gap(line, '~', '.')
    if find_modifier(line, 'w '):
        day = str(find_day_week(line))
    return day


def view_all():
    for line in file:
        day = find_modifiers(line)
        print_line(line, day)


def compare_date(day, month):
    return datetime(current_date.year, month, day) > current_date.now()


def print_text(line, day):
    print_line(line, day)
    line_text = file.readline()
    while line_text[0] != '"':
        print(Fore.WHITE + line_text)
        line_text = file.readline()


def view_nearest():
    for line in file:
        if find_modifiers(line):
            day = find_modifiers(line)
            month = gap(line, '.', '"')
            if compare_date(int(day), int(month)):
                print_text(line, day)
                break


def like_dates(date1, date2):
    return date1 == date2


def view_only():
    for line in file:
        if find_modifiers(line):
            day = find_modifiers(line)
            month = '.' + gap(line, '.', '"')
            if like_dates(day + month, args.viewOnly):
                print_text(line, day)
                return
    print('nothing')


if __name__ == "__main__":
    init()
    parser = argparse.ArgumentParser(
        prog=tprint('DATE WORKER'),
        description='save and replace dates',
        epilog='version 1.0.0'
    )
    parser.add_argument('-a', '--afternoon', action='store_true', help='displaying today`s date')
    parser.add_argument('-v', '--view', action='store_true', help='reading all dates')
    parser.add_argument('-vo', '--viewOnly', help='displays complete date information')
    parser.add_argument('-gn', '--getNearest', action='store_true', help='get nearest date')
    file = open('date.conf', 'r', encoding='utf-8')
    args = parser.parse_args()
    directoryWeek = {
        'monday': 0,
        'tuesday': 1,
        'wednesday': 2,
        'thursday': 3,
        'friday': 4,
        'sunday': 5,
        'saturday': 6
    }
    listMonth = ['january   |', 'february  |', 'mart      |', 'april     |', 'may       |', 'june      |',
                 'july      |', 'august    |', 'september |', 'october   |', 'november  |', 'december  |']
    current_date = datetime.now()
    if args.afternoon:
        print(Fore.BLUE + Style.BRIGHT + str(current_date.date()))
    if args.view:
        view_all()
    if args.viewOnly:
        view_only()
    if args.getNearest:
        view_nearest()
    file.close()

