import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def find_signup(wait):
    """Try a list of robust locators for the Sign-Up / Register link/button."""
    candidates = [
        (By.LINK_TEXT, "Sign Up"),
        (By.LINK_TEXT, "Sign up"),
        (By.PARTIAL_LINK_TEXT, "Sign"),
        (By.XPATH, "//a[contains(@href,'/register') and (contains(normalize-space(.),'Sign') or contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'register'))]"),
        (By.CSS_SELECTOR, "a[href*='/register']"),
        (By.XPATH, "//button[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'sign')]"),
    ]
    for by, val in candidates:
        try:
            el = wait.until(EC.visibility_of_element_located((by, val)))
            el_clickable = wait.until(EC.element_to_be_clickable((by, val)))
            return el_clickable
        except Exception:
            continue
    return None

@pytest.fixture(scope="function")
def driver():
    service = Service(ChromeDriverManager().install())
    opts = webdriver.ChromeOptions()
    opts.add_argument("--start-maximized")
    opts.add_argument("--disable-extensions")
    drv = webdriver.Chrome(service=service, options=opts)
    yield drv
    drv.quit()

def test_signup_redirects_to_register(driver):
    driver.get("https://www.guvi.in/")
    wait = WebDriverWait(driver, 12)

    # find the signup element (tries multiple strategies)
    signup = find_signup(wait)
    if not signup:
        snippet = driver.page_source[:8000]
        print("\n--- PAGE SNIPPET (first 8k chars) ---\n")
        print(snippet)
        pytest.fail("Sign-Up element not found by candidate locators. See printed page snippet.")

    # click and wait for navigation
    signup.click()

    # wait until URL changes away from the homepage (or until register appears)
    wait.until(lambda d: d.current_url != "https://www.guvi.in/")

    # final assertion
    assert driver.current_url.startswith("https://www.guvi.in/register"), (
        f"Expected URL to start with https://www.guvi.in/register but got: {driver.current_url}"
    )
