import pyderman as pyder
from selenium import webdriver
from bs4 import BeautifulSoup
import urllib
import time
import json
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

#function to scroll the whole page(Thanks to Github)
def scrollAll(driver):
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

#function to select each baanSize to load JSON URL
def clickBaan(driver, baanSize):
    allClick = driver.find_elements_by_xpath("//*[contains(text()," + baanSize +')]')
    for gonnaClick in allClick:
        gonnaClick.click()
    scrollAll(driver)
    return

#Init driver  
path = pyder.install(browser=pyder.chrome, file_directory='./lib/')
options = Options()
options.add_argument("--headless")
options.add_argument("window-size=1920,1080") #use this size to avoid mobile window
driver = webdriver.Chrome(options = options, executable_path=path)
print(driver.get_window_size())
url = 'https://rubnongkaomai.com'
driver.get(url)

#Get BAAN to click (After observation, there is only 1 element with text() = 'BAAN')
allClick = driver.find_elements_by_xpath("//*[text()='BAAN']")
time.sleep(1)
print(len(allClick)) 

#Click BAAN to get to BAAN page
for baanClick in allClick:
    baanClick.click()
    time.sleep(1)

#Click All Size
baanSizeString = ["'บ้านขนาดเล็ก (S)'", "'บ้านขนาดกลาง (M)'", "'บ้านขนาดใหญ่ (L)'","'บ้านขนาดใหญ่พิเศษ (XL)'"]
for baanSize in baanSizeString:
    clickBaan(driver, baanSize)
    time.sleep(0.5)

#Find JSON URL
soup = BeautifulSoup(driver.page_source, 'lxml')
allLink = soup.find_all('link')
allBaan = []
for link in allLink:
    if(link['href'] != None):
        if(link['href'].find('json') != -1 and link['href'].find('baan') != -1):
            allBaan.append(link['href'])

#Unique list (After observation, there are times when there are repeated link)
allBaan = list(set(allBaan))
print("number of Baan: " + str(len(allBaan)))

#Add Tuple of (baanName, baanSlogan) to baanTable to write html later
baanTable = []
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

#Write table.html
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
                    <table>
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
    tableContent += "<tr>\n"
    tableContent += "<td>" + baanDetail[0] + "</td>\n"
    tableContent += "<td>" + baanDetail[1].replace('\n', '<br>') + "</td>\n"
    tableContent += "</tr>\n"
    print( baanDetail[1])
whole = tableFile % tableContent
table.write(whole)
table.close()
