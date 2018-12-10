import json
from pprint import pprint
import datetime as dt
from collections import OrderedDict
from DayRecord import DayRecord

def get_city_data(path="./downloaded_data/SpasDemensk.json"):
    data = json.load(open(path, 'r'))
    city_name = data[0]['city']
    city_data = []
    for month in data[1:]:
        month_data = parse_month(month)
        city_data.extend(month_data)
    pcp_data = []
    for month in data[1:]:
        month_len = len(month['date'])
        year = month['year']
        for i in range(month_len - 1):
            date = month['date'][i] + ' ' + year
            pcp = month['R'][i]
            pcp_data.append([date, pcp])
    pcp_data = recount_pcp(pcp_data)[:-1]# last day pcp is not counable coz its needed 
    # next day pcp to recount it
    for dr, pcp, in zip(city_data, pcp_data):
        dr.pcp = pcp[1]
    # for el in pcp_data:
    #     print(el[0].isoformat(), '    ', el[1])
    return city_data, city_name

def recount_pcp(pcp_data):
    dates = OrderedDict()
    for el in pcp_data:
        try:
            date = dt.datetime.strptime(el[0], '%H %d.%m %Y').date()
        except ValueError:
            pcp_data.remove(el)
            continue
        if date not in dates:
            dates[date] = [el[1]]
        else:
            dates[date].append(el[1])
    records = [[key, value] for key, value in dates.items()]
    records_len = len(records)
    pcp = None
    for i in range(records_len - 1):
        today_pcp = records[i][1]
        tomorrow_pcp = records[i + 1][1]
        try:
            if today_pcp[5] != '':
                if tomorrow_pcp[1] != '':
                    pcp = float(today_pcp[5]) + float(tomorrow_pcp[1])
                else:
                    pcp = float(today_pcp[5])
            elif today_pcp[6] != '':
                if tomorrow_pcp[2] != '':
                    pcp = float(today_pcp[6]) + float(tomorrow_pcp[2])
                else:
                    pcp = float(today_pcp[6])
            elif tomorrow_pcp[1] != '':
                pcp = float(tomorrow_pcp[1])
            elif tomorrow_pcp[2] != '':
                pcp = float(tomorrow_pcp[2])
        except IndexError:
            pcp = None
        if pcp != None and pcp > 200:
            pcp = pcp / 50
        if pcp != None and pcp > 100:
            pass # avarage with nearest station!
        records[i][1] = pcp
        pcp = None
    return records


def parse_month(month):
    year = month['year']
    num_of_recs_by_day = num_of_records_by_day(month)
    # pprint(num_of_recs_by_day)
    i = 0
    month_records = []
    for key in num_of_recs_by_day.keys():
        j = i + num_of_recs_by_day[key]
        month_records.append(DayRecord(start=i, end=j, month_data=month, date=key))
        i += num_of_recs_by_day[key]
    return month_records


def num_of_records_by_day(month):
    year = month['year']
    month['date'] = month['date'][0:-1]
    num_of_recs_by_day = {}
    for date_str in month['date']:
        try:
            date = dt.datetime.strptime(date_str + " " + year, '%H %d.%m %Y')
        except ValueError:
            continue
        num_of_recs_by_day[date] = 0
    res = OrderedDict()
    for key in num_of_recs_by_day.keys():
        day = key.replace(hour=0)
        res[day] = 0
        for key2 in num_of_recs_by_day:
            if key.day == key2.day:
                res[day] += 1
    return res


# def print_month(month_data):
#     keys = month_data.keys()
#     number_of_recs = len(month_data['date']) - 1
#     for key in keys:
#         print("{:30s}".format(key), end=" ")
#     print()
#     for i in range(number_of_recs):
#         for key in keys:
#             if key == 'cloud':
#                 try:
#                     slash_index = month_data[key][i].index('/')
#                     print("{:30s}".format(month_data[key][i])[:slash_index], end=" ")
#                 except ValueError:
#                     print("{:30s}".format(month_data[key][i]), end=" ")
#                 continue
#             if key != 'year' and month_data[key][i] == "":
#                 print("{:30s}".format("_"), end=" ")
#                 continue
#             if key != 'year':
#                 print("{:30s}".format(month_data[key][i]), end=" ")
#         print()


if __name__ == '__main__':
    get_city_data()