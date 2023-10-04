#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  1 20:58:25 2023

@author: yunusemreavci
"""

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
import os
from datetime import datetime

# Initialize Driver
browser = webdriver.Safari()
browser.maximize_window()

# Create a directory to hold screenshots
screenshot_folder = "tenant_screenshots"
if not os.path.exists(screenshot_folder):
    os.makedirs(screenshot_folder)

# Get date and time    
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

# Residents Payment Page credentials
mail_address = "your_mail_address"
password = "password"

# head to resident portal login page
browser.get('https://jmark.twa.rentmanager.com/?locationID=arizona')

time.sleep(2)

# find username/email field and send the username itself to the input field
browser.find_element("id", "Username").send_keys(mail_address)
# find password input field and insert password as well
browser.find_element("id", "Password").send_keys(password)
# click login button
login_button = browser.find_element(by='xpath', value='/html/body/div[3]/div/form/div/div/div[8]/input')
login_button.click()

errors = [NoSuchElementException, ElementNotInteractableException]

wait = WebDriverWait(browser, timeout=10,ignored_exceptions=errors)

# Charges page
locator = (By.ID, "horizontal-charges")
wait.until(EC.presence_of_element_located(locator))

searchID = wait.until(EC.element_to_be_clickable((By.ID, "horizontal-charges")))
searchID.click()

time.sleep(3)  # wait for page

# Screenshot of charges page
screenshot_path = os.path.join(screenshot_folder, f"charges_{timestamp}.png")
browser.save_screenshot(screenshot_path)
browser.get_screenshot_as_file('/tenant_log/charges.png')

# Go back to main page
browser.back()

# Transactions page containing pagination
locator = (By.ID, "horizontal-transactions")
wait.until(EC.presence_of_element_located(locator))

searchID = wait.until(EC.element_to_be_clickable((By.ID, "horizontal-transactions")))
searchID.click()

# Follow the paginantion number
page_number = 1

while True:
    # Get SS each page on transactions
    time.sleep(3)  
    screenshot_name = f"transactions_{page_number}_{timestamp}.png"
    screenshot_path = os.path.join(screenshot_folder, screenshot_name)
    browser.save_screenshot(screenshot_path)
    
    print(f"{screenshot_name} saved!")

    # Check next button for pagination
    next_button = (By.ID, "TransactionsGrid_next")
    wait.until(EC.presence_of_element_located(next_button))

    next_button_element = browser.find_element(*next_button)

    # If "Next" button has "unavailable" or "disabled" classes it is last page
    if "unavailable" in next_button_element.get_attribute("class") or "disabled" in next_button_element.get_attribute("class"):
        print("Last page")
        break

    next_button = wait.until(EC.element_to_be_clickable((By.ID, "TransactionsGrid_next")))

    next_button.click()
        
    time.sleep(3) 

    page_number += 1


browser.quit()