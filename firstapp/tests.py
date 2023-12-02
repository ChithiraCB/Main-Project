
# from django.test import TestCase
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# import unittest

# class LoginTestCase(TestCase):
#     def setUp(self):
#         self.driver = webdriver.Chrome()
#         self.driver.implicitly_wait(10)

#     def tearDown(self):
#         self.driver.quit()

#     def test_login(self):
#         self.driver.get('http://127.0.0.1:3000/login/')  # Update the URL as needed

#         # Find the form by its ID
#         login_form = self.driver.find_element(By.CSS_SELECTOR, 'form')

#         # Fill in the form fields
#         username_input = login_form.find_element(By.NAME, 'username')
#         password_input = login_form.find_element(By.NAME, 'password')

#         username_input.send_keys('athiracb@gmail.com')
#         password_input.send_keys('athira#097')

#         # Submit the form
#         login_form.submit()

#         # You can add assertions here to check if the login was successful
#         # For example, check if the user is redirected to the home page after login
#         self.assertEqual(self.driver.current_url, 'http://127.0.0.1:3000/userhome/')  # Update the expected URL

#         # If the login is not successful, you might want to check for error messages on the page

# if __name__ == '__main__':
#     unittest.main()

# from django.test import TestCase
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

# class SeleniumTest(TestCase):
#     def setUp(self):
#         # Set up the WebDriver in the setUp method
#         self.driver = webdriver.Chrome()

#     def tearDown(self):
#         # Close the WebDriver in the tearDown method
#         self.driver.quit()

#     def test_selenium_example(self):
#         # Navigate to the userhome page
#         self.driver.get('http://127.0.0.1:3000/userhome/')  # Update the URL as needed

#         # Wait for the Ornaments dropdown to be clickable
#         ornaments_dropdown = WebDriverWait(self.driver, 10).until(
#             EC.element_to_be_clickable((By.ID, 'ornamentsDropdown'))
#         )

#         ornaments_dropdown.click()

#         earrings_link = WebDriverWait(self.driver, 10).until(
#             EC.element_to_be_clickable((By.LINK_TEXT, 'Earrings'))
#         )

#         print("Found Earrings link")

#         earrings_link.click()

#         print("Clicked on Earrings link")

#         # Now you are on the page displaying earrings. You can proceed with adding to the cart or performing other actions.
#         WebDriverWait(self.driver, 20).until(
#             EC.presence_of_element_located((By.XPATH, '//div[@class="earrings-content"]'))
#         )
