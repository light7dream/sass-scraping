from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
import pandas as pd
import time
from webdriver_manager.chrome import ChromeDriverManager
import pymongo

driver = uc.Chrome(driver_executable_path=ChromeDriverManager().install())
driver.maximize_window()

LOGIN_URL = "https://affilisting.com/login"

categories = []
program_datas = []

# Connect to the MongoDB server
client = pymongo.MongoClient("mongodb://localhost:27017/")

# Select the database
db = client["mydatabase"]

def log_in():
    driver.get(LOGIN_URL)
    time.sleep(10)

    email = "waynapayer@gmail.com"
    password = "Malitr$$324olr"

    email_field = driver.find_element(By.ID, 'email')
    email_field.send_keys(email)

    password_field = driver.find_element(By.ID, 'password')
    password_field.send_keys(password)

    submit_btn = driver.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/form/div[4]/button')
    submit_btn.click()

    time.sleep(10)


def save_into_excelfile():
    df = pd.DataFrame({'Title': titles, 'categories': categories, 'commissions0': commissions_0, 'commissions1': commissions_1,})  # Create a DF with the lists

    with pd.ExcelWriter('result.xlsx') as writer:
        df.to_excel(writer, sheet_name='Sheet1')


def get_data():

    try:
        #get the categories
        btn = driver.find_element(By.XPATH, '//*[@id="filter-section-0"]/div/div/div[1]/button')
        btn.click()
        time.sleep(10)
        lists = driver.find_element(By.XPATH, '//*[@id="options"]').find_elements(By.TAG_NAME, 'li')
        for i in range(len(lists)):
            element = lists[i]
            text = element.find_element(By.TAG_NAME, 'span').get_attribute('innerHTML')
            categories.append(text)

        #get the programs
        tr_elements = driver.find_element(By.TAG_NAME, "tbody").find_elements(By.TAG_NAME, "tr")
        for i in range(len(tr_elements)):
            tr_element = tr_elements[i]
            td_elements = tr_element.find_elements(By.TAG_NAME, 'td')
            round_elements = td_elements[0].find_elements(By.CLASS_NAME, "space-x-1")[0].find_elements(By.TAG_NAME, 'div')

            rounds = []
            for i in range(len(round_elements)):
                element = round_elements[i]
                text = element.find_element(By.TAG_NAME, 'span').get_attribute('innerHTML')
                rounds.append(text)

            title = td_elements[0].find_elements(By.TAG_NAME, 'div')[0].get_attribute('innerHTML')
            commission_0 = td_elements[1].get_attribute('innerHTML')
            commission_1 = td_elements[2].get_attribute('innerHTML')

            data = {"title": title, "categories": rounds, "commission_0": commission_0, "commission_1": commission_1}
            program_datas.append(data)
            
    except:
        print("error")
    
def get_random_rgbcolor():
    r = random.randint(100,255)
    g = random.randint(100,255)
    b = random.randint(100,255)
    rgb = "rgb" + str((r,g,b))
    return rgb;

def save_into_database():
    # Check if the collection exists
    if 'programs' in db.list_collection_names():
        program_collection = db['programs']
        program_collection.drop()

    if 'categories' in db.list_collection_names():
        category_collection = db['categories']
        category_collection.drop()

    program_collection = db.create_collection('programs')
    category_collection = db.create_collection('categories')

    for i in range(len(categories)):
        category = categories[i]
        color = get_random_rgbcolor()
        data = {"category": category, "color": color}
        category_collection.insert_one(data)

    program_collection.insert_many(program_datas)

def scrape_site():
    time.sleep(10)
    get_data()
    next_btn = driver.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/main/div/div/div[2]/div/main/section/div/div[2]/div[2]/div[1]/div[3]/div/div/div/nav/div[2]/button')
    while next_btn:
        next_btn.click()
        time.sleep(10)
        get_data()

        try:
            next_btn = driver.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/main/div/div/div[2]/div/main/section/div/div[2]/div[2]/div[1]/div[3]/div/div/div/nav/div[2]/button[2]')
        except:
            next_btn = None

def main():
    log_in()
    scrape_site()
    
if __name__ == '__main__':
    main()

