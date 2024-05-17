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
from app import create_app, db
from app.models import User, Post

class LikeButtonTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.flask_process = subprocess.Popen(['python', 'Project.py'])
        time.sleep(5)  # Wait for the Flask application to start

    @classmethod
    def tearDownClass(cls):
        cls.flask_process.terminate()

    def setUp(self):
        chrome_options = Options()
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
        self.driver.maximize_window()

        # Set up the Flask test app and database
        self.app = create_app('config.TestConfig')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.populate_db()

    def tearDown(self):
        self.driver.quit()
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def populate_db(self):
        user1 = User(username='z', email='z@gmail.com')
        user1.set_password('ZZZZZZZZ!')
        user2 = User(username='m', email='m@gmail.com')
        user2.set_password('MMMMMMMM!')
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()

    def test_like_buttons(self):
        driver = self.driver
        driver.get('http://127.0.0.1:5000/login')

        # Log in as user1 and submit a review
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'email')))
        driver.find_element(By.ID, 'email').send_keys('user1@example.com')
        driver.find_element(By.ID, 'password').send_keys('Password1!')
        driver.find_element(By.CSS_SELECTOR, '.btn-primary').click()

        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'h1')))
        driver.get('http://127.0.0.1:5000/vodka')

        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'toggle-review-form'))).click()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'drink-review-form')))
        driver.find_element(By.ID, 'drink-name').send_keys('test')
        driver.find_element(By.ID, 'instructions').send_keys('test instructions')
        driver.find_element(By.ID, 'ingredients').send_keys('test ingredients')
        driver.find_element(By.ID, 'review').send_keys('test review')
        driver.find_element(By.CSS_SELECTOR, '.star:nth-child(3)').click()
        driver.find_element(By.CSS_SELECTOR, '.btn:nth-child(6)').click()

        WebDriverWait(driver, 10).until(EC.alert_is_present())
        driver.switch_to.alert.accept()

        # Log out user1
        driver.get('http://127.0.0.1:5000/logout')

        # Log in as user2 and interact with the review
        driver.get('http://127.0.0.1:5000/login')
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'email')))
        driver.find_element(By.ID, 'email').send_keys('user2@example.com')
        driver.find_element(By.ID, 'password').send_keys('Password2!')
        driver.find_element(By.CSS_SELECTOR, '.btn-primary').click()

        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'h1')))
        driver.get('http://127.0.0.1:5000/vodka')

        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'btn-like'))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'btn-super-like'))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'btn-dislike'))).click()

if __name__ == '__main__':
    unittest.main()
