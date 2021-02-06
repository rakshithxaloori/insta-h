from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import selenium.common.exceptions
import time
import random
import itertools
from explicit import waiter, XPATH


# Login Credentials
username = "uchiha.leo.06@gmail.com"
password = "q3w2e1r4t5"
url = 'https://instagram.com/'
# page = input("Enter the instagram page username: ")
page = "indiaofficialfreefire"

chrome = webdriver.Chrome()


def url_name(url):
    chrome.get(url)
    time.sleep(4)


def login(username, your_password):
    usern = chrome.find_element_by_name("username")
    usern.send_keys(username)

    passw = chrome.find_element_by_name("password")
    passw.send_keys(your_password)

    passw.send_keys(Keys.RETURN)
    time.sleep(5.5)


def send_message():
    chrome.get(url + page + "/")
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
            chrome, follower_css.format(group+11))
        chrome.execute_script("arguments[0].scrollIntoView();", last_follower)


url_name(url)
login(username, password)
for count, follower in enumerate(send_message(), 1):
    print("\t{:>3}: {}".format(count, follower))
chrome.close()
