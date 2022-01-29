
import requests
import datetime
import schedule
import datetime
import time
from bs4 import BeautifulSoup

# 모듈을 읽어 들입니다.
#list = []
TARGET_URL = 'https://notify-api.line.me/api/notify'
TOKEN = 'gFX3KsVTvX0MEvcQFN8W14lghJj0MCX2x2B862C3flV'

#today
now = datetime.datetime.now()
today = now.strftime('%Y-%m-%d')
today2 = now.strftime('%Y.%m.%d')

# 요청합니다.
def sendMessage(title,text,url):
    response = requests.post(
    TARGET_URL,
    headers={
        'Authorization': 'Bearer ' + TOKEN
    },
    data={
        'message': "\n"+title+"에 새로운 글이 추가되었습니다.\n"+text+'\n'+url
    }
    )
    print(response.text)  

#소프트웨어학부 크롤링
def software(): 
    count = 0 
    url = 'https://sw.ssu.ac.kr/bbs/board.php?bo_table=sub6_1'
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'}
    page = requests.get(url,headers=headers)
    page.content
    soup = BeautifulSoup(page.content,'html.parser')
    datelist = soup("td",class_="datetime")
    textlist = soup("td",class_="subject")

    for date in datelist:
        #if(today[2:] == date.get_text()):
        if('21-12-02'==date.get_text()):
            sendMessage("소프트웨어학부",textlist[count].get_text(),'https://sw.ssu.ac.kr/'+textlist[count].a.get('href')[2:])
            #print(date.get_text())
            #print(textlist[count].get_text())
            #print('https://sw.ssu.ac.kr/'+textlist[count].a.get('href')[2:])
        count+=1



def computer(): 
    count = 0
    datelist = [] 
    urlList = []
    today3 = '2012.02.27'
    url = 'http://cse.ssu.ac.kr/03_sub/01_sub.htm'
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'}
    page = requests.get(url,headers=headers)
    page.content
    soup = BeautifulSoup(page.content,'html.parser')
    
    tempUrlList = soup('a',class_="blue")
    for url in tempUrlList:
        urlList.append('http://cse.ssu.ac.kr/03_sub/01_sub.htm'+(url.get('href')))
    

    tempDateList1 = soup("td",class_="etc")
    for date in tempDateList1:
        if(date.get_text()[0].isdigit()):
            datelist.append(date.get_text())
            
    tempDateList2 = soup("td",class_="center")
    for date in tempDateList2:
        if(date.get_text()[0].isdigit()):
           datelist.append(date.get_text())
            
    textlist = soup.find_all("a",class_="blue")
    
        
    for date in datelist:
        if(today3 == date):
            sendMessage("숭실대 컴퓨터학부",textlist[count].get_text(),urlList[count])
        count +=1
    

    # sendMessage 설정해야함



def Interational():
    today3 ='2022.01.18'
    count = 0 
    dateList = []
    urlList = []
    url = 'https://scatch.ssu.ac.kr/%ea%b3%b5%ec%a7%80%ec%82%ac%ed%95%ad/?f&category=%EA%B5%AD%EC%A0%9C%EA%B5%90%EB%A5%98&keyword'
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'}
    page = requests.get(url,headers=headers)
    page.content
    soup = BeautifulSoup(page.content,'html.parser')
    tempDateList = soup.findAll("div",class_="row no-gutters align-items-center")
    textList = soup.findAll("span",class_="d-inline-blcok m-pt-5")
    
    for date in tempDateList:
        if(today3 == date.find('div',class_='notice_col1 m-text-left').get_text()[1:11]):
            sendMessage('숭실대 국제처',date.find('span',class_="d-inline-blcok m-pt-5").get_text(),date.a.get('href'))
            #print(date.find('div',class_='notice_col1 m-text-left').get_text()[1:11])
            #print(date.find('span',class_="d-inline-blcok m-pt-5").get_text())
            #print(date.a.get('href'))
            #print('\n----\n')
    




# 1시간마다 탐색 
schedule.every().day.at("16:14").do(software)
schedule.every().day.at("16:15").do(Interational)
schedule.every().day.at("16:16").do(computer)
# 요청 완료
while True:
    schedule.run_pending()
    time.sleep(1)
