import subprocess
import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

# Start the Flask application
flask_process = subprocess.Popen(['python', 'Project.py'])

# Wait for the Flask application to start
time.sleep(10)  # Adjust the sleep time if necessary

class UserProfileTestCase(unittest.TestCase):
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

    def test_clicking_on_user_profiles(self):
        driver = self.driver
        driver.get('http://127.0.0.1:5000')
        print("Navigated to home page:", driver.current_url)

        # Log in
        driver.get('http://127.0.0.1:5000/login')
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, 'email'))
        )
        driver.find_element(By.ID, 'email').send_keys('z@gmail.com')
        driver.find_element(By.ID, 'password').send_keys('ZZZZZZZZ!')
        driver.find_element(By.CSS_SELECTOR, '.btn-primary').click()
        print("Submitted login form")

        # Wait for login to complete by checking for a unique element on the landing page
        try:
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'h1'))
            )
            print("Login successful")
        except Exception as e:
            print("Login failed:", e)
            print("Current URL:", driver.current_url)
            print("Page title:", driver.title)
            print("Page source:\n", driver.page_source)
            raise

        # Click on Leaderboard
        leaderboard_link = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.LINK_TEXT, 'Leaderboard'))
        )
        leaderboard_link.click()
        print("Navigated to Leaderboard page:", driver.current_url)

        # Click on the first user profile (e.g., 'z') from the leaderboard
        user_profile_link = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.LINK_TEXT, 'z'))
        )
        user_profile_link.click()
        print("Clicked on user 'z' profile:", driver.current_url)

        # Click on Popular Reviews
        popular_reviews_link = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.LINK_TEXT, 'Popular Reviews'))
        )
        popular_reviews_link.click()
        print("Navigated to Popular Reviews page:", driver.current_url)

        # Click on the first user profile (e.g., 'test') from the popular reviews
        popular_review_user_link = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.LINK_TEXT, 'test'))
        )
        popular_review_user_link.click()
        print("Clicked on user 'test' profile:", driver.current_url)

        # Perform a search
        search_input = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.NAME, 'query'))
        )
        search_input.send_keys('test')
        search_input.send_keys(Keys.ENTER)
        print("Performed search for 'test'")

        # Click on the first search result (e.g., 'test')
        search_result_link = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.LINK_TEXT, 'test'))
        )
        search_result_link.click()
        print("Clicked on user 'test' profile from search results:", driver.current_url)

if __name__ == '__main__':
    try:
        unittest.main()
    finally:
        flask_process.terminate()  # Ensure the Flask process is terminated
