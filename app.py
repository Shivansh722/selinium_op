from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Function to automate Gmail login and email address capture
def automate_gmail_login(email, password, recipient_name):
    # Create a new instance of the browser driver
    driver = webdriver.Chrome()  # or webdriver.Firefox()

    # Open Gmail login page
    driver.get("https://gmail.com")

    # Log in to Gmail
    driver.find_element(By.ID, "identifierId").send_keys(email + Keys.RETURN)
    time.sleep(2)  # Wait for the password field to load

    driver.find_element(By.NAME, "Passwd").send_keys(password + Keys.RETURN)
    time.sleep(5)  # Wait for Gmail to load

    # Click on the Compose button
    driver.find_element(By.XPATH, "//div[@role='button' and text()='Compose']").click()
    time.sleep(2)

    # Type the recipient's name in the 'To' field
    to_field = driver.find_element(By.ID, ":st")  # Updated to use the name attribute
    to_field.send_keys(recipient_name)
    time.sleep(2)  # Wait for suggestions to appear

    # Find the suggestion div using the class name
    suggestions = driver.find_elements(By.CLASS_NAME, "aL8")
    if suggestions:
        # Iterate through suggestions to find the one that matches the recipient name
        for suggestion in suggestions:
            if recipient_name in suggestion.get_attribute("data-name"):
                email_address = suggestion.get_attribute("data-hovercard-id")  # Get the email from data-hovercard-id
                print(f"Captured Email: {email_address}")
                break  # Exit loop after capturing the email

    # Clean up: close the browser
    driver.quit()

# Replace with your email, password, and recipient name
automate_gmail_login("sc5268@srmist.edu.in", "@sHI722VANSH", "AMRITESH KUMAR")
