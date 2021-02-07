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


def login(chrome, username, password):
    chrome.get("https://www.instagram.com/")
    time.sleep(4)

    usern = chrome.find_element_by_name("username")
    usern.send_keys(username)

    passw = chrome.find_element_by_name("password")
    passw.send_keys(password)

    passw.send_keys(Keys.RETURN)
    time.sleep(5.5)


def scrap_usernames(chrome, total_followers_count):
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
                raise StopIteration
            element = WebDriverWait(chrome, 100).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, follower_css.format(follower_index)))
            )
            # yield waiter.find_element(chrome, follower_css.format(follower_index)).text
            yield element.text

        last_follower = waiter.find_element(
            chrome, follower_css.format(group + 11))
        chrome.execute_script("arguments[0].scrollIntoView();", last_follower)


def create_json_file(chrome, total_followers_count, followers_count, dir_path):
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)

    follower_list = list()
    for count, follower in enumerate(scrap_usernames(chrome, total_followers_count), 1):
        print("\t{:>3}: {}".format(count, follower))
        follower_list.append(follower)
        if (count % followers_count) == 0:
            # Create the file
            print(os.path.join(dir_path, 'P_' +
                               str(int(count / followers_count)) + ".json"))
            with open(os.path.join(dir_path, 'P_' + str(int(count / followers_count)) + ".json"), 'w') as json_file:
                json.dump(
                    {"status": "P", "followers_list": follower_list, "follower_count": followers_count}, json_file, indent=4)
            # Refresh the follower list
            follower_list.clear()
            time.sleep(5)


if __name__ == "__main__":
    if (len(sys.argv) != 7):
        sys.exit(
            "Usage: python3 scrap_usernames.py username password page_username total_followers_count follower_group_size output_dir_path")

    username = sys.argv[1]
    password = sys.argv[2]
    url = 'https://instagram.com/'
    page = sys.argv[3]
    total_followers_count = int(sys.argv[4])
    follower_count = int(sys.argv[5])
    output_dir_path = sys.argv[6]

    chrome = webdriver.Chrome()

    login(chrome, username, password)
    create_json_file(
        chrome, total_followers_count, follower_count, output_dir_path)
    chrome.close()
