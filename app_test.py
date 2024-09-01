from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import json
import time

# Function to automate Gmail login and email address capture
def automate_gmail_login(email, password, recipient_names):
    # Create a new instance of the browser driver
    driver = webdriver.Chrome()  # or webdriver.Firefox()
    
    # Open Gmail login page
    driver.get("https://contacts.google.com")

    # Log in to Gmail
    driver.find_element(By.ID, "identifierId").send_keys(email + Keys.RETURN)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "Passwd"))).send_keys(password + Keys.RETURN)
    
    # Wait for the Contacts page to load
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//input[@aria-label='Search']")))

    email_addresses = {}

    for recipient_name in recipient_names:
        # Find the search bar
        search_bar = driver.find_element(By.XPATH, "//input[@aria-label='Search']")
        
        # Clear the search bar using JavaScript
        driver.execute_script("arguments[0].value = '';", search_bar)
        
        # Enter the recipient name and search
        search_bar.send_keys(recipient_name)
        search_bar.send_keys(Keys.RETURN)
        
        # Wait for the search results and go to the profile
        time.sleep(2)  # Adjust as needed
        try:
            # Click on the first profile that appears in the search results
            first_profile = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//div[@role='option']"))
            )
            first_profile.click()

            # Wait for the profile page to load and locate the email elements
            email_elements = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, "//div[@data-email]"))
            )
            
            # Extract emails
            extracted_emails = []
            for element in email_elements:
                email = element.get_attribute("data-email")
                if email:
                    extracted_emails.append(email)
            
            # Store the emails for this recipient
            if extracted_emails:
                email_addresses[recipient_name] = extracted_emails
                print(f"Captured Emails for {recipient_name}: {extracted_emails}")
            else:
                email_addresses[recipient_name] = None

        except Exception as e:
            print(f"Failed to retrieve email for {recipient_name}: {e}")
            email_addresses[recipient_name] = None

        # Go back to the search page
        driver.execute_script("window.history.go(-1)")
        time.sleep(2)  # Adjust as needed

    # Save captured emails as JSON
    with open('captured_emails.json', 'w') as json_file:
        json.dump(email_addresses, json_file, indent=4)

    # Clean up: close the browser
    driver.quit()

# Load names from Excel
df = pd.read_excel('dtbt.xlsx')  # Replace 'dtbt.xlsx' with your Excel file name
names_list = df['NAME'].tolist()  # Assuming the column is named 'NAME'

# Replace with your email and password
automate_gmail_login("sc5268@srmist.edu.in", "@sHI722VANSH", names_list)
