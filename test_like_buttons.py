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

class LikeSuperlikeDislikeTestCase(unittest.TestCase):
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

    def test_like_superlike_dislike(self):
        driver = self.driver
        
        # First user logs in and submits a review
        driver.get('http://127.0.0.1:5000/login')
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'email'))
        ).send_keys('z@gmail.com')
        driver.find_element(By.ID, 'password').send_keys('ZZZZZZZZ!')
        driver.find_element(By.CSS_SELECTOR, '.btn-primary').click()
        time.sleep(3)
        
        driver.get('http://127.0.0.1:5000/rum')
        driver.find_element(By.ID, 'toggle-review-form').click()
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'drink-name'))
        ).send_keys('Rum Punch')
        driver.find_element(By.ID, 'instructions').send_keys('Mix all ingredients and serve over ice.')
        driver.find_element(By.ID, 'ingredients').send_keys('Rum, Pineapple juice, Orange juice, Grenadine')
        driver.find_element(By.ID, 'review').send_keys('Delicious and refreshing!')
        driver.find_element(By.CSS_SELECTOR, '#rating-stars .star[data-value="5"]').click()
        driver.find_element(By.CSS_SELECTOR, '.btn-custom').click()
        time.sleep(3)
        
        driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(3)
        
        # Second user logs in and likes, superlikes, and dislikes the review
        driver.get('http://127.0.0.1:5000/login')
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'email'))
        ).send_keys('m@gmail.com')
        driver.find_element(By.ID, 'password').send_keys('MMMMMMMM!')
        driver.find_element(By.CSS_SELECTOR, '.btn-primary').click()
        time.sleep(3)
        
        driver.get('http://127.0.0.1:5000/rum')
        
        # Like the review
        like_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.btn-like'))
        )
        like_button.click()
        time.sleep(2)
        
        # Superlike the review
        superlike_button = driver.find_element(By.CSS_SELECTOR, '.btn-super-like')
        superlike_button.click()
        time.sleep(2)
        
        # Dislike the review
        dislike_button = driver.find_element(By.CSS_SELECTOR, '.btn-dislike')
        dislike_button.click()
        time.sleep(2)
        
        # Verify reactions
        like_count = driver.find_element(By.ID, 'like-count-1').text
        superlike_count = driver.find_element(By.ID, 'super-like-count-1').text
        dislike_count = driver.find_element(By.ID, 'dislike-count-1').text
        
        self.assertEqual(like_count, '1')
        self.assertEqual(superlike_count, '1')
        self.assertEqual(dislike_count, '1')

if __name__ == '__main__':
    try:
        unittest.main()
    finally:
        flask_process.terminate()  # Ensure the Flask process is terminated
