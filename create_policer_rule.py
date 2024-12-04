#!/usr/bin/python3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import credentials
import argparse

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


# Define the file path
file_path = "subnets.txt"

# Read the file and load subnets into a list
try:
    with open(file_path, "r") as file:
        subnets = file.read().splitlines()  # Split by newline
        print("Subnets loaded:", subnets)
except FileNotFoundError:
    print(f"Error: The file {file_path} was not found.")
except Exception as e:
    print(f"An error occurred: {e}")

# HTML template for a new value-row div
value_row_template = """
<div class="row col-12 no-gutters value-row">
    <div class="form-group col-1">
        <button type="button" class="btn btn-outline-danger remove-value" 
            data-toggle="tooltip" data-placement="top" 
            title="" data-original-title="Removes this value">-</button>
    </div>
    <div class="form-group col-11" id="conditions_0_values_{index}_field">
        <input type="text" id="conditions_0_values_{index}" 
            name="conditions[0].values[{index}]" value="{value}" class="form-control">
    </div>
</div>
"""

def define_parser():
    """
    Define the argument parser for the script.
    """
    parser = argparse.ArgumentParser(description="Add destination IPs/subnets and specify a rule type.")
    
    # Add arguments with long and short options
    parser.add_argument(
        "-d", "--destination", 
        type=str, 
        nargs="+", 
        required=True, 
        help="List of destination IPs/subnets to be added (e.g., 192.168.1.0/24 10.0.0.0/8)"
    )
    parser.add_argument(
        "-r", "--rule-type", 
        type=str, 
        required=True, 
        choices=["policer", "accept"], 
        help="Specify the rule type: 'policer' or 'accept'."
    )

    # Parse the arguments
    args = parser.parse_args()

    # Validate the rule type early
    if args.rule_type.lower() not in ["policer", "accept"]:
        print("Error: Invalid rule type! Only 'policer' or 'accept' are allowed.", file=sys.stderr)
        sys.exit(1)

    return args

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
    # Wait for the <h1> element with text "Dashboard" to appear
    # WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, "//h1[text()='Dashboard']")))
    print ("WELCOME SCREEN")
    # WebDriverWait(driver, 10).until(EC.url_contains(LOGIN_URL))
    driver.get(TARGET_PAGE_URL)
    

    # Locate the parent container for the value rows
    parent_container = driver.find_element(By.CSS_SELECTOR, "div.row.values")

    # Log the existing content for verification
    print("Before injection:", driver.execute_script("return arguments[0].innerHTML;", parent_container))

    # Inject new divs for each subnet
    for i, subnet in enumerate(subnets):
        # Generate the HTML for the new row
        new_row_html = value_row_template.format(index=i, value=subnet)
        
        # Inject the new HTML into the parent container
        driver.execute_script("""
            arguments[0].insertAdjacentHTML('beforeend', arguments[1]);
        """, parent_container, new_row_html)

    # Log the modified content for verification
    print("After injection:", driver.execute_script("return arguments[0].innerHTML;", parent_container))

    # Optional: Wait to visually confirm changes in the browser
    import time
    time.sleep(300)

    
    # creation_id = driver.find_element(By.ID, "2fa")

    # Locate the submit button
    submit_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "form button[type='submit']")))
    print("ID:", submit_button)

except Exception as e:
    print("An error occurred:", e)

finally:
    time.sleep(5)  # Optional: Wait before closing to observe results
    driver.quit()

if __name__ == "__main__":
    # Parse command-line arguments
    args = define_parser()

    # Call the function with parsed arguments
    # edit_firewall_rules(args.destination, args.rule_type)