import sys
import csv
import io
import argparse
import json
from datetime import datetime, timedelta

def last_date_of_the_week(date):
    if isinstance(date, datetime):
        start = date - timedelta(days=date.weekday())
        end = start + timedelta(days=6)
        return end.strftime('%Y-%m-%dT00:00:00Z')
    else:
        print('ERROR date could not be recognized!: {}'.format(date))
        return None

def first_date_of_the_week(date):
    start = date - timedelta(days=date.weekday())
    return start.strftime('%Y-%m-%dT00:00:00Z')

def string_to_date(string_value, format='%Y-%m-%dT%H:%M:%S%fZ'):
    return datetime.strptime(string_value, format)

def date_to_string(date_value, format='%Y-%m-%dT23:59:59Z'):
    return date_value.strftime(format)

def progress_bar(name, value, endvalue, bar_length=20):
    percent = 1.0 * value / endvalue
    arrow = '-' * int(round(percent * bar_length)-1) + '>'
    spaces = ' ' * (bar_length - len(arrow))
    sys.stdout.write("\r{0}: [{1}] {2}%".format(name, arrow + spaces, int(round(percent * 100))))
    sys.stdout.flush()


def sort_date_array(arr, format='%Y-%m-%dT%H:%M:%S.%fZ'):
    return sorted(arr, key=lambda x: x.strftime(format))

def write_model_to_csv(model, data):
    output = io.StringIO()
    writer = csv.writer(output, delimiter=',')
    if model is not None:
        writer.writerow(model)
    for row in data:
        write_arr = []
        for field in model:
            if field in row and row[field] is not None:
                write_arr.append(str(row[field]))
            else:
                write_arr.append('')
        writer.writerow(write_arr)
    return output.getvalue().encode('utf-8')


def write_rows_to_csv(rows):
    output = io.StringIO()
    writer = csv.writer(output, delimiter=',')
    for row in rows:
        writer.writerow(row)
    return output.getvalue().encode('utf-8')

def save_csv(path, data, model, delimiter=','):
    with open(path, mode='w') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=delimiter)
        if model is not None:
            csv_writer.writerow(model)
        for row in data:
            write_arr = []
            for field in model:
                if field in row and row[field] is not None:
                    write_arr.append(str(row[field]))
                else:
                    write_arr.append('')
            csv_writer.writerow(write_arr)
    print('File saved: {}'.format(path))

def save_json(path, data):
    with open(path, 'w') as outfile:
        json.dump(data, outfile, indent=4)
    print('File saved: {}'.format(path))


def read_har(path):
    harfile = open(path)
    harfile_json = json.loads(harfile.read())
    i = 0
    for entry in harfile_json['log']['entries']:
        i = i + 1
        yield entry

def read_csv(path, delimiter=',', skip_header=True):
    with open(path, 'r') as csvfile:
        rows = csv.reader(csvfile, delimiter=delimiter)
        counter = 0
        for row in rows:
            counter += 1
            if skip_header and counter == 1:
                continue
            yield row

def read_csv_to_object(path, encoding='ISO-8859-1', delimiter=','):
    keys = {}
    with open(path, 'r', encoding=encoding) as csvfile:
        rows = csv.reader(csvfile, delimiter=delimiter)
        counter = 0
        for row in rows:
            counter += 1
            if counter == 1:
                keys = row
                continue
            yield get_object_from_csv_row(keys, row)

def get_object_from_csv_row(keys, row):
    object = {}
    for i, value in enumerate(row):
        object[keys[i]] = value
    return object

def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


def next_weekday(d, weekday):
    days_ahead = weekday - d.weekday()
    if days_ahead <= 0:  # Target day already happened this week
        days_ahead += 7
    return d + timedelta(days_ahead)


def next_monday(d):
    return next_weekday(d, 0)  # 0 = Monday, 1=Tuesday, 2=Wednesday...


def percentage(value):
    return '{:.0f}%'.format(value * 100)

def human_readable_ms(duration):
    if duration > 1000:
        return '{:.2f}s'.format(duration / 1000)
    else:
        return '{:.2f}ms'.format(duration)

def human_readable_bytes(b):
    mbs = bytes_to(b, 'm')
    if mbs > 0:
        return bytes_to_mega_bytes(b)
    else:
        return bytes_to_kilo_bytes(b)

def bytes_to(bytes, identifier):
    to = {'k': 1, 'm': 2, 'g': 3}
    r = float(bytes)
    return  float(bytes) / (1024 ** to[identifier])

def bytes_to_mega_bytes(b):
    r = float(b)
    mbs = b / (1024 ** 2)
    return ('{:,.0f}mb'.format(bytes_to(b, 'm')))

def bytes_to_kilo_bytes(b):
    r = float(b)
    mbs = b / (1024 ** 1)
    return ('{:,.0f}kb'.format(bytes_to(b, 'k')))

def avg(values):
    return sum(int(value) for value in values) / len(values)

def median(values):
    values.sort()
    if len(values) / 2 != int:
        return values[len(values) / 2]
    else:
        return (values[len(values) / 2] + values[(len(values) / 2) - 1]) / 2
