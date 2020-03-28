#TODO on URL find "/" before the title and "/" after title to fix the category names
import requests
from bs4 import  BeautifulSoup
import xlwt 
from xlwt import Workbook
import openpyxl 
import re

def findAllSubCats():
    URL = "https://www.ab.gr/en-gr/eshop"
    headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36' }
    
    print('The URL given is:' + URL)
    page = requests.get(URL, headers=headers)
    parser = BeautifulSoup(page.content, 'html.parser')
    
    URL_list =[]
    for div in parser.findAll('div', class_="gridItem"):
        a = div.find('a')
        URL_list.append('https://www.ab.gr'+ a['href'])
    
    URL_list.remove(URL_list[0])  
    URL_list.remove(URL_list[-1])    
    URL_list.remove(URL_list[-1])  
    print("The Categories fall into the following "+ str(len(URL_list))+ " URLS:")
    
    i=0
    while i < len(URL_list):
        print(URL_list[i])
        i=i+1
    return URL_list    
def findAllPagesInCat(URL_list):
    headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36' }
    print("Finding all the sub-pages of all the categories...")
    URL_cat_list=[]
    waiting = ''
    for each_cat in URL_list:
        page_cat1 = requests.get(each_cat, headers=headers)
        parser_cat1 = BeautifulSoup(page_cat1.content, 'html.parser')
        for div in parser_cat1.findAll('li', class_="pagination-button"):
            a=div.find('a')
    
        waiting = waiting +'.'
        
        print(waiting)
        for x in range(int(a.getText())):
            URL_cat_list.append(each_cat+'?pageNumber='+str(x))
    
    print(URL_cat_list)
    return URL_cat_list   
def extractIntoExcel(URL_cat_list): 
    headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36' }
    entries_list = []
    
    wb = xlwt.Workbook()
    
    i = 0
    j = 0
    sheetname = re.sub(r'[^\w]', ' ', URL_cat_list[0][35:56])
    sheet1 = wb.add_sheet(sheetname)
    sheet1.col(0).width = 14000
    for cat in URL_cat_list:
        print("Extracting Products: " + cat)
    
        if sheetname != re.sub(r'[^\w]', ' ', cat[35:56]):
            sheet1 = wb.add_sheet(re.sub(r'[^\w]', ' ', cat[35:56]))
            sheet1.col(0).width = 14000
            sheetname = re.sub(r'[^\w]', ' ', cat[35:56])
            i = 0
            j = 0
            z = 0
        i = 1
        z = 0
        sub_page = requests.get(cat, headers=headers)
        parser_page = BeautifulSoup(sub_page.content, 'html.parser')
        title = parser_page.findAll('p', class_='ellipsis') # div class="description anchor--no-style"
        price = parser_page.findAll('span', class_='quantity-price super-bold')
    
        while i <= len(title):
            entries_list.append(title[i-1].text.strip() +' - '+ title[i].text.strip())
            sheet1.write(j,0,title[i-1].text.strip() +' - '+ title[i].text.strip() )
            sheet1.write(j,1,price[z].text.strip()[0:8])
    
            i = i + 2
            j = j + 1
            z = z + 1 
        i = len(entries_list) + i
        z = z +  len(entries_list)
    excel_name = input("Type how you want your excel file to be called")
    wb.save(excel_name+'.xls') 
def checkIfLegitInput(URL_str):
    URL_list = URL_str.split(',')
    print(URL_list)  
    len(URL_list)
    counter = 0
    for eachURL in URL_list:
        if eachURL.find('https://www.ab.gr/en-gr/click2shop/')!= -1:
            counter = counter + 1
            continue
        else:
            print("The URL: "+ eachURL+"found in position "+ str(counter)+" is invalid")
            print("Please re-enter the AB-Basilopoulos URLs of products correctly this time.")
            URL_list = []
            break
    return URL_list

def parseData(URL_list):
    headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36' }
    for each_URL in URL_list:
        sub_page = requests.get(each_URL, headers=headers)
        parser_page = BeautifulSoup(sub_page.content, 'html.parser')
        title = parser_page.find('h1', class_='page-title').text.strip() # div class="description anchor--no-style"
        price = parser_page.find('span', class_='ultra-bold test-price-property').text.strip()
        print(title)
        print(price)
        wb = xlwt.Workbook()
        sheet1 = wb.add_sheet("Price Tracking Sheet")
choice = input("Press 1 or 2: \n 1. Extract all the products (from all categories) of AB Basilopoulos into an excel  \n 2. Receive an automatic email when the price of a AB Basilopoulos product has gone down.\n")
if int(choice) == 1:
    #URL_
    URL_list = findAllSubCats()
    URL_cat_list = findAllPagesInCat(URL_list)
    extractIntoExcel(URL_cat_list)
else:  
    URL_str = input("Please copy and paste the URL of a specific product or if you want to add a list of products insert multiple URLS divided by ','(comma)\n")
    URL_list = checkIfLegitInput(URL_str)
    while len(URL_list) == 0:
        URL_str = input("Please copy and paste the URL of a specific product or if you want to add a list of products insert multiple URLS divided by ','(comma)\n")
        URL_list = checkIfLegitInput(URL_str)
    print("All URLs are correct.\n")
    parseData(URL_list)    
    #URL_list = findAllSubCats()
    #URL_cat_list = findAllPagesInCat(URL_list)
    #extractIntoExcel(URL_cat_list)
    