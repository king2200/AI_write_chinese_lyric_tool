import os
from collections import Counter
import jieba
from wordcloud import WordCloud, ImageColorGenerator
import re
#import matplotlib.pyplot as plt
#from scipy import imread
import cv2
from pylab import mpl
from PIL import Image
import numpy as np

#第一步：定义停用词库
def stopwordslist(filepath):
    stopwords = [line.strip() for line in open(filepath, 'r').readlines()]
    return stopwords
stopwords=stopwordslist('/Users/wangyun/Downloads/stopwords-master/cn_stopwords.txt')

# 第二步：读取文件，分词，生成all_words列表，用停用词检查后生成新的all_words_new
all_words=[]
main_word="爱情"
outstr = ''
specail_list = ['',"\n",'(', ')', '～', '(', '（', '）','Oh','ho','】', main_word]
root_path = '/Users/wangyun/Downloads/163music'
for dir_name in os.listdir(root_path):
    if dir_name[0] == '.':
        continue
    for filename in os.listdir(root_path + '/' + dir_name):
        with open(root_path + '/' + dir_name + '/' + filename) as f:
            lyrics = f.readlines()
            for line in lyrics:
                if line.find(':') != -1:
                    continue
                str = re.sub('[a-zA-Z0-9’!"#$%&\'()*+,-./:;<=>?@，。?★、…【】《》？“”‘’！[\\]^_`{|}~\s]+', "", line)
                data = jieba.cut(line)
                tmp_line_words = list(data)
                if main_word in tmp_line_words:
                    all_words.extend(tmp_line_words)



for word in all_words:
    if word not in stopwords:
        if word != '\t':
            outstr += word
            outstr += " "
all_words_new= outstr.split(" ") #转成列表
def is_cn(n):
    for ch in n:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
        else:
            return False
def is_special_word(n):
    if n in specail_list or is_cn(n) == False:
        return False
    else:
        return True

tmplist = filter(is_special_word, all_words_new)
all_words_new2 = list(tmplist)
#第三步：对all_words中的词计数，并按照词频排序
count=Counter(all_words_new2)
result=sorted(count.items(), key=lambda x: x[1], reverse=True)
print(result)
#第四步，词云显示
#将频率变成字典
word_dic=dict(count.items())

# 使matplotlib模块能显示中文
mpl.rcParams['font.sans-serif'] = ['SimHei'] # 指定默认字体
mpl.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题
color_mask = cv2.imread('/Users/wangyun/Downloads/backgroud4word.jpeg') #背景图

back_groud_image = np.array(Image.open('/Users/wangyun/Downloads/backgroud4word.jpeg'))
img_color = ImageColorGenerator(back_groud_image)

cloud = WordCloud(
    #font_path='/System/Library/Fonts/PingFang.ttc',
    font_path='/System/Library/AssetsV2/com_apple_MobileAsset_Font6/263f8d1ebcf06f4703bab24071039da20fb4bb92.asset/AssetData/Libian.ttc',
    width=color_mask.shape[1],
    height=color_mask.shape[0],
    background_color='white',
    mask=color_mask,
    max_words=350,
    max_font_size=150)
cloud.fit_words(word_dic)
#cloud.generate_from_frequencies(word_dic)
cloud.recolor(color_func=img_color)
cloud.to_file(root_path + '/' + main_word + '.jpeg')