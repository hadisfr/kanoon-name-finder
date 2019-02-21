#!/usr/bin/env python3

import re
import json
import requests


def search_per_page(name, year, group_code, page):
    pattern = r"<a[^>]*?href='/Public/StudentProfile\?year=(?P<year>[0-9]+)\&pid=(?P<pid>[0-9]+)'[^>]*?>[^<]*?%s" % name
    res = json.loads(requests.post(
        "http://www.kanoon.ir/Public/SuperiorsGroupBased.aspx/FillTableAjax",
        data="{'gc':'%d','year':'%d','pageindex':'%d','persiancher':'-1','ssahmie':'0','yyearinkanoon':'0'}" % (group_code, year, page),
        headers={'content-type': 'application/json'}
    ).text)['d']
    return res != "", re.findall(pattern, res)


def search_per_group(name, year, group_code):
    print("%d (group %d)" % (year, group_code))
    progress = True
    page = 0
    while progress:
        progress, res = search_per_page(name, year, group_code, page)
        if res:
            return res
        page += 1


def search_per_year(name, year):
    for group_code in [
        1,  # ریاضی
        3,  # تجربی
        5,  # انسانی
        7,  # هنر
        9,  # زبان
    ]:
        res = search_per_group(name, year, group_code)
        if res:
            return res


def search(name, start_year=97):
    for year in range(start_year, 79, -1):
        res = search_per_year(name, year)
        if res:
            return res


def create_link(year, pid):
    return "http://www.kanoon.ir/Public/StudentProfile?year=%s&pid=%s" % (year, pid)


def main():
    print(create_link(*search(input())[0]))


if __name__ == '__main__':
    main()
