"""
制作人：18期爬虫-04-正则表达式-赵经纬
时间：2022-06-28
"""
import re
import requests
import csv
import time

'''
获取页面的歌名，歌手名
'''


def source(url):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    html = response.content.decode('utf-8')
    # print(html)
    return html


# 获取信息内容
def content(html):
    songlist = []
    re_text = re.findall('<textarea id="song-list-pre-data" style="display:none;">.*</textarea>', html)[0]
    # print(re_text)信息
    re_infos = re.findall('\[(.*)\]', re_text)[0]
    # print(re_infos,type(re_infos),len(re_infos))
    re_artistss = re.findall('("artists":.*?"fee":.*?"name".*?"id".*?)', re_infos)
    # print(re_artistss, len(re_artistss),type(re_artistss))
    for re_ratists in re_artistss:
        # print(re_ratists)
        # time.sleep(5)
        re_names=re.findall('"name":"(.*?)"',re_ratists)
        re_length=len(re_names)
        # print(re_names)
        # print(re_length)
        # 歌
        for i in range(0,re_length):
            songdict={}
            if re_names[-1]==re_names[i]:
                # 歌名
                songtitle=re_names[i]
            elif i==0:
                singer=re_names[i]
                # 歌手名
            else:
                singer=f'{singer}/{re_names[i]}'
        # print(songtitle,singer)
        songdict['songtitle']=songtitle
        songdict['singer']=singer
        songlist.append(songdict)
    return songlist
def save(songlist):
    header=['songtitle','singer']
    with open('歌单排行榜.csv','w',encoding='utf-8-sig',newline='') as f :
        writer=csv.DictWriter(f,header)
        writer.writeheader()
        writer.writerows(songlist)


def main():
    url = "https://music.163.com/discover/toplist"
    html = source(url)
    songlist=content(html)
    save(songlist)


if __name__ == '__main__':
    main()
