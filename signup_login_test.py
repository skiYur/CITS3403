import subprocess
import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

# Start the Flask application
flask_process = subprocess.Popen(['python', 'Project.py'])

# Wait for the Flask application to start
time.sleep(5)  # Adjust the sleep time if necessary

class SignupLoginTestCase(unittest.TestCase):
    def setUp(self):
        chrome_options = Options()
        # Remove headless mode to see the browser
        # chrome_options.add_argument("--headless")  # Enable headless mode
        chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration
        chrome_options.add_argument("--no-sandbox")  # Bypass OS security model
        chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems

        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
        self.driver.maximize_window()

    def tearDown(self):
        self.driver.quit()

    def test_signup_and_login(self):
        driver = self.driver
        driver.get('http://127.0.0.1:5000/login?next=%2F')
        print("Navigated to:", driver.current_url)

        # Wait for the sign-up link to be clickable and then click it
        try:
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.LINK_TEXT, 'Sign up here'))
            ).click()
        except Exception as e:
            print("Error clicking sign-up link:", e)
            print("Current URL:", driver.current_url)
            print("Page title:", driver.title)
            print("Page source:\n", driver.page_source)
            raise

        # Wait for the sign-up page to load
        WebDriverWait(driver, 10).until(
            EC.url_to_be('http://127.0.0.1:5000/sign-up')
        )
        print("Navigated to sign-up page:", driver.current_url)

        # Generate unique username and email
        unique_id = str(int(time.time()))
        username = f'seleniumuser{unique_id}'
        email = f'selenium{unique_id}@example.com'
        password = 'Selenium!'

        # Wait for the username field to be present and then enter username
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, 'username'))
            ).send_keys(username)
        except Exception as e:
            print("Error entering username:", e)
            print("Current URL:", driver.current_url)
            print("Page title:", driver.title)
            print("Page source:\n", driver.page_source)
            raise

        # Enter email
        driver.find_element(By.ID, 'email').send_keys(email)
        # Enter password
        driver.find_element(By.ID, 'password1').send_keys(password)
        driver.find_element(By.ID, 'password2').send_keys(password)

        # Click the submit button
        driver.find_element(By.CSS_SELECTOR, '.btn-primary').click()

        # Wait for the sign-up process to complete
        time.sleep(3)

        # Log in
        driver.get('http://127.0.0.1:5000/login')
        print("Navigated to:", driver.current_url)

        try:
            driver.find_element(By.ID, 'email').send_keys(email)
            driver.find_element(By.ID, 'password').send_keys(password)
            driver.find_element(By.CSS_SELECTOR, '.btn-primary').click()
        except Exception as e:
            print("Error logging in:", e)
            print("Current URL:", driver.current_url)
            print("Page title:", driver.title)
            print("Page source:\n", driver.page_source)
            raise

        # Wait for the login process to complete
        time.sleep(3)

        # Verify successful login
        try:
            body_text = driver.find_element(By.CSS_SELECTOR, 'body').text
            self.assertIn('Welcome', body_text)
        except Exception as e:
            print("Error verifying login:", e)
            print("Current URL:", driver.current_url)
            print("Page title:", driver.title)
            print("Page source:\n", driver.page_source)
            raise

if __name__ == '__main__':
    try:
        unittest.main()
    finally:
        flask_process.terminate()  # Ensure the Flask process is terminated
