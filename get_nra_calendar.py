#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import sys
import lxml.html
import requests

# 地方競馬情報サイト　月別開催日程のページ
target_url = 'http://www2.keiba.go.jp' \
           + '/KeibaWeb/MonthlyConveneInfo' \
           + '/MonthlyConveneInfoTop?k_year={0}&k_month={1}'

def print_manual():
    """マニュアル文を出力する。"""

    print("年を指定して下さい。")

def get_raceinfo_from_mark(mark):
    """●、☆、Ｄ、△の各マークを開催状態に変換する。

    戻り値はタプル(開催有無, 開催状態の説明)
    """

    if mark == '●':
        return (True, '通常開催')
    elif mark == '☆':
        return (True, 'ナイター競馬')
    elif mark == 'Ｄ':
        return (True, 'ダート交流重賞競争')
    elif mark == '△':
        return (False, '別の日に代替開催')
    else:
        return (False, 'なし')

def print_icalendar_start():
    print('')

def print_icalendar_end():
    print('')

def print_icalendar_data(year, month, day, racecourse, raceinfo):
    print('')


if __name__ == "__main__":

    # 引数から対象の年を取得（引数がない場合は使用法を表示）
    year = 0
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        year = int(sys.argv[1])

    if year == 0:
        print_manual()
        exit()

    # 1月から12月までループ
    for month in range(1, 12):

        # Webページを文字列として取得
        web_page = requests.get(str.format(target_url, year, month)).text

        # Webページからカレンダー部分を取り出す
        root = lxml.html.fromstring(web_page)
        racecourse_rows = \
            root.xpath('//td[@class="dbtbl"][1]/table/tr[td[@class="dbitem"]]')

        # 競馬場の行ごとにループ
        for racecourse_row in racecourse_rows:
            
            # 競馬場名を取得
            racecourse = racecourse_row \
                        .xpath('td[@class="dbitem"]')[0] \
                        .text_content() \
                        .strip()
            
            # 日ごとにループ
            day_cols = racecourse_row.xpath('td[@class="dbdata"]')
            for day in range(1, len(day_cols)):
                day_mark = str(day_cols[day-1].text_content()).strip()
                day_raceinfo = get_raceinfo_from_mark(day_mark)

                # iCalendar形式で出力
                if day_raceinfo[0]:
                     print(racecourse + '\t' + str(day) + '\t' + day_raceinfo[1])
