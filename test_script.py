# Save this as test_my_script.py

import json
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pytest

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

def test_table_data(driver):
    url = "https://testpages.herokuapp.com/styled/tag/dynamic-table.html"
    driver.get(url)

    element = driver.find_element(By.XPATH, "//details/summary")
    element.click()

    data = [{"name": "Bob", "age": 20, "gender": "male"},
            {"name": "George", "age": 42, "gender": "male"},
            {"name": "Sara", "age": 42, "gender": "female"}]

    data_string = json.dumps(data)

    input_text_box = "//textarea[@id='jsondata']"
    input_element = driver.find_element(By.XPATH, input_text_box)
    input_element.clear()
    time.sleep(2)
    input_element.send_keys(data_string)
    time.sleep(2)

    refresh_table = "#refreshtable"
    refresh_table_element = driver.find_element(By.CSS_SELECTOR, refresh_table)
    refresh_table_element.click()
    time.sleep(3)

    mock_dict = {}
    l1 = []

    for i in range(1, 4):
        name = f"//*[@id='dynamictable']/tr[{i + 1}]/td[1]"
        age = f"//*[@id='dynamictable']/tr[{i + 1}]/td[2]"
        gender = f"//*[@id='dynamictable']/tr[{i + 1}]/td[3]"
        name_1 = driver.find_element(By.XPATH, name).text
        age_1 = driver.find_element(By.XPATH, age).text
        gender_1 = driver.find_element(By.XPATH, gender).text
        mock_dict["name"] = name_1
        mock_dict["age"] = int(age_1)
        mock_dict["gender"] = gender_1
        l1.append(mock_dict)
        mock_dict = {}

    # Convert lists to JSON strings
    data_str = json.dumps(data, sort_keys=True)
    l1_str = json.dumps(l1, sort_keys=True)

    # Assert that the string representations are the same
    assert data_str == l1_str
