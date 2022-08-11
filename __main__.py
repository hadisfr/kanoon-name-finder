#!/usr/bin/env python3

import re
import requests
from pprint import pprint
from sys import argv, stderr


def search_per_page(query, year, group_code, page):
    pattern = r"(?s)<tr>.*?/Public/StudentProfile/(?P<pid>.*?)\">\s*(?P<name>[^<\r\n]+)\s*</a>\s*</td>.*?>\s*(?P<city>[^<\r\n]+)\s*</td>.*?>\s*(?P<total_rank>[^<\r\n]+)\s*</td>.*?>\s*(?P<regional_rank>[^<\r\n]+)\s*</td>.*?>\s*(?P<region>[^<\r\n]+)\s*</td>.*?>\s*(?P<kanoon_year>[^<\r\n]+)\s*</td>.*?>\s*(?P<kanoon_score>[^<\r\n]+)\s*</td>.*?>\s*(?P<kanoon_tests>[^<\r\n]+)\s*</td>.*?>\s*(?P<major>[^<\r\n]+)\s*</td>.*?>\s*(?P<university>[^<\r\n]+)\s*</td>.*?</tr>"
    response = requests.get(
        "https://www.kanoon.ir/Public/ShowStudentListTable",
        params={
            "groupCode": group_code,
            "year": year-1300,
            "pageindex": page,
            "alphanum": -1,
            "list": "t",
        },
    )
    if response.status_code != 200:
        print("Could not get response:\t%s" % response.status_code, file=stderr)
        exit()
    res = response.text
    names_list = re.finditer(pattern, res)
    return res != "", filter(lambda m: re.match(query, m["name"]), map(
        lambda m: {**m, "year": year, "group": group_code},
        map(
            lambda match: match.groupdict(),
            names_list,
        )
    ))


def search_per_group(query, year, group_code):
    print("%d (group %d)" % (year, group_code))
    progress = True
    page = 0
    while progress:
        progress, res = search_per_page(query, year, group_code, page)
        for person in res:
            print_person(person)
        page += 1


def search_per_year(query, year):
    for group_code in [
        1,  # ریاضی
        3,  # تجربی
        5,  # انسانی
        7,  # هنر
        9,  # زبان
    ]:
        search_per_group(query, year, group_code)


def translate_group(group):
    return {
        1: "ریاضی",
        3: "تجربی",
        5: "انسانی",
        7: "هنر",
        9: "زبان",
    }.get(group, group)


def search(query, start_year):
    for year in range(start_year, 79, -1):
        search_per_year(query, year)


def print_person(person):
    person["link"] = create_link(person)
    person["group"] = translate_group(person["group"])
    print(pprint(person))


def create_link(person):
    return "http://www.kanoon.ir/Public/StudentProfile/%s" % person["pid"]


def main():
    query = input("query:\t") if len(argv) < 2 else argv[1]
    start_year = 1397 if len(argv) < 3 else int(argv[2])
    search(query, start_year)


if __name__ == '__main__':
    main()
