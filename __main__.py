#!/usr/bin/env python3

import re
import requests
from pprint import pprint
from sys import argv, stderr


def search_per_page(name, year, group_code, page):
    pattern = r"(?s)<tr>.*?/Public/StudentProfile/(.*?)\">\s*([^<\r\n]+)\s*.*?</tr>"
    response = requests.get(
        "https://www.kanoon.ir/Public/ShowStudentListTable",
        params={
            "groupCode": group_code,
            "year": year,
            "pageindex": page,
            "alphanum": -1,
            "list": "t",
        },
    )
    if response.status_code != 200:
        print("Could not get response:\t%s" % response.status_code, file=stderr)
        exit()
    res = response.text
    names_list = re.findall(pattern, res)
    return res != "", map(
        lambda t: {"name": t[1], "pid": t[0], "year": year, "group": group_code},
        filter(lambda t: t[1] == name, names_list)
    )


def search_per_group(name, year, group_code):
    print("%d (group %d)" % (year, group_code))
    progress = True
    page = 0
    while progress:
        progress, res = search_per_page(name, year, group_code, page)
        for person in res:
            print_person(person)
        page += 1


def search_per_year(name, year):
    for group_code in [
        1,  # ریاضی
        3,  # تجربی
        5,  # انسانی
        7,  # هنر
        9,  # زبان
    ]:
        search_per_group(name, year, group_code)


def translate_group(group):
    return {
        1: "ریاضی",
        3: "تجربی",
        5: "انسانی",
        7: "هنر",
        9: "زبان",
    }.get(group, group)


def search(name, start_year=97):
    for year in range(start_year, 79, -1):
        search_per_year(name, year)


def print_person(person):
    person["link"] = create_link(person)
    person["group"] = translate_group(person["group"])
    print(pprint(person))


def create_link(person):
    return "http://www.kanoon.ir/Public/StudentProfile?year=%s&pid=%s" % (person["year"], person["pid"])


def main():
    name = input() if len(argv) == 1 else argv[1]
    search(name)


if __name__ == '__main__':
    main()
