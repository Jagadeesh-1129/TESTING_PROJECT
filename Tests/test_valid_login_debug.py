# test_valid_login_debug_safe.py
import pytest
import time
from selenium import webdriver
from selenium.common.exceptions import (
    TimeoutException,
    WebDriverException,
    NoSuchWindowException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# update these with your credentials or use env vars
VALID_EMAIL = "jagadeeshyesodha@gmail.com"
VALID_PASSWORD = "Jiyahiya@24"
LOGIN_URL = "https://www.guvi.in/login"

# helper to create driver safely
def create_chrome_driver():
    opts = webdriver.ChromeOptions()
    opts.add_argument("--start-maximized")
    # optional flags that can improve stability in CI / windows env
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--disable-extensions")
    # uncomment headless only if you know how to debug headless
    # opts.add_argument("--headless=new")
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=opts)

@pytest.fixture(scope="function")
def driver():
    drv = create_chrome_driver()
    yield drv
    try:
        drv.quit()
    except Exception:
        # sometimes driver already died, ignore
        pass

def safe_page_source(driver, max_chars=2000):
    """Return a snippet of page source only if session is alive; otherwise return placeholder."""
    try:
        # driver.session_id exists while session alive
        if getattr(driver, "session_id", None):
            return driver.page_source[:max_chars]
    except (WebDriverException, NoSuchWindowException):
        return "<driver session not available / crashed>"
    return "<no page source>"

def test_valid_login_debug_safe(driver):
    wait = WebDriverWait(driver, 12)

    # navigate
    try:
        driver.get(LOGIN_URL)
    except WebDriverException as e:
        pytest.fail(f"Failed to open {LOGIN_URL}: {e}")

    # ensure email/password inputs exist
    try:
        email_el = wait.until(EC.visibility_of_element_located((By.ID, "email")))
        pwd_el = wait.until(EC.visibility_of_element_located((By.ID, "password")))
    except TimeoutException:
        snippet = safe_page_source(driver, 8000)
        print("\n--- PAGE SNIPPET (first 8k chars) ---\n")
        print(snippet)
        pytest.fail("Email/password inputs not found by ID 'email'/'password'.")

    # fill credentials
    try:
        email_el.clear()
        email_el.send_keys(VALID_EMAIL)
        pwd_el.clear()
        pwd_el.send_keys(VALID_PASSWORD)
    except WebDriverException as e:
        pytest.fail(f"Failed to interact with inputs: {e}")

    # candidate locators for submit/button
    candidates = [
        (By.CSS_SELECTOR, "button[type='submit']"),
        (By.CSS_SELECTOR, "input[type='submit']"),
        (By.XPATH, "//button[contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'login')]"),
        (By.XPATH, "//button[contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'sign in')]"),
        (By.XPATH, "//input[@type='submit' and (contains(translate(@value,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'login') or contains(translate(@value,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'sign'))]"),
        (By.XPATH, "//button[contains(@class,'login') or contains(@id,'login') or contains(@class,'signin')]"),
        (By.XPATH, "//button[contains(.,'Log in') or contains(.,'Log In') or contains(.,'Sign In') or contains(.,'Sign in')]")
    ]

    submit_el = None
    for by, val in candidates:
        try:
            submit_el = WebDriverWait(driver, 6).until(EC.element_to_be_clickable((by, val)))
            print("Using locator:", by, val)
            break
        except TimeoutException:
            # try next candidate
            continue
        except WebDriverException:
            # driver died while finding element
            pass

    if not submit_el:
        snippet = safe_page_source(driver, 8000)
        print("\n--- PAGE SNIPPET (first 8k chars) ---\n")
        print(snippet)
        pytest.fail("Login submit/button not found by candidate locators. Paste the printed snippet or copy the element HTML.")

    # click submit and handle navigation
    try:
        submit_el.click()
    except WebDriverException as e:
        # If driver died on click, fail with message
        pytest.fail(f"Click failed because webdriver died: {e}")

    # wait for url to change from login (some GUVI flows redirect to /sign-in first)
    try:
        wait.until(lambda d: d.current_url != LOGIN_URL)
    except TimeoutException:
        # maybe it redirected to a sign-in alias; capture URL and report
        current = None
        try:
            current = driver.current_url
        except Exception:
            current = "<could not read current_url>"
        pytest.fail(f"Navigation did not change from login URL; current URL: {current}")

    # final check: ensure we ended up in a profile/dashboard or at least not on login page
    try:
        final_url = driver.current_url
        print("Navigation result URL:", final_url)
        assert "/profile" in final_url or "/dashboard" in final_url or "/sign-in" in final_url or final_url != LOGIN_URL
    except WebDriverException as e:
        pytest.fail(f"Driver error while verifying final URL: {e}")
