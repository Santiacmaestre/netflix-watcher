"""Module providing confirmation for Netflix Household update"""
import imaplib
import email
import re
import time
import os
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

EMAIL_IMAP = os.environ['EMAIL_IMAP']
EMAIL_LOGIN = os.environ['EMAIL_LOGIN']
EMAIL_PASSWORD = os.environ['EMAIL_PASSWORD']
NETFLIX_EMAIL_SENDER = os.environ['NETFLIX_EMAIL_SENDER']


def extract_links(text):
    """Finds all https links"""
    url_pattern = r'https?://\S+'
    urls = re.findall(url_pattern, text)
    return urls

def open_link_with_selenium(body):
    """Opens Selenium and clicks a button to confirm connection"""
    print("Extracting links from email body...")
    links = extract_links(body)

    for link in links:
        print(f"Found link: {link}")
        if "update-primary-location" in link:
            print(f"Target confirmation link detected: {link}")
            options = webdriver.ChromeOptions()
            options.add_argument("--headless")

            print("Connecting to remote Selenium server...")
            driver = webdriver.Remote(
                command_executor='http://netflix_watcher_selenium:4444/wd/hub',
                options=options
            )

            print("Navigating to confirmation link...")
            driver.get(link)
            time.sleep(3)  # Give the page time to load

            try:
                print("Waiting for confirmation button to be clickable...")
                element = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((
                        By.CSS_SELECTOR, '[data-uia="set-primary-location-action"]'
                    ))
                )
                print("Clicking the confirmation button...")
                element.click()
                print("Confirmation button clicked successfully.")
            except TimeoutException as exception:
                print("Error: Timed out waiting for confirmation button.", exception)

            time.sleep(3)
            print("Closing Selenium browser.")
            driver.quit()
        else:
            print("This link does not match the confirmation URL pattern.")

def fetch_last_unseen_email():
    """Gets body of last unseen mail from inbox"""
    mail = imaplib.IMAP4_SSL(EMAIL_IMAP)
    mail.login(EMAIL_LOGIN, EMAIL_PASSWORD)
    mail.select("inbox")

    _, email_ids = mail.search(None, '(UNSEEN FROM ' + NETFLIX_EMAIL_SENDER + ')')
    email_ids = email_ids[0].split()

    if email_ids:
        email_id = email_ids[-1]
        _, msg_data = mail.fetch(email_id, "(RFC822)")
        msg = email.message_from_bytes(msg_data[0][1])

        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                if "text/plain" in content_type:
                    body = part.get_payload(decode=True).decode()
                    open_link_with_selenium(body)
        else:
            body = msg.get_payload(decode=True).decode()
            open_link_with_selenium(body)

    mail.logout()


if __name__ == "__main__":
    print("Watcher started...")
    while True:
        try:
            fetch_last_unseen_email()
        except Exception as e:
            print("Unhandled error:", e)
        time.sleep(10)

