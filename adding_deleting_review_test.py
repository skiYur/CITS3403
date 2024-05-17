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

class ReviewTestCase(unittest.TestCase):
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

    def test_add_and_delete_review(self):
        driver = self.driver
        driver.get('http://127.0.0.1:5000/login')
        print("Navigated to login page:", driver.current_url)

        # Log in
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, 'email'))
        )
        driver.find_element(By.ID, 'email').send_keys('z@gmail.com')
        driver.find_element(By.ID, 'password').send_keys('ZZZZZZZZ!')
        driver.find_element(By.CSS_SELECTOR, '.btn-primary').click()
        print("Submitted login form")

        # Wait for login to complete by checking for a unique element on the landing page
        try:
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'h1'))
            )
            print("Login successful")
        except Exception as e:
            print("Login failed:", e)
            print("Current URL:", driver.current_url)
            print("Page title:", driver.title)
            print("Page source:\n", driver.page_source)
            raise

        # Adding and Deleting Reviews for Each Spirit
        spirits = ["Vodka", "Whiskey", "Gin", "Rum", "Tequila", "Liqueur", "Other", "Non-alcoholic"]
        for spirit in spirits:
            # Open home page
            driver.get('http://127.0.0.1:5000/')
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, 'alcoholicDropdown'))
            )

            # Click on Alcoholic Dropdown and Select Spirit
            driver.find_element(By.ID, 'alcoholicDropdown').click()
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.LINK_TEXT, spirit))
            ).click()
            print(f"Navigated to {spirit} page")

            # Click on "Add a Review" button
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, 'toggle-review-form'))
            ).click()
            print("Clicked 'Add a Review' button")

            # Fill in the review form
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.ID, 'drink_review-form'))
            )
            driver.find_element(By.ID, 'drink-name').send_keys('test')
            driver.find_element(By.ID, 'instructions').send_keys('test instructions')
            driver.find_element(By.ID, 'ingredients').send_keys('test ingredients')
            driver.find_element(By.ID, 'review').send_keys('test review')
            driver.find_element(By.CSS_SELECTOR, '.star:nth-child(3)').click()
            driver.find_element(By.CSS_SELECTOR, '.btn:nth-child(6)').click()
            print("Submitted review form for", spirit)

            # Confirm submission
            try:
                WebDriverWait(driver, 10).until(
                    EC.alert_is_present()
                )
                alert = driver.switch_to.alert
                alert.accept()
                print(f"Review for {spirit} added successfully.")
            except Exception as e:
                print(f"Failed to add review for {spirit}: {e}")
                print("Current URL:", driver.current_url)
                print("Page title:", driver.title)
                print("Page source:\n", driver.page_source)
                continue

            # Delete the review
            try:
                WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, '.btn-danger'))
                ).click()

                # Confirm the deletion
                WebDriverWait(driver, 10).until(
                    EC.alert_is_present()
                )
                alert = driver.switch_to.alert
                alert.accept()

                WebDriverWait(driver, 10).until(
                    EC.text_to_be_present_in_element((By.CSS_SELECTOR, 'body'), 'Review deleted successfully')
                )
                print(f"Review for {spirit} deleted successfully.")
            except Exception as e:
                print(f"Failed to delete review for {spirit}: {e}")
                print("Current URL:", driver.current_url)
                print("Page title:", driver.title)
                print("Page source:\n", driver.page_source)
                continue

if __name__ == '__main__':
    try:
        unittest.main()
    finally:
        flask_process.terminate()  # Ensure the Flask process is terminated
