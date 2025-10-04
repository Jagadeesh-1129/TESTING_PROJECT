import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Invalid credentials for testing
INVALID_EMAIL = "wrong_user@example.com"
INVALID_PASSWORD = "wrongpassword123"

@pytest.fixture(scope="function")
def driver():
    service = Service(ChromeDriverManager().install())
    opts = webdriver.ChromeOptions()
    opts.add_argument("--start-maximized")
    drv = webdriver.Chrome(service=service, options=opts)
    yield drv
    drv.quit()

def test_invalid_login(driver):
    driver.get("https://www.guvi.in/login")
    wait = WebDriverWait(driver, 12)

    # 1. Enter invalid email
    email_input = wait.until(EC.visibility_of_element_located((By.ID, "email")))
    email_input.clear()
    email_input.send_keys(INVALID_EMAIL)

    # 2. Enter invalid password
    password_input = wait.until(EC.visibility_of_element_located((By.ID, "password")))
    password_input.clear()
    password_input.send_keys(INVALID_PASSWORD)

    # 3. Click Login button
    login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Login')]")))
    login_button.click()

    # 4. Wait for error message
    try:
        error_message = wait.until(
            EC.visibility_of_element_located((By.XPATH, "//*[contains(text(),'Invalid') or contains(text(),'incorrect') or contains(text(),'failed')]"))
        )
        assert error_message.is_displayed()
        print("Test Case 7 Passed: Invalid login shows error message")
    except Exception:
        # fallback check: still on login page
        assert driver.current_url == "https://www.guvi.in/login", \
            f"Expected to remain on login page, but got {driver.current_url}"
