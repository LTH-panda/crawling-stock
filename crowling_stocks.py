import requests as rq
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from openpyxl import Workbook


codes = []

for page in range(1, 20):
    url = f'https://finance.naver.com/sise/sise_market_sum.naver?&page={page}'
    html = rq.get(url).content
    soup = BeautifulSoup(html, 'html.parser')

    titlesTag = soup.select('.tltle')

    for titleTag in titlesTag:
        codes.append(titleTag.attrs['href'].split('/item/main.naver?code=')[1])

wb = Workbook()
sheet = wb.active
sheet.title = '주식 액면가 5000원 이상'
browser = webdriver.Chrome()

for code in codes:
    url = f'https://finance.naver.com/item/main.naver?code={code}'
    browser.get(url)

    try:
        price = browser.find_element(
            By.XPATH, '//*[@id="tab_con1"]/div[1]/table/tbody/tr[4]/td/em[1]').text
        if int(''.join(price.split(','))) >= 5000:
            name = browser.find_element(By.XPATH,
                                        '//*[@id="middle"]/div[1]/div[1]/h2/a').text
            current_price = browser.find_element(By.XPATH,
                                                 '//*[@id="chart_area"]/div[1]/div/p[1]/em').text

            sheet.append([name, current_price, price])
    except:
        pass

wb.save('주식.xlsx')

print('end')
