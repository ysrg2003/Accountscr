from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from unidecode import unidecode
import random
import os
import time

# Termux ARM configuration
os.environ['MOZ_HEADLESS'] = '1'
os.environ['SE_SERVICE_LOG_PATH'] = 'null'

class GmailCreator:
    def __init__(self):
        self.first_name = random.choice([
            "Amélie", "Antoine", "Aurélie", "Benoît", "Camille", "Charles",
            "Chloé", "Claire", "Clément", "Dominique", "Élodie", "Émilie"
        ])
        self.last_name = random.choice([
            "Leroy", "Moreau", "Bernard", "Dubois", "Durand", "Lefebvre",
            "Mercier", "Dupont", "Fournier", "Lambert", "Fontaine"
        ])
        self.username = self.generate_username()
        self.driver = self.init_firefox()
        self.password = f"{unidecode(self.first_name)[0].upper()}!{random.randint(1000,9999)}"

    def generate_username(self):
        clean_first = unidecode(self.first_name).lower()
        clean_last = unidecode(self.last_name).lower()
        return f"{clean_first}.{clean_last}{random.randint(100,999)}"

    def init_firefox(self):
        options = FirefoxOptions()
        options.binary_location = "/data/data/com.termux/files/usr/bin/firefox"
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        
        # ARM performance optimizations
        options.set_preference("dom.ipc.processCount", 1)
        options.set_preference("javascript.options.mem.max", 256000000)
        options.set_preference("fission.bfcacheInParent", False)
        
        return webdriver.Firefox(options=options)

    def wait_element(self, locator, timeout=20):
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(locator)
        )

    def create_account(self):
        try:
            # Step 1: Name entry
            self.driver.get("https://accounts.google.com/signup/v2/createaccount")
            self.wait_element((By.NAME, "firstName")).send_keys(self.first_name)
            self.driver.find_element(By.NAME, "lastName").send_keys(self.last_name)
            self.driver.find_element(By.CSS_SELECTOR, "button.VfPpkd-LgbsSe").click()

            # Step 2: Birthday and gender
            self.wait_element((By.ID, "day")).send_keys("15")
            Select(self.driver.find_element(By.ID, "month")).select_by_value("5")
            self.driver.find_element(By.ID, "year").send_keys("1990")
            Select(self.driver.find_element(By.ID, "gender")).select_by_value("1")
            self.driver.find_element(By.CSS_SELECTOR, "button.VfPpkd-LgbsSe").click()

            # Step 3: Username selection
            self.wait_element((By.ID, "selectionc4")).click()
            username_field = self.wait_element((By.NAME, "Username"))
            username_field.clear()
            username_field.send_keys(self.username)
            self.driver.find_element(By.CSS_SELECTOR, "button.VfPpkd-LgbsSe").click()

            # Step 4: Password setup
            self.wait_element((By.NAME, "Passwd")).send_keys(self.password)
            self.driver.find_element(By.NAME, "PasswdAgain").send_keys(self.password)
            self.driver.find_element(By.CSS_SELECTOR, "button.VfPpkd-LgbsSe").click()

            # Step 5: Skip optional steps
            skip_buttons = self.driver.find_elements(By.CSS_SELECTOR, "button.VfPpkd-vQzf8d")
            for btn in skip_buttons:
                try:
                    btn.click()
                    time.sleep(1)
                except:
                    pass

            # Final agreement
            self.wait_element((By.CSS_SELECTOR, "button.VfPpkd-vQzf8d")).click()
            
            print(f"\n✅ Account Created Successfully!\n"
                  f"Email: {self.username}@gmail.com\n"
                  f"Password: {self.password}")

        except Exception as e:
            print(f"\n❌ Creation Failed: {str(e)}")
        finally:
            self.driver.quit()

if __name__ == "__main__":
    GmailCreator().create_account()
