import os, sys
import pytest
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select

from django.contrib.auth import authenticate
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ['DJANGO_SETTINGS_MODULE'] = 'ETIToDoList.todolist.settings'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ETIToDoList.todolist.settings")
import django
django.setup()

def test_login_without_entering_username_or_password():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get('http://localhost:8000')
    time.sleep(1)
    button = driver.find_element_by_tag_name('a')
    button.click()
    button = driver.find_element_by_xpath("//button")
    button.click()
    time.sleep(1)
    assert driver.find_element_by_css_selector("input:invalid")
    driver.quit()
    
def test_login_without_entering_username():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get('http://localhost:8000')
    time.sleep(1)
    button = driver.find_element_by_tag_name('a')
    button.click()

    time.sleep(1)
    password = driver.find_element_by_id('id_password')
    password.send_keys("admin123")
    button = driver.find_element_by_xpath("//button")
    button.click()
    assert driver.find_element_by_css_selector("input:invalid")
    driver.quit()

def test_login_without_entering_password():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get('http://localhost:8000')
    time.sleep(1)
    button = driver.find_element_by_tag_name('a')
    button.click()

    time.sleep(1)
    username = 'admin'
    driver.find_element_by_id('id_username').send_keys(username)
    button = driver.find_element_by_xpath("//button")
    button.click()
    time.sleep(2)
    assert driver.find_element_by_css_selector("input:invalid")
    driver.quit()

def test_login_with_incorrect_username():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get('http://localhost:8000')
    time.sleep(1)
    button = driver.find_element_by_tag_name('a')
    button.click()

    time.sleep(1)
    username = 'admin?'
    driver.find_element_by_id('id_username').send_keys(username)
    password = driver.find_element_by_id('id_password')
    password.send_keys("admin123")
    button = driver.find_element_by_xpath("//button")
    button.click()
    time.sleep(2)
    assert "The username or password you have entered is incorrect, please try again." in driver.page_source
    driver.quit()

def test_login_with_incorrect_password():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get('http://localhost:8000')
    time.sleep(1)
    button = driver.find_element_by_tag_name('a')
    button.click()

    time.sleep(1)
    username = 'admin'
    driver.find_element_by_id('id_username').send_keys(username)
    password = driver.find_element_by_id('id_password')
    password.send_keys("admin123?")
    button = driver.find_element_by_xpath("//button")
    button.click()
    time.sleep(2)
    assert "The username or password you have entered is incorrect, please try again." in driver.page_source
    driver.quit()

def test_successful_login():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get('http://localhost:8000')
    time.sleep(1)
    button = driver.find_element_by_tag_name('a')
    button.click()

    time.sleep(2)
    username = 'admin'
    driver.find_element_by_id('id_username').send_keys(username)
    password = driver.find_element_by_id('id_password')
    password.send_keys("admin123")
    button = driver.find_element_by_xpath("//button")
    button.click()
    time.sleep(2)
    assert "Our Todo List" in driver.page_source
    driver.quit()
    
def test_navigation_to_login_page():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get('http://localhost:8000')
    assert "You are not logged in." in driver.page_source

    time.sleep(2)
    button = driver.find_element_by_tag_name('a')
    button.click()
    time.sleep(2)
    assert "Login" in driver.page_source
    driver.quit()

def test_logout():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get('http://localhost:8000')
    time.sleep(1)
    button = driver.find_element_by_tag_name('a')
    button.click()

    time.sleep(2)
    username = 'admin'
    driver.find_element_by_id('id_username').send_keys(username)
    password = driver.find_element_by_id('id_password')
    password.send_keys("admin123")
    button = driver.find_element_by_xpath("//button")
    button.click()
    
    logout = driver.find_element_by_xpath("//a[contains(text(), 'Log Out')]")
    logout.click()
    time.sleep(2)
    assert "You are not logged in." in driver.page_source
    driver.quit()

@pytest.mark.django_db
def test_successful_login_pytest():
    user = authenticate(username="admin", password='admin123')
    assert user != None

@pytest.mark.django_db
def test_login_with_incorrect_username_pytest():
    user = authenticate(username="admin?", password='admin123')
    assert user == None

@pytest.mark.django_db
def test_login_with_incorrect_password_pytest():
    user = authenticate(username="admin", password='admin123?')
    assert user == None
