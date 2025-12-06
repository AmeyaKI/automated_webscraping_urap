from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import numpy as np
import time
import sys
from datetime import date

DEFAULT_EMAILS = [
    "berkeleyhousingstudy@gmail.com",
    "lailavoss@berkeley.edu",
]

def rnd_wait():
    return float(np.random.choice(np.arange(0.8, 2, 0.2)))

def parse_url(driver, url: str, repetitions=2):
    driver.get(url)
    wait = WebDriverWait(driver, 5)
    print(f"Fetching emails from {url}")
    
    # Email list to be returned
    email_list = []
    try:
        flagged = driver.find_elements(
            By.XPATH, "//*[contains(text(), 'This posting has been deleted') or contains(text(), 'deleted')]"
        )
        if flagged:
            print(f"[FLAGGED] {url.strip()} — using default emails.")
            email_list.extend(["berkeleyhousingstudy@gmail.com, lailavoss@berkeley.edu"])
            return email_list

        for _ in range(repetitions):
            # Reply Button
            time.sleep(rnd_wait())
            reply_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.reply-button")))
            reply_button.click()
            print("[INFO] Clicked reply button")

            # Email Button
            time.sleep(rnd_wait())
            email_button = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'email') or contains(text(), 'Email')]"))
            )
            email_button.click()
            print("[INFO] Clicked email button")

            # Craigslist Email
            time.sleep(rnd_wait())
            email_link = wait.until(
                EC.presence_of_element_located((By.XPATH, "//a[starts-with(@href,'mailto:')]"))
            )
            email_link = str(email_link.get_attribute("href"))
            email_link = email_link.replace("mailto:", "").split("?")[0]
            email_list.append(email_link)
            
            driver.refresh()

        return email_list[:2]
    except Exception as e:
        print(f"Error: {e}")
        email_list.extend(["berkeleyhousingstudy@gmail.com, lailavoss@berkeley.edu"])
        return email_list
    finally:
        driver.quit()
  

    
    
def compile_all(driver, url_list):
    formatted_urls = []
    for url in url_list:
        emails = parse_url(driver, url)
        formatted = f"{url}:::{emails[0]}, {emails[1]}"
        formatted_urls.append(formatted)
        
        time.sleep(rnd_wait())
    # formatted_results = "\n".join(formatted_urls)
    return formatted_urls
    

def results_to_txt(entries):
    today = date.today()
    filename = f'{today}_Emails.txt'
    with open(filename, 'a') as file:
        for line in entries:
            file.write(line + '\n')
        print("Saved to txt file.")
        file.close() 

def main():
    options = Options()
    options.add_argument("start-maximized")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")
    
    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(60)
    
    print("Paste all urls. Press Enter and Cntrl + D to proceed. ")
    url_list = sys.stdin.readlines()
    
    print("Urls Received. Starting collection of emails.")
    formatted_urls = compile_all(driver, url_list)
    
    results_to_txt(formatted_urls)
    
    

if __name__ == '__main__':
    main()



    
    
    
    # Test Code
    # url = "https://newyork.craigslist.org/que/roo/d/astoria-room-in-4br-available-in/7888003567.html"
    # email_list = parse_url(url, 2)
    # formatted_output = url_formatter(url, email_list)
    # print(formatted_output)
    
    
    
    