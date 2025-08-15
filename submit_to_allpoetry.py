from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# --- User credentials ---
USERNAME = "your_username"
PASSWORD = "your_password"

# --- ChromeDriver path ---
CHROMEDRIVER_PATH = r"C:\path\to\chromedriver"

# --- Read poems from file ---
poems = []
with open("poems.txt", "r", encoding="utf-8") as f:
    lines = f.read().split("\n\n")  # split by blank line
    for chunk in lines:
        parts = chunk.strip().split("\n", 1)  # title + body
        if len(parts) == 2:
            poems.append({"title": parts[0], "body": parts[1]})

print(f"Loaded {len(poems)} poems from file.\n")

# --- Chrome options ---
options = Options()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--disable-extensions")
options.add_argument("--disable-infobars")
options.add_argument("--profile-directory=Default")
options.add_argument("--headless")  # Uncomment to run headless

driver = webdriver.Chrome(service=webdriver.chrome.service.Service(CHROMEDRIVER_PATH), options=options)
wait = WebDriverWait(driver, 15)

try:
    # --- Navigate to login page ---
    driver.get("https://www.allpoetry.com/login")
    print("Navigated to login page.")

    # --- Wait for username and password fields ---
    try:
        username_elem = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="user_name"]')))
        password_elem = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="user_password"]')))
    except:
        print("Could not find login fields.")
        driver.quit()
        exit()

    # --- Fill login form ---
    username_elem.clear()
    username_elem.send_keys(USERNAME)
    password_elem.clear()
    password_elem.send_keys(PASSWORD)

    # --- Click login ---
    try:
        login_btn = wait.until(EC.element_to_be_clickable(
            (By.XPATH, '/html/body/div[1]/div/div[2]/form/div[4]/div[2]/input')))
        login_btn.click()
        print("Clicked login button. Waiting for submission page...")
    except:
        print("Could not find login button.")
        driver.quit()
        exit()

    time.sleep(5)  # wait for login to complete

    # --- Submit each poem ---
    for poem in poems:
        driver.get("https://allpoetry.com/poem/add")
        print(f"Navigated to poem submission page for: {poem['title']}")

        try:
            title_elem = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="item_title"]')))
            body_elem = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="item_rendered"]')))
        except:
            print(f"Could not find poem input fields for: {poem['title']}")
            continue

        title_elem.clear()
        title_elem.send_keys(poem["title"])
        body_elem.clear()
        body_elem.send_keys(poem["body"])

        # --- Click first submit button ---
        try:
            submit_btn = wait.until(EC.element_to_be_clickable(
                (By.XPATH, '/html/body/div[1]/div/div[2]/form/div[2]/div/div/div[1]/div/div/div/div[3]/div[6]/input')))
            submit_btn.click()
            print(f"Clicked first submit for: {poem['title']}")
        except:
            print(f"Could not click first submit for: {poem['title']}")
            continue

        # --- Click confirmation button on second page ---
        try:
            confirm_btn = wait.until(EC.element_to_be_clickable(
                (By.XPATH, '/html/body/div[1]/div/div[2]/ol/li[5]/a')))
            confirm_btn.click()
            print(f"Confirmed submission for: {poem['title']}")
        except:
            print(f"Could not click confirmation button for: {poem['title']}")

        time.sleep(2)  # short pause between submissions

finally:
    driver.quit()
    print("All done. Browser closed.")
