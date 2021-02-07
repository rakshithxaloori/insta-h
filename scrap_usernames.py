from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import selenium.common.exceptions
import time
import itertools
from explicit import waiter, XPATH
import os
import json
import sys


def login(chrome, username, password):
    chrome.get("https://www.instagram.com/")
    time.sleep(4)

    usern = chrome.find_element_by_name("username")
    usern.send_keys(username)

    passw = chrome.find_element_by_name("password")
    passw.send_keys(password)

    passw.send_keys(Keys.RETURN)
    time.sleep(5.5)


def scrap_usernames(chrome):
    chrome.get("https://www.instagram.com/" + page + "/")
    time.sleep(4)

    # Click on a tag
    followers_a_tag = chrome.find_element_by_partial_link_text("follower")
    followers_a_tag.click()

    # Get the followers list
    waiter.find_element(chrome, "//div[@role='dialog']", by=XPATH)
    follower_count = 1000
    # Taking advange of CSS's nth-child functionality
    follower_css = "ul div li:nth-child({}) a.notranslate"
    for group in itertools.count(start=1, step=12):
        for follower_index in range(group, group + 12):
            if follower_index > follower_count:
                raise StopIteration
            yield waiter.find_element(chrome, follower_css.format(follower_index)).text

        last_follower = waiter.find_element(
            chrome, follower_css.format(group + 11))
        time.sleep(1)
        chrome.execute_script("arguments[0].scrollIntoView();", last_follower)


def create_json_file(chrome, followers_count, dir_path):
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)

    follower_list = list()
    for count, follower in enumerate(scrap_usernames(chrome), 1):
        # print("\t{:>3}: {}".format(count, follower))
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


if __name__ == "__main__":
    if (len(sys.argv) != 6):
        sys.exit(
            "Usage: python3 scrap_usernames.py username password page_username follower_group_size output_dir_path")

    username = sys.argv[1]
    password = sys.argv[2]
    url = 'https://instagram.com/'
    page = sys.argv[3]
    follower_count = int(sys.argv[4])
    output_dir_path = sys.argv[5]

    chrome = webdriver.Chrome()

    login(chrome, username, password)
    create_json_file(chrome, follower_count, output_dir_path)
    chrome.close()
