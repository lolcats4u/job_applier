import bs4
import csv
import getpass
import keyring
import os
from playwright.sync_api import sync_playwright
import requests
import typer

app = typer.Typer()
def main():
    job_file = File().load()

class File():
    def __init__(self, file_name):
        self.file_name = file_name
        self.contents = self.read_file(self.file_name)

    def read_file(self):
        with open( self.file_name , "r", encoding="utf-8") as file:
            csv_reader = csv.DictReader(file)
            self.contents = list(csv_reader)

class Job():
    def __init__(self):
        pass
    def save_job():
        pass

    def duplicate():
        pass

    def applied():
        pass

def load_accounts(name:str=None):
    """format:
      name, email, url, check_login_page
      """
    info = File("./account_info.csv").contents
    accounts = {}
    for account in info:
        if not name:
            accounts[account[0]] = Account(account[0], account[1], account[2], account[3])
        else:
            if name in account:
                accounts[account[0]] = Account(account[0], account[1], account[2], account[3])
    return accounts

class Account:
    def __init__(self,name, email, url, check_login_page):
        self.name = name
        self.email = email
        self.url = url
        self.credentials = self.Credentials(name).read()
        self.session = self.LoginSession(self.credentials, check_login_page)

    class Credentials():
        def __init__(self, name):
            self.name = name
            
        def get_credential(self):
            try:
                self.read()
            except KeyError:
                self.write("email")
                self.write("password")

        def read(self):
            self.email = keyring.get_password(self.name, "email")
            self.passwd = keyring.get_credential(self.name, "password")
        
        def write(self,key):
            value = getpass.getpass(f"Enter {key}:")
            save = input(f"Save {key} to keychain? (y/n): ")
            if save.lower() == "y":
                keyring.set_password(self.name, key, value)
            return value
    
    class LoginSession():
        def __init__(self, creds:Credentials, goto):
            self.credentials = creds
            self.goto = goto

        def expired(self):
            profile_access_page = page.goto(self.goto)
            with sync_playwright() as p:
                browser, page = get_page(p)
                if "feed" not in profile_access_page:
                    self.new_session(self.credentials.name)

        def new_session(self):
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=False)
                context = browser.new_context(storage_state=f"./sessions/{self.credentials.name}_session.json") if False else browser.new_context()
                page = context.new_page()

                page.goto("https://www.linkedin.com/login")
                page.fill("#username", self.credenials.email)
                page.fill("#password", self.credentials.password)
                page.click("[type=submit]")
                page.wait_for_load_state("networkidle")

                # Save session cookies/storage to disk
                context.storage_state(path=f"./sessions/{self.credentials.name}_session.json")
                browser.close()

if __name__ == "__main__":
    main()