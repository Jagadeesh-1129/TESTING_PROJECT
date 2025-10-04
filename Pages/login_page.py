import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By

URL = "https://www.guvi.in/"

@pytest.mark.smoke
def test_url_loads():
    """Verify whether the GUVI URL is valid and loads successfully."""
    driver = webdriver.Chrome()
    driver.get(URL)

    # Assert title or some unique element
    assert "GUVI" in driver.title, "Page title does not contain 'GUVI'!"

    driver.quit()
