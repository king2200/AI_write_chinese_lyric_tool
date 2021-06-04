# 第一部分：爬取数据
import requests
import re
import os
import json
from bs4 import BeautifulSoup
import urllib.request as urllib2
from selenium import webdriver


def validateTitle(title):
    rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
    new_title = re.sub(rstr, "_", title)  # 替换为下划线
    return new_title

#发起响应
def get_html(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36'}
    try:
        response = requests.get(url, headers=headers)
        html = response.content
        return html
    except:
        print('request error')
        pass

#函数：按照歌曲id，提取歌词内容
def download_by_music_id(music_id):
    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
              'Accept-Encoding': 'gzip, deflate',
              'Accept-Language': 'zh-CN,zh;q=0.9',
              'Cache-Control': 'max-age=0',
              'Connection': 'keep-alive',
              'Cookie': '_ntes_nnid=73f9fe5eabfd03ba0818a7cf3d837984,1596679531022; _ntes_nuid=73f9fe5eabfd03ba0818a7cf3d837984; mail_psc_fingerprint=455c7400ea385847f8c6ea142693674b; nts_mail_user=m18611621504_1@163.com:-1:1; P_INFO=m18611621504_1@163.com|1612765558|0|mail163|00&99|bej&1612765417&carddav#bej&null#10#0#0|186504&0||18611621504@163.com; _iuqxldmzr_=32; NMTID=00Ov4FBVVlHpva7e0_6uxE29qBsb10AAAF5jjz3lw; WEVNSM=1.0.0; WM_TID=ZCb6cgq3J2ZAREUVEAN%2BSuEGgDFd4ANJ; csrfToken=8hK86DjKMCdOmkQAUyyGupUW; WM_NI=59o4Uuz69iEEdTwn4UDLGDnWqxpKMOg5KXtEwIhF5RpGREycPW%2BpUHdEwzGHiJn7OTxtWUyAMnVAzMhJpNjZxVg0F4b9JN8SBexcQX4KWEUNt0RBlbxVjx3LbmpizzPyZFk%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6eea8ce59ba8be5d0b444ac968fa6c45a929b8eaef468b1ba00bad47fb1e7a895db2af0fea7c3b92af7e7a1d5d87fbaeaf78ac84fa88cb98fb75f889489a5ed5db3a8c0acd045a5eb85b9f74fb597a8a7b85ab4999ea6fc699489e591d844a89bb99bc644ab96a2d8ce60bcac99b6fc4b8fb29aa2f947ac96c0afe952bc8aa9d1c540a2e786afbb5982bbb884d454f89599a6d846b8f09ea3ef6abc8aa699b248a2b3c08af97294a796a7ea37e2a3; JSESSIONID-WYYY=yC%2Fw8vmZq%2FgYiHuI7%2FmhH5Ok6v2jElxz%2BRk4oTty%5ChW3cY5P0gH3snrrHViHbktRBkYd1MDZge6rTOyWxeYd4Vx%2FM%2B4PZrZkkgI3%5Cuw02nIn8Fpu%2FTO%2BPJTc95TSXgGzCWFCAf7VbS%2BlQQJ358AuK6Qsm4u52ig3j1rWnzWevjSidWXu%3A1621849766268',
              'Host': 'music.163.com',
              'Upgrade-Insecure-Requests': '1',
              'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'}
    lrc_url = 'http://music.163.com/api/song/lyric?'+'id='+str(music_id) + '&lv=1&kv=1&tv=-1'
    r = requests.get(lrc_url, headers=headers)
    json_obj = r.text
    j = json.loads(json_obj)
    try:
        lrc = j['lrc']['lyric']
        pat = re.compile(r'\[.*\]')
        lrc = re.sub(pat, "",lrc)
        lrc = lrc.strip()
        return lrc
    except:
        pass

#函数：按照歌手id，发起请求，解析网页，提取歌曲id
def get_music_ids_by_musician_id(singer_id):
    singer_url = 'http://music.163.com/artist?id={}'.format(singer_id)
    r = get_html(singer_url)
    soupObj = BeautifulSoup(r,'lxml')
    song_ids = soupObj.find('textarea').text
    jobj = json.loads(song_ids)
    ids = {}
    for item in jobj:
        print(item['id'])
        split_name = item['name'].split()
        tmp_name = "".join(split_name)
        new_tmp_name = validateTitle(tmp_name)
        ids[new_tmp_name] = item['id']
    return ids

def get_musician_ids():
    #1001表示话语男歌手
    singer_url = 'https://music.163.com/#/discover/artist/cat?id={}'.format(1001)
    driver = webdriver.Chrome(executable_path="/Users/wangyun/Downloads/chromedriver")
    driver.get(singer_url)
    iframe = driver.find_elements_by_tag_name("iframe")[0]
    driver.switch_to_frame(iframe)
    #r = get_html(singer_url)
    soupObj = BeautifulSoup(driver.page_source, 'lxml')
    sml_infos = soupObj.find_all('li', class_="sml")
    songer_dict = {}
    for info in sml_infos:
        info_soup = BeautifulSoup(str(info), 'lxml')
        tmp_href = info_soup.find('a').attrs['href']
        singer_num = re.findall("/artist\?id=(.+)", tmp_href)
        tmp_text = info_soup.find('a').text.strip()
        songer_dict[tmp_text] = singer_num[0]

    return songer_dict

# 创建文件夹，在文件夹下存储每首歌的歌词
# os.mkdir创建目录，os.chdir改变当前工作目录到指定的路径
def download_lyric(uid, name):
    tmp_name = name.replace(" ","")
    tmp_dir = "/Users/wangyun/Downloads/163music/" + tmp_name + '_' + str(uid)
    try:
        os.mkdir(tmp_dir)
    except Exception as e:
        print(e)
        pass

    os.chdir(str(tmp_dir))
    music_ids = get_music_ids_by_musician_id(uid)
    for key in music_ids:
        text = download_by_music_id(music_ids[key])
        file = open(key+'.txt', 'a')
        file.write(key+'\n')
        file.write(str(text))
        file.close()

if __name__ == '__main__':
    singer_dict = get_musician_ids()
    for name, id in singer_dict.items():
        download_lyric(id, name)

