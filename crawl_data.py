from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver 
import re
import time 

def get_name(browser, names):
    column_els = browser.find_elements_by_xpath("//td[@valign='top']")
    for column_el in column_els:
        text = column_el.text 
        pattern = re.compile(r'[a-zA-Z_-]+')
        id_user = pattern.findall(text)
        names.extend(id_user)
    return names

browser = webdriver.Chrome(ChromeDriverManager().install())
url = "https://www.britishbabynames.com/blog/top-1000-names-in-england-and-wales-2015.html"
browser.get(url)

names = []
get_name(browser, names)
all_names = '\n'.join(names)
with open('all_names.txt', 'w') as f:
    f.write(all_names)

browser.close()