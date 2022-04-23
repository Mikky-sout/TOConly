import re
import requests
import pandas as pd
import json


def getHTML():
    url = "https://en.wikipedia.org/wiki/List_of_best-selling_Nintendo_Switch_video_games"
    res = requests.get(url)
    res.encoding = "utf-8"
    source = str(res.text)
    allItem = re.findall(
        '<th scope="row">[/i<>]*<a href="/wiki/[^"]+" [clas=]*"?m?w?-?r?e?d?i?r?e?c?t?"? ?title="[^"]+">[<>i]*[^<]*[<>/i]*[^<]*[<>i]*[^<]*[<>/i]*[/ai<>]*\r*\n*</th>\r*\n<td><span data-sort-value="[0-9]*♠"[^<]*</span><span class="nowrap">&#160;</span>million<sup id="[^"]*" class="reference"><a href="[^"]*">[^<">]*</a></sup>\r?\n?</td>\r?\n?<td><span data-sort-value="[^"]*" style="white-space:nowrap">[a-zA-Z]+ [0-9]+, [0-9]+</span>\r?\n?</td>\r?\n?<td><span data-sort-value="[^"]*" style="white-space:nowrap">[a-zA-Z]+ [0-9]+, [0-9]+</span>\r?\n?</td>\r?\n?<td>[^=]*=?[^<]*[<>uli]*<a href="/wiki/[^"]+" [clas=]*"?m?w?-?r?e?d?i?r?e?c?t?"? ?title="[^"]*">[^<]+[</a>]*[<>uli]*[^>]*>?[^<]*[a-z/<>]*\r?\n?</td>\r?\n?<td>[<a href="/wik]*[a-zA-Z0-9_ ]* ?[clas=]?"?m?w?-?r?e?d?i?r?e?c?t?"? ?[tile="]*[a-zA-Z0-9_ ]*"?[^<]*[^t]*t?d?>?[<div clas=]*"?[a-zA-z0-9 _-]*"?>?<?u?l?>?<?l?i?>? ?"?[clas=]*"?m?w?-?r?e?d?i?r?e?c?t?"? ?[tile="]*[a-zA-Z0-9_ ]*"?>?[a-zA-z0-9 _-]*[</ali>]*[<a href="/wik]*[a-zA-Z0-9_. ]*"? ?[clas=]*"?m?w?-?r?e?d?i?r?e?c?t?"? ?[tile="]*[a-zA-Z0-9_. ]*"?>?[a-zA-Z0-9_. ]*[</alui>]*[/div>]*\r?\n?',
        source)
    return allItem

def listToPandas():
    text = getHTML()
    df = pd.DataFrame()
    nameList = []
    soldList = []
    updateList = []
    releaseList = []
    genreList = []
    devList = []
    webList = []
    for i, val in enumerate(text):
        name = re.search('title="[^"]*', val)
        name = name[0][7:]
        web = re.search('<th scope="row">[<i>]*<a href="/wiki/[^"]*',val)
        web = re.search('/wiki/[^"]*',web[0])
        web = 'https://en.wikipedia.org' + web[0]
        webList.append(web)
        nameList.append(name)
        sold = re.search('♠">[0-9.]+', val)
        sold = sold[0][3:]
        soldList.append(sold)
        date = re.findall('[a-zA-Z]+ [0-9]+, [0-9]{4}', val)
        updateDate = date[0]
        updateList.append(updateDate)
        releaseDate = date[1]
        releaseList.append(releaseDate)
        spText = val.split('<td>')
        genText = spText[4]
        genFound = re.findall('title="[^"]*', genText)
        genre = ''
        for x, gen in enumerate(genFound):
            if x == len(genFound) - 1:
                genre += gen[7:]
            else:
                genre += gen[7:] + ' , '
        genreList.append(genre)

        devText = spText[5]
        devFound = re.findall('title="[^"]*', devText)
        dev = ''
        if len(devFound):
            for x, d in enumerate(devFound):
                if x == len(devFound) - 1:
                    dev += d[7:]
                else:
                    dev += d[7:] + ' , '
        else:
            dev = re.search('[a-zA-Z0-9 _/%-]+', devText)[0]
        devList.append(dev)
    df['Name'] = nameList
    df['Copies sold'] = soldList
    df['Update'] = updateList
    df['Release'] = releaseList
    df['Genre'] = genreList
    df['Developer'] = devList
    df['Website'] = webList
    return df

def pandas2Json():
    df = listToPandas()
    obj = df.to_json(orient="records")
    parsed = json.loads(obj)
    return parsed

def saveJSON():
    parsed = pandas2Json()
    with open("data.json", "w", encoding="utf-8") as output:
        json.dump(parsed, output,ensure_ascii=False,indent=2)
        print("Save data completely")
    return parsed

def getJSON():
    with open("data.json", encoding='utf-8') as f:
        data = json.load(f)
    return data


