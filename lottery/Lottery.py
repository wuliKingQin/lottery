import requests
import codecs
from bs4 import BeautifulSoup


# 彩票实体类
class Data(object):
    year = ''
    date = ''
    date_num = ''
    lottery_data = ''


# 得到彩票数据
def get_lottery_data(start=2016001, end=2017019):
    lottery_list = list()
    params = {'type': 'range', 'start': start, 'end': end}
    response = requests.get("http://baidu.lecai.com/lottery/draw/list/50", params=params)
    soup = BeautifulSoup(open('data.txt'), 'html.parser')
    for item in soup.find_all('tr'):
        a_str = item.find_all('a')
        if a_str:
            data = Data()
            for a in a_str:
                a_list = a.contents
                data.date_num = a_list[0]
            td_str = item.find_all('td')
            for td in td_str:
                if len(list(td.descendants)) == 1:
                    data_list = td.contents
                    if '-' in data_list[0]:
                        date = data_list[0]
                        date_list = date.split('-')
                        data.year = date_list[0]
                        data.date = date
            em_str = item.find_all('em')
            index = 0
            for em in em_str:
                if index == 0:
                    data.lottery_data += em.contents[0]
                elif index < 7:
                    data.lottery_data += ',' + em.contents[0]
                index += 1
            lottery_list.append(data)
    return lottery_list


# 将彩票数据写到txt文件，文件名由年来决定
def write_lottery_to_txt_file():
    old_year = ''
    file = None
    for lottery in get_lottery_data():
        if lottery.year != old_year:
            old_year = lottery.year
            if file:
                file.close()
            file = codecs.open(lottery.year + ".txt", 'w', 'utf-8')
        else:
            file.write(lottery.date_num + "\t" + lottery.date + "\t" + lottery.lottery_data + "\r\n")
    if file:
        file.close()


# 读文件数据
def read_txt_file(start=3, end=15):
    file_list = list()
    for index in range(start, end):
        file_list.append(str(2000 + index))
    data_list = list()
    for name in file_list:
        file = open(name + '.txt', 'r')
        while file:
            line = file.readline()
            if not line:
                break
            data = Data()
            lottery_list = line.split('    ')
            date = lottery_list[2].replace('\n', '')
            data.date = date
            data.year = date.split('-')[0]
            data.date_num = lottery_list[0]
            data.lottery_data = lottery_list[1].replace('|', ',')
            data_list.append(data)
        if file:
            file.close()
    return data_list

for data_item in read_txt_file():
    print(data_item.year, data_item.date_num, data_item.date, data_item.lottery_data)



