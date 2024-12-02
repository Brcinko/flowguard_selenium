from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import credentials

# Replace these with your specific details
# LOGIN_URL = "https://example.com/login"
# USERNAME = "your_username"
# PASSWORD = "your_password"
# TARGET_PAGE_URL = "https://example.com/target/url"

LOGIN_URL = credentials.LOGIN_URL
USERNAME = credentials.USERNAME
PASSWORD = credentials.PASSWORD
TARGET_PAGE_URL = credentials.TARGET_PAGE_URL

# Set up the WebDriver
driver = webdriver.Chrome()

try:
    # Navigate to the login page
    driver.get(LOGIN_URL)

    # Log in with username and password
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username"))).send_keys(USERNAME)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "password"))).send_keys(PASSWORD + Keys.RETURN)

    # Wait for the 2FA page to load
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "2fa")))

    # Prompt the user to input the SMS 2FA code manually
    print("An SMS with a 2FA code has been sent to your registered phone number.")
    two_factor_code = input("Please enter the 2FA code received via SMS: ")

    # Input the code into the form and submit
    driver.find_element(By.ID, "2fa").send_keys(two_factor_code + Keys.RETURN)

    # Navigate to the target page after logging in
    WebDriverWait(driver, 10).until(EC.url_contains(LOGIN_URL))
    driver.get(TARGET_PAGE_URL)

    # Locate the submit button
    submit_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "form button[type='submit']")))
    print("Submit button located:", submit_button)

except Exception as e:
    print("An error occurred:", e)

finally:
    time.sleep(5)  # Optional: Wait before closing to observe results
    driver.quit()
