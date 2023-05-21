from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from undetected_chromedriver import Chrome, ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import random
import time
from random import randrange
from webdriver_manager.chrome import ChromeDriverManager
import pymongo
import json
import re
import subprocess

options = ChromeOptions()
# prefs = {
#     "profile.managed_default_content_settings.images": 2,
#     "profile.managed_default_content_settings.stylesheets": 2
# }
# options.add_experimental_option("prefs", prefs)
options.add_experimental_option("excludeSwitches", ["enable-logging"])
# options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--disable-extensions')
options.add_argument('--disable-features=NetworkService')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--no-sandbox')
# options.add_argument('--blink-settings=imagesEnabled=false')
# options.add_argument('--disable-features=CSSStylusUsage')
options.add_argument("--disable-blink-features=AutomationControlled")
# options.add_argument("--pageLoadStrategy=none")

# # set network conditions to disable css and images
# network_conditions = {
#     'offline': False,
#     'latency': 5,  # additional latency (ms)
#     'download_throughput': 500 * 1024,  # download speed (bytes/s)
#     'upload_throughput': 500 * 1024  # upload speed (bytes/s)
# }
# options.set_network_conditions(offline=False, **network_conditions)

driver = Chrome(options=options, executable_path=ChromeDriverManager().install())
wait = WebDriverWait(driver, 500)
# Enable Chrome DevTools
driver.execute_cdp_cmd('Page.enable', {})

# Disable CSS
css_remove_script = '''
    var styleSheets = document.styleSheets;
    for (var i = 0; i < styleSheets.length; i++) {
        styleSheets[i].disabled = true;
    }
'''
driver.execute_script(css_remove_script)

driver.maximize_window()

LOGIN_URL = "https://affilisting.com/login"
modal_xpath = '//*[@id="app"]/div/div[2]/main/div/div[2]/div[2]/div/div/div/div[2]/div/div[3]/dl'
close_xpath = '//*[@id="app"]/div/div[2]/main/div/div[2]/div[2]/div/div/div/div[1]/button'
dropdown_xpath = '//*[@id="filter-section-0"]/div/div/div[1]/button'
ul_xpath = '//*[@id="options"]'

tags_file = open('tags.txt', 'w')
programs_file = open('products.txt', 'w')
platforms_file = open('platforms.txt', 'w')
geolocations_file = open('geolocations.txt', 'w', encoding='utf-8')
productlinks_file = open('productlinks.txt', 'w')

# Connect to the MongoDB server
client = pymongo.MongoClient("mongodb://localhost:27017/")

# Select the database
db = client["mydatabase"]

def log_in():
    driver.get(LOGIN_URL)
    
    email = "waynapayer@gmail.com"
    password = "Malitr$$324olr"

    email_field = wait.until(EC.presence_of_element_located((By.ID, 'email')))
    email_field.send_keys(email)

    password_field = driver.find_element(By.ID, 'password')
    password_field.send_keys(password)

    submit_btn = driver.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/form/div[4]/button')
    submit_btn.click()
    # time.sleep(20)

def get_tags():
    try:
        #get the tags
        dropdown1_xpath = '//*[@id="app"]/div/div[2]/main/div/div/div[2]/div/main/section/div/div[1]/div/div/div[1]/h3/button'
        btn = wait.until(EC.element_to_be_clickable((By.XPATH, dropdown1_xpath)))
        driver.execute_script("arguments[0].scrollIntoView();", btn)
        btn.click()
       
        btn = wait.until(EC.element_to_be_clickable((By.XPATH, dropdown_xpath)))
        btn.click()
        # btn = driver.find_element(By.XPATH, dropdown_xpath)
    
        lists = wait.until(EC.presence_of_element_located((By.XPATH, ul_xpath)))
        lists = lists.find_elements(By.TAG_NAME, 'li')
        for i in range(len(lists)):
            element = lists[i]
            text = element.find_element(By.TAG_NAME, 'span').get_attribute('innerText')
            tags_file.write(text + '\n')

        tags_file.close()

        btn.click()
        btn = wait.until(EC.element_to_be_clickable((By.XPATH, dropdown1_xpath)))
        btn.click()

        print("tags scraping success")
    except:
        print("get_tags error")
    

def get_platforms():
    try:
        #get the platforms
        dropdown1_xpath = '//*[@id="app"]/div/div[2]/main/div/div/div[2]/div/main/section/div/div[1]/div/div/div[2]/h3/button'
        
        btn = wait.until(EC.element_to_be_clickable((By.XPATH, dropdown1_xpath)))
        # driver.execute_script("arguments[0].scrollIntoView();", btn)
        btn.click()

        btn = wait.until(EC.element_to_be_clickable((By.XPATH, dropdown_xpath)))
        btn.click()

        lists = wait.until(EC.presence_of_element_located((By.XPATH, ul_xpath)))
        lists = lists.find_elements(By.TAG_NAME, 'li')

        for i in range(len(lists)):
            element = lists[i]
            text = element.find_element(By.TAG_NAME, 'span').get_attribute('innerText')
            platforms_file.write(text + '\n')

        platforms_file.close()

        btn.click()
        btn = wait.until(EC.element_to_be_clickable((By.XPATH, dropdown1_xpath)))
        btn.click()

        print("platforms scraping success")
    except:
        print("get_platforms error")
    

def get_geolocations():
    # #get the geolocations
    # dropdown1_xpath = '//*[@id="app"]/div/div[2]/main/div/div/div[2]/div/main/section/div/div[1]/div/div/div[3]/h3/button'
        
    # btn = wait.until(EC.element_to_be_clickable((By.XPATH, dropdown1_xpath)))
    # btn.click()

    # btn = wait.until(EC.element_to_be_clickable((By.XPATH, dropdown_xpath)))
    # btn.click()

    # lists = wait.until(EC.presence_of_element_located((By.XPATH, ul_xpath)))
    # lists = lists.find_elements(By.TAG_NAME, 'li')
        
    # for i in range(len(lists)):
    #     element = lists[i]
    #     text = element.find_element(By.TAG_NAME, 'span').get_attribute('innerText')
    #     geolocations_file.write(text + '\n')

    # geolocations_file.close()

    # btn.click()
    # btn = wait.until(EC.element_to_be_clickable((By.XPATH, dropdown1_xpath)))
    # btn.click()

    # print("geolocations scraping success")

    try:
        #get the geolocations
        dropdown1_xpath = '//*[@id="app"]/div/div[2]/main/div/div/div[2]/div/main/section/div/div[1]/div/div/div[3]/h3/button'
        
        btn = wait.until(EC.element_to_be_clickable((By.XPATH, dropdown1_xpath)))
        # driver.execute_script("arguments[0].scrollIntoView();", btn)
        btn.click()

        btn = wait.until(EC.element_to_be_clickable((By.XPATH, dropdown_xpath)))
        btn.click()

        lists = wait.until(EC.presence_of_element_located((By.XPATH, ul_xpath)))
        lists = lists.find_elements(By.TAG_NAME, 'li')
        
        for i in range(len(lists)):
            element = lists[i]
            text = element.find_element(By.TAG_NAME, 'span').get_attribute('innerText')
            geolocations_file.write(text + '\n')

        geolocations_file.close()

        btn.click()
        btn = wait.until(EC.element_to_be_clickable((By.XPATH, dropdown1_xpath)))
        btn.click()

        print("geolocations scraping success")
    except:
        print("get_geolocations error")
    


def get_elements(element):
    title = element.find_elements(By.TAG_NAME, 'td')[0].find_elements(By.TAG_NAME, 'div')[0].get_attribute('innerText')
    
    elements = driver.find_element(By.XPATH, modal_xpath).find_elements(By.TAG_NAME, "dd")
    affilication_type = elements[0].get_attribute('innerText')
    affilication_platform = elements[1].get_attribute('innerText')
    # if(affilication_platform.contains("</a>")):
    #     affilication_platform = elements[1].find_element(By.TAG_NAME, 'a').get_attribute('innerHTML')
    product_type = elements[2].get_attribute('innerText')
    geolocation = elements[3].find_element(By.TAG_NAME, 'div').get_attribute('innerText')
    # if geolocation.contains("<div>"):
    #     geolocation = ""
    commission_0 = elements[4].get_attribute('innerText')
    commission_1 = elements[5].get_attribute('innerText')

    rounds = []
    round_elements = driver.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/main/div/div[2]/div[2]/div/div/div/div[2]/div/div[4]/div/ul').find_elements(By.TAG_NAME, 'span')
    for i in range(len(round_elements)):
        round_element = round_elements[i].get_attribute('innerText')
        rounds.append(round_element)
    
    product_link = driver.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/main/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/a').get_attribute('href')
    productlinks_file.write(product_link + '\n')

    data = {"title": title, "type": affilication_type, "platform": affilication_platform, "product_type": product_type, "geolocation": geolocation, "commission_0": commission_0, "commission_1": commission_1, "tags": rounds}
    
    numbers = re.findall(r'\d+\.\d+|\d+', commission_0)
    if(len(numbers) > 0):
        number = float(numbers[0])
        data['num_commission_0'] = number

    numbers = re.findall(r'\d+\.\d+|\d+', commission_1)
    if(len(numbers) > 0):
        number = float(numbers[0])
        data['num_commission_1'] = number

    json.dump(data, programs_file)
    programs_file.write('\n')

def get_programdata():
    try:
        # tbody_element = wait.until(EC.presence_of_element_located((By.TAG_NAME, "tbody")))
        # tr_elements = tbody_element.find_elements(By.TAG_NAME, "tr")
        tr_elements = driver.find_element(By.TAG_NAME, "tbody").find_elements(By.TAG_NAME, "tr")
        for i in range(len(tr_elements)):
            tr_element = tr_elements[i]
            
            try:
                tr_element.click()
                #get elements from modal
                get_elements(tr_element)
                driver.find_element(By.XPATH, close_xpath).click()
            except:
                print("each element error")
    except:
        print("get_programdata error")
        
    
def get_random_rgbcolor():
    r = random.randint(100,255)
    g = random.randint(100,255)
    b = random.randint(100,255)
    rgb = "rgb" + str((r,g,b))
    return rgb;

def setStatus(status):
    # Find the first document in the collection and update it
    collection = db["schedules"]
    query = {}
    new_values = { "$set": { "running": status } }
    updated_doc = collection.find_one_and_update(query, new_values)
    # Print the updated document
    print(updated_doc)
        
def scrape_site():

    get_tags()
    get_platforms()
    get_geolocations()
    get_programdata()

    page_num = 0
    next_btn_path = '//*[@id="app"]/div/div[2]/main/div/div/div[2]/div/main/section/div/div[2]/div[2]/div[1]/div[3]/div/div/div/nav/div[2]/button'
    next_btn = wait.until(EC.element_to_be_clickable((By.XPATH, next_btn_path)))
    
    while next_btn:
        page_num += 1
        print(page_num)
        try:
            next_btn.click()
            # wait.until(EC.url_changes(f"https://affilisting.com/list?page={page_num}"))
            time.sleep(20)
            get_programdata()

            try:
                next_btn = driver.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/main/div/div/div[2]/div/main/section/div/div[2]/div[2]/div[1]/div[3]/div/div/div/nav/div[2]/button[2]')
            except:
                next_btn = None
        except:
            print("page scraping error")

    programs_file.close()
    productlinks_file.close()
    
    print("Scraping Success")


def main():
    try:
        setStatus(True)
        log_in()
        scrape_site()
    except:
        print("Scraping Failure")
    subprocess.run('node index.js', shell=False)

if __name__ == '__main__':
    main()

