from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# 1. Launch Browser
driver = webdriver.Chrome()
driver.maximize_window()

# 2. Open GUVI homepage
driver.get("https://www.guvi.in/")

# 3. Wait for Login button to be present
wait = WebDriverWait(driver, 10)
login_button = wait.until(EC.presence_of_element_located((By.XPATH, "//a[@id='login-btn']")))

# 4. Check if button is visible
if login_button.is_displayed():
    print("Login button is visible")
else:
    print("Login button is not visible")

# 5. Check if button is clickable
clickable_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@id='login-btn']")))
print("Login button is clickable")

# 6. Click the Login button
clickable_button.click()
time.sleep(3)

# 7. Verify navigation to Login page
expected_url = "https://www.guvi.in/login"
if driver.current_url.startswith(expected_url):
    print("Navigation successful: Reached Login page")
else:
    print(f"Navigation failed. Current URL: {driver.current_url}")

driver.quit()
