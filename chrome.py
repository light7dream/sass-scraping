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

commissions_0 = []
commissions_1 = []
categories = []
titles = []

driver = uc.Chrome(driver_executable_path=ChromeDriverManager().install())
driver.maximize_window()

LOGIN_URL = "https://affilisting.com/login"

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

            titles.append(td_elements[0].find_elements(By.TAG_NAME, 'div')[0].get_attribute('innerHTML'))
            categories.append(rounds)
            commissions_0.append(td_elements[1].get_attribute('innerHTML'))
            commissions_1.append(td_elements[2].get_attribute('innerHTML'))

            save_into_excelfile()

    except:
        print("error")
    

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

