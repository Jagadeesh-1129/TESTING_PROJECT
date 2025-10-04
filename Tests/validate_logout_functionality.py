# test_logout.py
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

VALID_EMAIL = "jagadeeshyesodha@gmail.com"
VALID_PASSWORD = "Jiyahiya@24"

@pytest.fixture(scope="function")
def driver():
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    drv = webdriver.Chrome(service=service, options=options)
    yield drv
    drv.quit()

def test_logout(driver):
    driver.get("https://www.guvi.in/login")
    wait = WebDriverWait(driver, 20)

    #  Login process
    email_input = wait.until(EC.visibility_of_element_located((By.ID, "email")))
    email_input.send_keys("jagadeeshyesodha@gmail.com")

    password_input = wait.until(EC.visibility_of_element_located((By.ID, "password")))
    password_input.send_keys("Jiyahiya@24")

    login_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'class=btn signup-btn)]"))
    )
    login_button.click()

    #  Wait until redirected to profile/dashboard
    wait.until(EC.url_contains("/profile"))

    #  Open profile dropdown (locator may vary; adjust if needed)
    profile_icon = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "img.user-img"))
    )
    profile_icon.click()

    #  Click logout (Logout is usually an <a> link, not button)
    logout_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),Sign Out)]"))
    )
    logout_button.click()

    #  Verify user is redirected to login page
    wait.until(EC.url_contains("login"))
    assert "login" in driver.current_url
    print(" Logout successful and user redirected.")
