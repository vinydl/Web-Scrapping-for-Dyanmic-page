from selenium import webdriver as web 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
import sched
import datetime
import csv
s = sched.scheduler(time.time, time.sleep)

class scrape:
    def __init__(self):
        self.url="https://s.tradingview.com/miniwidgetembed/?Forex=FX%3AEURUSD%7C1d,FX%3AUSDJPY%7C1d,FX%3AGBPUSD%7C1d,FX%3AEURGBP%7C1d,FX%3AUSDCHF%7C1d,FX%3AUSDCAD%7C1d,FX%3AEURJPY%7C1d,FX%3AGBPJPY%7C1d,FX%3ACADJPY%7C1d,FX%3AUSDCNH%7C1d,FX_IDC%3AUSDCNY,FX%3AAUDJPY%7C1d,FX%3AAUDUSD%7C1d,FX%3ANZDUSD%7C1d,FX%3AAUDNZD%7C1d,FX%3AEURJPY%7C1d,FX%3AEURCHF%7C1d,FX%3AEURAUD%7C1d,FX%3AEURNZD%7C1d,FX%3AEURNOK%7C1d,FX%3AUSDHKD%7C1d,FX%3AUSDDKK%7C1d,FX%3AUSDMXN%7C1d,FX%3AUSDNOK%7C1d,FX%3AUSDSEK%7C1d,FX_IDC%3AUSDRUB%7C1d,FX_IDC%3AUSDSGD%7C1d,FX%3AUSDTRY%7C1d,FX%3AUSDTRY%7C1d,FX%3AGBPAUD%7C1d,FX%3AGBPCHF%7C1d,FX%3AGBPNZD%7C1d&Equities=S%26P500,NQ100,Dow30,Nikkei225,FTSE%20(UK100),DAX,FRA%20CAC40,Stoxx50,Shanghai%20A&Commodities=Gold,Silver,Oil%20WTI,Oil%20Brent,Gas&Bonds=US%202YR,US%2010YR,US%2030YR,Euro%20Bund,Euro%20BTP,Euro%20BOBL&tabs=Forex%2CEquities%2CCommodities%2CBonds&S%26P500=SPX500%7C1d&NQ100=NAS100%7C1d&Dow30=DOWI%7C1d&Nikkei225=JPN225%7C1d&FTSE%20(UK100)=FX%3AUK100%7C1d&DAX=GER30%7C1d&FRA%20CAC40=FRA40%7C1d&Stoxx50=EUSTX50%7C1d&Shanghai%20A=XGY0%7C1d&Gold=FX%3AXAUUSD%7C1d&Silver=FX%3AXAGUSD%7C1d&Oil%20WTI=FX%3AUSOIL%7C1d&Oil%20Brent=FX%3AUKOIL%7C1d&Gas=NG1!%7C1d&US%202YR=TUZ2015%7C1d&US%2010YR=TYZ2015%7C1d&US%2030YR=USZ2015%7C1d&Euro%20Bund=FX%3ABUND%7C1d&Euro%20BTP=EUREX%3AII1!%7C1d&Euro%20BOBL=EUREX%3AHR1!%7C1d&activeTickerBackgroundColor=%23eeeeee&trendLineColor=%239800ff&underLineColor=%23795492&fontColor=%2383888D&gridLineColor=%23eeeeee&large_chart_url=http%3A%2F%2Fwww.forexlive.com%2Flivecharts&width=100%25&height=1100px&utm_source=www.forexlive.com&utm_medium=widget&utm_campaign=market-overview"
        self.PJ = r'D:\Users\vinayaka.d\Desktop\Python projects\Forex\phantomjs-2.1.1-windows\bin\phantomjs.exe'
        
        self.driver = web.PhantomJS(self.PJ)
        self.currency =[]
        self.lastvalue =[]
        self.prevlastvalue = []
        self.change = []
        self.trend = []
        self.prevtrend = []
        self.trendmargin = []
        self.prevtrendmargin = []
        self.streak = []
        self.prevstreak = []
        
        
    def extractforex(self):

        while(int(time.strftime("%S"))<55):
            pass
        
        self.driver.get(self.url)

        try:

            #WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,'//div[starts-with(@id, "mainns_")]/iframe')))
            #WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//div[@class="pages"]/table')))
            #WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//div[@class="symbol-change"]')))
            #WebDriverWait(driver, 50).until(EC.visibility_of_element_located((By.CLASS_NAME, "symbol-last.falling")))
            #WebDriverWait(self.driver, 50).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "td[class='symbol-last growing']")))
            WebDriverWait(self.driver, 30).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "tr[class='ticker quote-ticker-inited']")))
            WebDriverWait(self.driver, 30).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div[style='opacity: 1; display: block;']")))
            html = self.driver.page_source
            #assert "Total Revenue" in html
            #print(html)
            #time.sleep(10)
            #html=driver.page_source.encode('utf-8')
            #print(html)
            print (time.strftime("%H:%M:%S"))
            print (time.strftime("%d/%m/%Y"))
            soup = BeautifulSoup(html,'html.parser')
            tabfin = soup.find('table',attrs={'class':'table'})
            #print(tabfin.prettify())

            self.currency =[t.get_text() for t in tabfin.findAll("a", { "class" : "symbol-short-name" })]
            #lastvalue = [t.get_text() for t in tabfin.findAll("a", { "class*" : "symbol-last","style" : "cursor: pointer;" })]
            #find('div', attrs={'id':'april2012'})
            self.lastvalue = ['0' if t.get_text()=='\xa0' else t.get_text() for t in tabfin.select("td[class*=symbol-last]")]
            self.lastvalue.pop(0)
            self.lastvalue = list(map(float, self.lastvalue))
            print(self.prevlastvalue)
            print(self.currency)
            print(self.lastvalue)
            self.change[:] = []
            if self.prevlastvalue:
                for idx, val in enumerate(self.lastvalue):
                    self.change.append(int(round((val - self.prevlastvalue[idx])*100000)))
            else:
                for idx, val in enumerate(self.lastvalue):
                    self.change.append(0)
            
            
            self.prevlastvalue[:] = []
            
            self.prevtrendmargin[:] = []
            self.prevstreak[:] = []
            self.prevtrend[:] = []
            
            for idx, val in enumerate(self.lastvalue):
                self.prevlastvalue.append(self.lastvalue[idx])
            #self.driver.quit()
            for idx, val in enumerate(self.currency):
                fn = val+".csv"
                fd = open(fn,'a')
              #  writer = csv.writer(fd)
                fd.write(str(time.strftime("%d/%m/%Y"))+';'+str(time.strftime("%H:%M:%S"))+';'+val+';'+str(self.lastvalue[idx])+';'+str(self.prevlastvalue[idx])+';')
                fd.write('\n')
                fd.close()

        except:
            print("Check internet, Its too slow!!!")
         
        time.sleep(30)
        
        

obj = scrape()
while True:
    if datetime.datetime.today().weekday()<7:
        obj.extractforex()
    else:
        print("Weekend!!!")

