import pyderman as pyder
from selenium import webdriver
from bs4 import BeautifulSoup
import urllib
import time
import json

def getBaanPage():
    return 'https://rubnongkaomai.com/baan'



path = pyder.install(browser=pyder.chrome, file_directory='./lib/', verbose=True, chmod=True, overwrite=False, version=None, filename=None, return_info=False)
driver = webdriver.Chrome(executable_path=path)
url = getBaanPage()
driver.get(url)
baanTable = []
from selenium.webdriver.common.keys import Keys

def clickBaan(driver, baanSize):
    allClick = driver.find_elements_by_xpath("//*[contains(text()," + baanSize +')]')
    for gonnaClick in allClick:
        gonnaClick.click()
    
    html = driver.find_element_by_tag_name('html')
    SCROLL_PAUSE_TIME = 1

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    html.send_keys(Keys.HOME)
    return
clickBaan(driver,"'บ้านขนาดเล็ก (S)'")
time.sleep(1)
clickBaan(driver,"'บ้านขนาดกลาง (M)'")
time.sleep(1)
clickBaan(driver,"'บ้านขนาดใหญ่ (L)'")
time.sleep(1)
clickBaan(driver,"'บ้านขนาดใหญ่พิเศษ (XL)'")
time.sleep(1)
soup = BeautifulSoup(driver.page_source, 'lxml')
allLink = soup.find_all('link')
allBaan = []
for link in allLink:
    if(link['href'] != None):
        if(link['href'].find('json') != -1 and link['href'].find('baan') != -1):
            allBaan.append(link['href'])
allBaan = list(set(allBaan))
print(len(allBaan))
for baan in allBaan:
    print(baan)
    jsonFile = urllib.request.urlopen('https://rubnongkaomai.com/' + baan).read()
    jsonContent = json.loads(jsonFile)
    #print(jsonContent['pageContext'])
    pageContext = jsonContent['pageContext']
    try:
        baanTable.append(('บ้าน' + pageContext['nameTH'], pageContext['sloganTH']))
    except:
        print("No nameTH or sloganTH")
    time.sleep(0.1)
print(baanTable)
table = open('table.html', 'w')
tableFile ="""<html>
                <head>
                    <style>
                        table, th, td {
                        border: 1px solid black;
                        border-collapse: collapse;
                        }
                        th, td {
                        padding: 5px;
                        text-align: left;    
                        }
                    </style>
                </head>
                <body>
                    <table style = "width:100%%">
                        <tr>
                            <th> ชื่อบ้าน </th>
                            <th> สโลแกน </th>
                        </tr>
                        %s
                    </table>
                </body>
            </html>    
            """
tableContent = ""
for baanDetail in baanTable:
    tableContent += "<tr>"
    tableContent += "<td>" + baanDetail[0] + "</td>"
    tableContent += "<td>" + baanDetail[1] + "</td>"
    tableContent += "</tr>"
whole = tableFile % tableContent
table.write(whole)
table.close()
