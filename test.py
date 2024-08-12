import math
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


def is_valid_email(email):
    regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return bool(re.match(regex, email))

file_path = 'Master Leads file.csv'
df = pd.read_csv(file_path)
df.drop_duplicates()
df_list = df.values.tolist()
options = Options()
options.add_argument('--disable-gpu')
# options.add_argument("--headless")
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-search-engine-choice-screen')
options.add_argument("--log-level=3")
options.add_argument("--silent")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options,)
new_list = []
new_list2 = []
df_list =[sublist for sublist in df_list if all(not (isinstance(item, float) and math.isnan(item)) for item in sublist)]
total = len(df_list)
index = 0
driver.get('https://disneyvacationclub.disney.go.com/sign-in?appRedirect=%2F&cancelUrl=%2F')
time.sleep(2)
iframe = driver.find_element(By.ID, 'oneid-iframe')
driver.switch_to.frame(iframe)
while (index < total):
    email = df_list[index]
    try:
        if is_valid_email(email[2]):
            email_key = driver.find_element(By.XPATH, '//*[@id="InputIdentityFlowValue"]')
            email_key.clear()
            email_key.send_keys(email[2])
            driver.find_element(By.XPATH, '//*[@id="BtnSubmit"]').click()
            time.sleep(0.5)
            check_text = driver.find_element(By.XPATH, '//*[@id="Title"]/span').text
            if check_text == 'Good news, you already have a MyDisney account':
                email.append('Email already registered')
                new_list.append(email)
                print(f"{index + 1} is verified out of {total}")
                index += 1
                driver.find_element(By.XPATH, '//*[@id="back"]').click()
            else:
                email.append('Email not registered')
                new_list2.append(email)
                print(f"{index + 1} is verified out of {total}")
                index += 1
                driver.find_element(By.XPATH, '//*[@id="back"]').click()
        else:
            email.append('Email not properly formatted')
            new_list2.append(email)
            print(f"{index + 1} is verified out of {total}")
            index += 1
        time.sleep(0.5)
    except Exception as e:
        driver.get('https://disneyvacationclub.disney.go.com/sign-in?appRedirect=%2F&cancelUrl=%2F')
        time.sleep(2)
        iframe = driver.find_element(By.ID, 'oneid-iframe')
        driver.switch_to.frame(iframe)
        print('continue')
        continue
driver.close()
df = pd.DataFrame(new_list, columns=['First_Name','Last_Name','Email', 'Status'])
df2 = pd.DataFrame(new_list2)
df.to_csv('output.csv', index=False)
df2.to_csv('output2.csv', index=False)