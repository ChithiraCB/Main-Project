
from django.test import TestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
import unittest

class LoginTestCase(TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)

    def tearDown(self):
        self.driver.quit()

    def test_login(self):
        self.driver.get('http://127.0.0.1:3000/login/')  # Update the URL as needed

        # Find the form by its ID
        login_form = self.driver.find_element(By.CSS_SELECTOR, 'form')

        # Fill in the form fields
        username_input = login_form.find_element(By.NAME, 'username')
        password_input = login_form.find_element(By.NAME, 'password')

        username_input.send_keys('athiracb@gmail.com')
        password_input.send_keys('athira#098')

        # Submit the form
        login_form.submit()
        self.assertEqual(self.driver.current_url, 'http://127.0.0.1:3000/userhome/')  # Update the expected URL

        # If the login is not successful, you might want to check for error messages on the page

if __name__ == '__main__':
    unittest.main()


from django.test import TestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
class SeleniumTest(TestCase):
    def setUp(self):
        # Set up the WebDriver in the setUp method
        self.driver = webdriver.Chrome()
    def tearDown(self):
        # Close the WebDriver in the tearDown method
        self.driver.quit()
    def test_selenium_example(self):
        # Navigate to the login page
        self.driver.get('http://127.0.0.1:3000/login/')  # Update the URL as needed
        # Fill out the login form with sample data
        username_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )
        password_input = self.driver.find_element(By.NAME, "password")
        username_input.send_keys("athiracb@gmail.com")  # Replace with actual username
        password_input.send_keys("athira#098")  # Replace with actual password
         # Submit the login form
        login_button = self.driver.find_element(By.ID, "login")
        login_button.click()
        # Wait for the userhome page to load
        ornaments_dropdown = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'ornamentsDropdown'))
        )
        ornaments_dropdown.click()
        earrings_link = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, 'Earrings'))
        )
        print("Found Earrings link")
        earrings_link.click()
        print("Clicked on Earrings link")
        # Wait for the 'Add to Cart' button on the product page
        add_to_cart_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[@class="cart-button"]'))
        )
        print("Found 'Add to Cart' button")
        # Click on the "Add to Cart" button
        add_to_cart_button.click()
        print("Clicked on 'Add to Cart' button")
      # Wait for the 'Add to Cart' button on the product page
        add_to_cart_button = WebDriverWait(self.driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, 'quantity-btn.increase-quantity'))
)
        print("Found 'Add to Cart' button")
        add_to_cart_button.click()
        print("Clicked on 'Add to Cart' button")
        print("Product added to the cart successfully")
        self.driver.get('http://127.0.0.1:3000/view_cart/')  # Update the URL as needed

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# Set up the WebDriver (assuming Chrome here)
driver = webdriver.Chrome()
try:
    # Open the login page
    driver.get("http://127.0.0.1:3000/login/")  # Change the URL accordingly
    # Fill out the login form with sample data
    username_input = driver.find_element(By.NAME, "username")
    password_input = driver.find_element(By.NAME, "password")
    username_input.send_keys("admin@gmail.com")
    password_input.send_keys("chithira#123")
    # Submit the login form
    driver.find_element(By.ID, "login").click()
    # Navigate to the add product page
    driver.get("http://127.0.0.1:3000/addproduct/")  # Change the URL accordingly
    # Fill out the form with sample data
    driver.find_element(By.ID, "product-name").send_keys("Test Product")
    driver.find_element(By.ID, "category-name").send_keys("ornaments")
    driver.find_element(By.ID, "subcategory-name").send_keys("Neckpieces")
    driver.find_element(By.ID, "stock").send_keys("10")
    driver.find_element(By.ID, "description").send_keys("This is a test product description.")
    driver.find_element(By.ID, "price").send_keys("100")
    driver.find_element(By.ID, "discount").send_keys("10")
    # Submit the form
    driver.find_element(By.ID, "add-product-button").click()
    # Open the view product page
    driver.get("http://127.0.0.1:3000/viewproduct/")  # Change the URL accordingly
    search_input = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, ".form-inline input.form-control"))
)
    search_input.send_keys("Test Product")
    search_input.send_keys(Keys.RETURN)
# Assert that the test product is in the table
    # assert "Test Product" in driver.page_source
    WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//table[@class='table']"))
)
finally:
    # Close the browser window
    driver.quit()


import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException  # Add this import

class SeleniumSearchTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()

    def tearDown(self):
        self.driver.quit()

    def test_search_product(self):
        # Navigate to the login page
        self.driver.get('http://127.0.0.1:3000/login/')  # Update the URL as needed

        # Log in (replace placeholders with actual data)
        username_input = self.driver.find_element(By.NAME, "username")
        password_input = self.driver.find_element(By.NAME, "password")

        username_input.send_keys("athiracb@gmail.com")
        password_input.send_keys("athira#098")

        login_button = self.driver.find_element(By.ID, "login")
        login_button.click()

        # Wait for the user home page to load
        ornaments_dropdown = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'ornamentsDropdown'))
        )
        ornaments_dropdown.click()
        bangles_link = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, 'Bangles'))
        )
        print("Found Bangles link")
        bangles_link.click()
        print("Clicked on Bangles link")

        # Wait for the search input to be clickable
        search_input = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'searchInput'))
        )

        # Enter the search term "blueray bangles"
        search_input.send_keys("Beaded Bangle")
        print("input blueray bangles")

        # Click the search button
        search_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'search'))
        )
        search_button.click()
        print("search button clicked")
        

        try:
            WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'product-card'))
            )
            print("Found")

            # Verify that the product is displayed in the results
            product_cards = self.driver.find_elements(By.CLASS_NAME, 'product-card')

            # Print the names of the products found
            product_names = [card.find_element(By.CLASS_NAME, 'product-details').find_element(By.TAG_NAME, 'h4').text.strip() for card in product_cards]
            print("Product Names:", product_names)

            # Check if the desired product is in the search results
            product_found = any("Beaded Bangle" in name for name in product_names)

            if not product_found:
                self.fail("Product not found in the search results")

        except TimeoutException:
            self.fail("Timed out waiting for search results to load")


if __name__ == "__main__":
    unittest.main()
