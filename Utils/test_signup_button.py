import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def find_signup_locator(wait):
    candidates = [
        (By.LINK_TEXT, "Sign Up"),
        (By.LINK_TEXT, "Sign up"),
        (By.PARTIAL_LINK_TEXT, "Sign"),
        (By.XPATH,
         "//a[contains(@href,'/register') and (contains(normalize-space(.),'Sign') or contains(normalize-space(.),'Register'))]"),
        (By.XPATH, "//a[contains(@href,'/register')]"),
        (By.CSS_SELECTOR, "a[href*='/register']"),
        (By.XPATH, "//button[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'sign')]")
    ]
    for by, val in candidates:
        try:
            el = wait.until(EC.visibility_of_element_located((by, val)))
            # ensure clickable too
            el_clickable = wait.until(EC.element_to_be_clickable((by, val)))
            return el_clickable
        except Exception:
            continue
    return None


@pytest.fixture(scope="function")
def driver():
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    drv = webdriver.Chrome(service=service, options=options)
    yield drv
    drv.quit()


def test_signup_button_navigation(driver):
    driver.get("https://www.guvi.in/")
    wait = WebDriverWait(driver, 12)

    # debug: optionally print small snippet if locator fails
    signup = find_signup_locator(wait)
    if not signup:
        # helpful debug output — comment out in final version
        page_snippet = driver.page_source[:8000]
        print("\n--- PAGE SNIPPET (first 8k chars) ---\n")
        print(page_snippet)
        pytest.fail("Sign-Up element not found by any candidate locator. See printed page snippet.")

    # we found it: click and verify
    signup.click()
    wait.until(lambda d: d.current_url != "https://www.guvi.in/")  # wait for navigation
    assert driver.current_url.startswith(
        "https://www.guvi.in/register"), f"Expected /register URL but got: {driver.current_url}"
