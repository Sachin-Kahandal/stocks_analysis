import requests
from bs4 import BeautifulSoup
from pandas import read_html
from selenium import webdriver
import time

# This code renders javascript generated html
# This requires to allow access to python of chrome webdriver
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
# your location of chromedriver.exe
# the version of chromedriver should be same as of browser
driver = webdriver.Chrome(r"C:\Users\Lenovo\.wdm\drivers\chromedriver\83.0.4103.39\win32\chromedriver.exe", options=options)


# Reliance Industries- script_code:500325 
def ratio_table(script_code):
    if len(str(script_code)) == 6:
        try:
            url = 'https://morningstar.in/handlers/autocompletehandler.ashx?criteria='+str(script_code)
            res = requests.get(url)
            soup = BeautifulSoup(res.text,'lxml')
            id = soup.select("id")[0].text
            url1 = 'https://financials.morningstar.com/ratios/r.html?t='+str(id)+'&culture=en&platform=sal'
            driver.get(url1)
            # Take a second to load javascript
            time.sleep(2)
            df = read_html(driver.page_source)
            financials = df[0].dropna().reset_index(drop=True)
            # margin_of_sales = df[1].dropna().reset_index(drop=True)
            # profitabilty = df[2].dropna().reset_index(drop=True)
            # growth = df[3].dropna().reset_index(drop=True)
            # cash_flow = df[4].dropna().reset_index(drop=True)
            # balance_sheet = df[5].dropna().reset_index(drop=True)
            # liquidity = df[6].dropna().reset_index(drop=True)
            # efficiency = df[7].dropna().reset_index(drop=True)
            return financials
        except:
            msg = {'info':'error, try extending time.sleep'}
    else:
        msg = {'info':'error'}
    return msg

    
def graham_data(script_code):
    if len(str(script_code)) == 6:
        # try:
        url = 'https://morningstar.in/handlers/autocompletehandler.ashx?criteria='+str(script_code)+''
        res = requests.get(url)
        soup = BeautifulSoup(res.text,'lxml')
        id = soup.select("id")[0].text
        url1 = 'https://financials.morningstar.com/ratios/r.html?t='+str(id)+'&culture=en&platform=sal'
        driver.get(url1)
        # Take a second to load javascript
        time.sleep(2)
        soup = BeautifulSoup(driver.page_source, 'lxml')
        graham = dict()
        graham['book_value'] = soup.select('div#financeWrap tr:nth-of-type(20) td:nth-of-type(11)')[0].text
        graham['eps'] = soup.select('div#financeWrap tr:nth-of-type(12) td:nth-of-type(11)')[0].text
        # except:
        #     msg = {'info':'error'}
        #     return msg
    else:
        msg = {'info':'script_code should be of 6 digits'}
        return msg
    return graham


def dcf_data(script_code):
    # scrape cashflows
    if len(str(script_code)) == 6:
        # try:
        url = 'https://morningstar.in/handlers/autocompletehandler.ashx?criteria='+str(script_code)
        res = requests.get(url)
        soup = BeautifulSoup(res.text,'lxml')
        id = soup.select("id")[0].text
        url1 = 'https://financials.morningstar.com/ratios/r.html?t='+str(id)+'&culture=en&platform=sal'
        driver.get(url1)
        # Take a second to load javascript
        time.sleep(2)
        soup = BeautifulSoup(driver.page_source, 'lxml')

        cf = soup.select('div#financeWrap tr:nth-of-type(28) td:nth-of-type(n+1)')
        yr = soup.select('div#financeWrap th:nth-of-type(n+2)')
        cfps, year = list(), list()
        for i in range(0,11):
            a = cf[i].text
            cfps.append(a) 
            b = yr[i].text
            year.append(b)
            
        data = dict(zip(year, cfps))
        # except:
        #     msg = {'info':'error'}
        #     return msg
    else:
        msg = {'info':'script_code should be of 6 digits'}
        return msg
    return data,year
