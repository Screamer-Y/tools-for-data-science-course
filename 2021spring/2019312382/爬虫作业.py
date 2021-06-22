#!/usr/bin/python

from bs4 import BeautifulSoup
import requests
import xlwt

def getitemList(url):
    Itcastitem =[]
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER'}
    #get信息
    res = requests.get(url,headers=headers)
    #解析
    soup = BeautifulSoup(res.content,'html.parser')
    Itcastitemname_divs = soup.find_all('div',class_='title')
    for Itcastitemname_div in Itcastitemname_divs:
        Itcastitemname_as=Itcastitemname_div.find_all('a')
        for Itcastitemname_a in Itcastitemname_as:
            Itcastitemname=[]
            Itcastitemname.append(Itcastitemname_a.get_text())
            Itcastitemname.append(Itcastitemname_a.get('href'))
            Itcastitem.append(Itcastitemname)
    huseinfo_divs = soup.find_all('div',class_='ItcastitemInfo')
    for i in range(len(huseinfo_divs)):
        info = huseinfo_divs[i].get_text()
        infos = info.split('|')
        #名称
        Itcastitem[i].append(infos[0])
        #类型
        Itcastitem[i].append(infos[1])
        #备注
        Itcastitem[i].append(infos[2])
    #价格
    Itcastitem_prices = soup.find_all('div',class_='totalPrice')
    for i in range(len(Itcastitem_prices)):
        #价格
        price = Itcastitem_prices[i].get_text()
        Itcastitem[i].append(price)
    return Itcastitem

#爬取样本详细信息
def detailinfo(url):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER'}
    res = requests.get(url,headers=headers)
    soup = BeautifulSoup(res.content,'html.parser')
    msg =[]
    listinfo = soup.find_all('span',class_='info')
    for i in listinfo:
        area = i.find('a')
        if(not area):
            continue
        hrefStr = area['href']
        if(hrefStr.startswith('javascript')):
            continue
        msg.append(area.get_text())
        break
    infolist = soup.find_all('div',id='infoList')
    num = []
    for info in infolist:
        cols = info.find_all('div',class_='col')
        for i in cols:
            pingmi = i.get_text()
            try:
                a = float(pingmi[:-2])
                num.append(a)
            except ValueError:
                continue
    msg.append(sum(num))
    return msg

#将房源信息写入excel文件
def writeExcel(excelPath,houses):
    workbook = xlwt.Workbook()
    #获取第一个sheet页
    sheet = workbook.add_sheet('git')
    row0=['标题','A','B','C','D','E','F','G']
    for i in range(0,len(row0)):
        sheet.write(0,i,row0[i])
    for i in range(0,len(houses)):
        house = houses[i]
        print(house)
        for j in range(0,len(house)):
            sheet.write(i+1,j,house[j])
    workbook.save(excelPath)

#主函数
def main():
    data = []
    for i in range(1,5):
        print('-----分隔符',i,'-------')
        if i==1:
            url ='http://www.itcast.cn/news/20170103/17414023367.shtml?xmtzly'
        itcastitem =getitemList(url)
        for item in itcastitem:
            link = item[1]
            if(not link or not link.startswith('http')):
                continue
            mianji = detailinfo(link)
            item.extend(mianji)
        data.extend(itcastitem)
    writeExcel('d:/item.xls',data)

if __name__ == '__main__':
    main()