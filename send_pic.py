import sys
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import selenium.common.exceptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from explicit import waiter, XPATH

from scrap_usernames import login
from connect_db import DatabaseOperations


def go_to_dms(chrome):
    chrome.get("https://www.instagram.com/direct/inbox/")
    time.sleep(4)

    waiter.find_element(chrome, "//div[@role='dialog']", by=XPATH)
    notk_button = chrome.find_element_by_xpath(
        "//button[contains(@class, 'aOOlW   HoLwm')]")
    notk_button.click()
    time.sleep(4)


def send_pic(chrome, new_database_connection, username):
    # Click on Write Message
    write_msg_button = chrome.find_element_by_xpath(
        "//button[contains(@class, 'wpO6b ZQScA')]")
    write_msg_button.click()

    waiter.find_element(chrome, "//div[@role='dialog']", by=XPATH)
    time.sleep(3)

    search_box = chrome.find_element_by_xpath("//input[@name='queryBox']")
    search_box.send_keys(username)

    select_toggle = WebDriverWait(chrome, 100).until(
        EC.presence_of_element_located(
            (By.XPATH, "//button[@class='dCJp8 ']"))
    )

    select_toggle.click()
    time.sleep(2)

    next_button = chrome.find_element_by_xpath(
        "//button[contains(@class, 'sqdOP yWX7d    y3zKF   cB_4K')]")
    next_button.click()
    time.sleep(2)

    # Wait until the username pops up in the char list
    # try:
    #     chat_username = WebDriverWait(chrome, 100).until(
    #         EC.presence_of_element_located(
    #             By.XPATH, "//div[contains(@class, '_7UhW9   xLCgt      MMzan  KV-D4              fDxYl') and ./text()={}]".format(username)
    #         )
    #     )
    #     time.sleep(1)
    # except Exception as e:
    #     print(e)
    #     return False

    # a_clickable = chrome.find_element_by_class_name("-qQT3 rOtsg")
    # a_clickable.click()

    # Send pic
    img_input = chrome.find_element_by_class_name("tb_sK")
    img_input.send_keys("/home/rakshith/proeliumx/instagram-h/wp1874041-boku-no-hero-wallpapers.png")
    time.sleep(100)

    return True


if __name__ == "__main__":
    if (len(sys.argv) != 3):
        sys.exit("Usage: python3 send_pic.py username password")

    username = sys.argv[1]
    password = sys.argv[2]

    chrome = webdriver.Chrome()
    new_database_connection = DatabaseOperations()

    login(chrome, username, password)
    go_to_dms(chrome)
    # Get 100 usernames with P status
    while True:
        status = send_pic(chrome, new_database_connection, "hello")
        update_status(new_database_connection, username, status)
    chrome.close()
