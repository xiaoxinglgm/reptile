from bs4 import BeautifulSoup
from lxml import etree
import requests
import js2xml
import sys
import time
import random
import datetime
import xlwt

def select(h1,i):
    listOwner=h1.find("property",{"name":"owner"})
    htmlOwner=BeautifulSoup(str(listOwner),'lxml')
    listMid=htmlOwner.find(attrs={"value":True})
    strMid=str(listMid.attrs['value'])    

    listName=htmlOwner.find(attrs={"name":'name'})
    strName=listName.text.strip()
    
    listStat=h1.find("property",{"name":"stat"})
    htmlStat=BeautifulSoup(str(listStat),'lxml')
    listValue=htmlStat.findAll(attrs={'value':True})
    strAvid=str(listValue[0].attrs['value'])
    strReply=str(listValue[1].attrs['value'])
    strNowRK=str(listValue[2].attrs['value'])
    strHisRk=str(listValue[3].attrs['value'])
    strViewson=str(listValue[-1].attrs['value'])    

    htmlVD=h1.find("property",{"name":"videoData"})
    htmlVDs=BeautifulSoup(str(htmlVD),'lxml')
    h5=htmlVDs.find("property",{"name":"bvid"})
    strBvid=str(h5.text).strip()

    h6=htmlVDs.find("property",{"name":"tname"})
    strTname=str(h6.text).strip()

    h4=h1.find("property",{"name":"title"})
    strTitle=str(h4.text).strip()

    record='av'+strAvid+'   '+strBvid+'   播放量:'+strViewson+'   分区:'+strTname+"   标题:"+strTitle+'   评论:'+strReply+"   up主:"+strName+"   mid:"+strMid+'\n' 

    with open ("record.txt","a+",encoding='utf-8') as r: 
        r.write(record)
        r.close()
    sheet.write(i+1,0,strAvid)
    sheet.write(i+1,1,strBvid)
    sheet.write(i+1,2,strViewson)
    sheet.write(i+1,3,strTname)
    sheet.write(i+1,4,strTitle)
    sheet.write(i+1,5,strReply)
    sheet.write(i+1,6,strName)
    sheet.write(i+1,7,strMid)
    
if __name__=='__main__':
    book=xlwt.Workbook()
    countErr=0
    st1=6
    st2=10
    #用来控制时间间隔，越大越慢
    lastTime=''
    avid=1921057
    #起始avid
    headers={
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36'
    }
    for j in range(20000):
        nameSheet=str(avid+1)
        sheet = book.add_sheet(nameSheet,cell_overwrite_ok=True)
        sheet.write(0,0,'avid')
        sheet.write(0,1,'Bvid')
        sheet.write(0,2,'Viewson')
        sheet.write(0,3,'Tname')
        sheet.write(0,4,'Title')
        sheet.write(0,5,'Reply')
        sheet.write(0,6,'Name')
        sheet.write(0,7,'mid')
        x=0
        for i in range(20000): 
            x+=1   
            avid+=1
            url="https://www.bilibili.com/video/av"+str(avid)
            try:
                html=requests.get(url,headers=headers)
            except: 
                print("html request error "+str(avid)+' '+str(datetime.datetime.now()))
            bs4Obj=BeautifulSoup(html.text,'lxml')       
            srcScript=bs4Obj.select("script")
            
            
            
            if len(srcScript)>4: 
                try:
                    srcElement=js2xml.parse(srcScript[3].string, encoding='utf-8', debug=False)
                    src_tree=js2xml.pretty_print(srcElement)
                    h1=BeautifulSoup(src_tree,"lxml")
                    select(h1,x)
                    time.sleep(random.random()*st1)
                    countErr=0
                    lastTime=str(datetime.datetime.now())
                    print("success: av"+str(avid))
                except:
                    time.sleep(random.random()*st2)                 
                    countErr+=1
                    if countErr>100:
                        time.sleep(300)
                        countErr=0
                    print('select error: '+str(avid)+"  CountErr: "+str(countErr)+"   now "+str(datetime.datetime.now())+'   last time '+lastTime)
                
        name='record'+str(avid)+'.xls'
        book.save(name)
        time.sleep(500)       

