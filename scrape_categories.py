import requests
from bs4 import  BeautifulSoup
import xlwt 
from xlwt import Workbook

URL = "https://www.ab.gr/en-gr/eshop"
headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36' }

page = requests.get(URL, headers=headers)
parser = BeautifulSoup(page.content, 'html.parser')
number = 0;
URL_list =[]
for div in parser.findAll('div', class_="gridItem"):
    #print(div)
    a = div.find('a')
   # print(a['href'])
    URL_list.append('https://www.ab.gr'+ a['href'])  
      #  a = li.find('li')
       # print(a['href'], a.get_text())
       # print(a)
    number = number +1
print('The URL given is:' + URL)
print("The Categories fall into the following "+ str(len(URL_list))+ " URLS:")

i=0
while i < len(URL_list):
    print(URL_list[i])
    i=i+1

print("Finding all the sub-pages of all the categories...")
URL_cat_list=[]
waiting = ''
for each_cat in URL_list:
    page_cat1 = requests.get(each_cat, headers=headers)
    parser_cat1 = BeautifulSoup(page_cat1.content, 'html.parser')
    for div in parser_cat1.findAll('li', class_="pagination-button"):
        a=div.find('a')
        #print(a['href'])
       # print(div)
       # a=div.findAll('a')
    #print(a.getText())
    waiting = waiting +'.'
    print(waiting)
    for x in range(int(a.getText())):
        URL_cat_list.append(each_cat+'?pageNumber='+str(x))
   #print(URL_cat_list)
   
print(URL_cat_list)
#print(len(URL_cat_list))
entries_list = []
prices_list = []
j=0
prices_counter = 0
wb = Workbook()
sheet1 = wb.add_sheet('Sheet 1')


URL_cat_list1 = ['https://www.ab.gr/en-gr/click2shop/New-Products/c/023?pageNumber=0','https://www.ab.gr/en-gr/click2shop/New-Products/c/023?pageNumber=1','https://www.ab.gr/en-gr/click2shop/New-Products/c/023?pageNumber=2' ]
for sub in URL_cat_list1:
    i = 1

    sub_page = requests.get(sub, headers=headers)
    parser_page = BeautifulSoup(sub_page.content, 'html.parser')
    title = parser_page.findAll('p', class_='ellipsis') # div class="description anchor--no-style"
    price = parser_page.findAll('span', class_='quantity-price super-bold')
    #print(price)
    #print(title)
    while i <= len(title):
        entries_list.append(title[i-1].text.strip() +' - '+ title[i].text.strip())

        sheet1.write(j,0,title[i-1].text.strip() +' - '+ title[i].text.strip() )
        #sheet1.write(j,1,price[i].text.strip()[0:8])
        
        #prices_list.insert(j,price[j].text.strip()[0:8])
        i = i + 2
        j = j + 1
    i = len(entries_list) + i
    #j = len(entries_list) + j 
    
    while price.__len__() > prices_counter:
        sheet1.write(prices_counter,1,price[i].text.strip()[0:8])
        prices_counter = prices_counter + 1
wb.save('extraction of data.xls')
print(entries_list) 
print(prices_list) 

  #  print(entries_list)   
    #for x in title:
   #     print(x)
    #    entries_list.insert((j), title[i-1].text.strip() +' - '+ title[i].text.strip())
    #    prices_list.insert(j,price[j].text.strip()[0:8])
    #    print(str(entries_list[j]) + " : "+str(prices_list[j]))   
    #print('entries legth'+str(len(entries_list)))
    #print(entries_list)

    #while price.__len__() > i:
    #    prices_list.insert(i,price[i].text.strip()[0:8])
    #    i = i+1
    #print(prices_list)
#while i < len(URL_cat_list):
#    print(str(entries_list[i]) + " : "+str(prices_list[i]))   
#   i=i+1