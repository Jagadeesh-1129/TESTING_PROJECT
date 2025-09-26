from selenium import webdriver
import time

# 1. Launch Browser
driver = webdriver.Chrome()
driver.maximize_window()

# 2. Open GUVI website
driver.get("https://www.guvi.in/")
time.sleep(3)

# 3. Get the actual title of the page
actual_title = driver.title
print("Page Title:", "GUVI|HCL")
time.sleep(5)

# 4. Expected title
expected_title = "GUVI | Learn to code in your native language"

# 5. Assertion
if actual_title == expected_title:
    print("Test Case 2 Passed: Title is correct")
else:
    print("Test Case 2 Failed: Expected:", expected_title, "but got:", actual_title)

# 6. Close Browser
driver.quit()
