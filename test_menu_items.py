import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture(scope="function")
def driver():
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    drv = webdriver.Chrome(service=service, options=options)
    yield drv
    drv.quit()

def test_menu_items_visible(driver):
    driver.get("https://www.guvi.in/")
    wait = WebDriverWait(driver, 20)

    menu_items = ["Courses", "LIVE Classes", "Practice"]

    for item in menu_items:
        element = wait.until(
            EC.visibility_of_element_located((By.LINK_TEXT, item))
        )
        assert element.is_displayed(), f" Menu item '{item}' not visible"
        print(f" Menu item '{item}' is visible and accessible.")
