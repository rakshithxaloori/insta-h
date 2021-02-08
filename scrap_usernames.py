import time
import itertools
import os
import json
import sys

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import selenium.common.exceptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from explicit import waiter, XPATH

from connect_db import DatabaseOperations


def login(chrome, username, password):
    chrome.get("https://www.instagram.com/")
    time.sleep(4)

    usern = chrome.find_element_by_name("username")
    usern.send_keys(username)

    passw = chrome.find_element_by_name("password")
    passw.send_keys(password)

    passw.send_keys(Keys.RETURN)
    time.sleep(5.5)


def scrap_usernames(chrome, new_database_connection, total_followers_count):
    chrome.get("https://www.instagram.com/" + page + "/")
    time.sleep(4)

    # Click on a tag
    followers_a_tag = chrome.find_element_by_partial_link_text("follower")
    followers_a_tag.click()

    # Get the followers list
    waiter.find_element(chrome, "//div[@role='dialog']", by=XPATH)
    # Taking advange of CSS's nth-child functionality
    follower_css = "ul div li:nth-child({}) a.notranslate"
    for group in itertools.count(start=1, step=12):
        for follower_index in range(group, group + 12):
            if follower_index > total_followers_count:
                return True
            try:
                element = WebDriverWait(chrome, 100).until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, follower_css.format(follower_index)))
                )
                # yield waiter.find_element(chrome, follower_css.format(follower_index)).text
                new_database_connection.add_to_database(element.text)
            except Exception as e:
                print("e")
                return False

        last_follower = waiter.find_element(
            chrome, follower_css.format(group + 11))
        chrome.execute_script("arguments[0].scrollIntoView();", last_follower)


if __name__ == "__main__":
   if (len(sys.argv) != 5):
        sys.exit(
            "Usage: python3 scrap_usernames.py username password page_username total_followers_count")

    username = sys.argv[1]
    password = sys.argv[2]
    url = 'https://instagram.com/'
    page = sys.argv[3]
    total_followers_count = int(sys.argv[4])

    chrome = webdriver.Chrome()
    new_database_connection = DatabaseOperations()

    login(chrome, username, password)
    call_scrap_usernames = scrap_usernames(
        chrome, new_database_connection, total_followers_count)

    while not call_scrap_usernames:
        chrome.close()
        chrome = webdriver.Chrome()
        login(chrome, username, password)
        new_database_connection.close_connection()
        new_database_connection = DatabaseOperations()

        call_scrap_usernames = scrap_usernames(
            chrome, new_database_connection, total_followers_count)

    chrome.close()
    new_database_connection.close_connection()
