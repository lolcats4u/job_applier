
import getpass
import keyring
from playwright.sync_api import sync_playwright
from file_handlers import File

class Account:
    def __init__(self,name, email=None, url=None, check_login_page=None):
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
        
        def write(self,key,file_handler):
            value = getpass.getpass(f"Enter {key}:")
            save = input(f"Save {key} to keychain? (y/n): ")
            if save.lower() == "y":
                keyring.set_password(self.name, key, value)
            print("Save this board with a name, email, url, and login page\n")
            email = None
            name = None
            url = None
            login_page = None
            write_info = input(f"email:{email}, name:{name}, url:{url}, login_page:{login_page}\n")
            file_handler.write_row(f"{name}, {email}, {url}, {login_page}")
            print(f"Wrote {name}, {email}, {url}, {login_page} to {file_handler.file_name}")
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
                    self.new_session()

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

def load_account(name):
    """format:
      name, email, url, check_login_page
      """
    accounts = {}
    loaded_account_file = File("./account_info.csv")
    account = Account(name)
    for account_info in loaded_account_file:
        if account.name in account_info:
            account.email = account_info[1]
            account.url = account_info[2]
            account.login_page = account_info[3]
    return loaded_account_file, account
    


