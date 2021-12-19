import unittest
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TspSeleniumTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Firefox()

    def test_example1_matrix(self):
        driver = self.driver
        driver.get("http://127.0.0.1:5000/")
        self.assertIn("TSP", driver.title)

        driver.find_element_by_xpath('//button[text()="Sample #1"]').click()
        driver.find_element_by_id('calculate').click()

        WebDriverWait(driver, 1).until(
            EC.text_to_be_present_in_element((By.ID, "message"), "OK")
        )

        expected_value = 10
        assert driver.find_element_by_id("info").\
            get_attribute("innerHTML").\
            endswith(str(expected_value))

    def set_matrix(self, m):
        for i in range(len(m)):
            for j in range(len(m)):
                if i == j:
                    continue
                elem = self.driver.find_element_by_id('A-{}-{}'.format(i, j))
                elem.clear()
                elem.send_keys(m[i][j])

    def test_enter_custom_matrix(self):
        driver = self.driver
        driver.get("http://127.0.0.1:5000/")
        self.assertIn("TSP", driver.title)

        driver.find_element_by_id('increment_size').click()

        self.set_matrix([
            [0, 1, 9, 9],
            [9, 0, 2, 9],
            [9, 9, 0, 3],
            [5, 9, 9, 0]])

        driver.find_element_by_id('calculate').click()

        WebDriverWait(driver, 1).until(
            EC.text_to_be_present_in_element((By.ID, "message"), "OK")
        )

        expected_value = 11
        assert driver.find_element_by_id("info").\
            get_attribute("innerHTML").\
            endswith(str(expected_value))

    def test_random_matrix(self):
        driver = self.driver
        driver.get("http://127.0.0.1:5000/")
        self.assertIn("TSP", driver.title)

        driver.find_element_by_id('increment_size').click()

        self.set_matrix([
            [0, 1, 9, 9],
            [9, 0, 2, 9],
            [9, 9, 0, 3],
            [5, 9, 9, 0]])

        driver.find_element_by_id('calculate').click()

        WebDriverWait(driver, 1).until(
            EC.text_to_be_present_in_element((By.ID, "message"), "OK")
        )

        expected_value = 11
        assert driver.find_element_by_id("info").\
            get_attribute("innerHTML").\
            endswith(str(expected_value))


    def test_smallest_matrix(self):
        driver = self.driver
        driver.get("http://127.0.0.1:5000/")
        self.assertIn("TSP", driver.title)

        driver.find_element_by_id('decrement_size').click()

        self.set_matrix([
            [0, 1,],
            [1, 0,]])

        driver.find_element_by_id('calculate').click()

        WebDriverWait(driver, 1).until(
            EC.text_to_be_present_in_element((By.ID, "message"), "OK")
        )

        expected_value = 2
        assert driver.find_element_by_id("info").\
            get_attribute("innerHTML").\
            endswith(str(expected_value))


    def test_enter_custom_big_matrix(self):
        driver = self.driver
        driver.get("http://127.0.0.1:5000/")
        self.assertIn("TSP", driver.title)

        m = [[0, 327, 353, 144, 217, 452, 333, 318, 304, 149, 280],
             [327, 0, 243, 183, 376, 174, 90, 158, 403, 251, 56],
             [353, 243, 0, 263, 245, 190, 155, 85, 217, 205, 206],
             [144, 183, 263, 0, 250, 318, 199, 203, 311, 118, 138],
             [217, 376, 245, 250, 0, 417, 327, 268, 90, 134, 320],
             [452, 174, 190, 318, 417, 0, 119, 150, 405, 330, 187],
             [333, 90, 155, 199, 327, 119, 0, 74, 337, 221, 74],
             [318, 158, 85, 203, 268, 150, 74, 0, 267, 183, 122],
             [304, 403, 217, 311, 90, 405, 337, 267, 0, 194, 349],
             [149, 251, 205, 118, 134, 330, 221, 183, 194, 0, 195],
             [280, 56, 206, 138, 320, 187, 74, 122, 349, 195, 0]]

        for i in range(len(m)-3):
            driver.find_element_by_id('increment_size').click()

        self.set_matrix(m)

        driver.find_element_by_id('calculate').click()

        WebDriverWait(driver, 5).until(
            EC.text_to_be_present_in_element((By.ID, "message"), "OK")
        )

        expected_value = 1372

        assert driver.find_element_by_id("info").get_attribute("innerHTML").endswith(str(expected_value))

    def test_biggest_matrix(self):
        driver = self.driver
        driver.get("http://127.0.0.1:5000/")
        self.assertIn("TSP", driver.title)

        m = [[0, 327, 353, 144, 217, 452, 333, 318, 304, 149, 280],
             [327, 0, 243, 183, 376, 174, 90, 158, 403, 251, 56],
             [353, 243, 0, 263, 245, 190, 155, 85, 217, 205, 206],
             [144, 183, 263, 0, 250, 318, 199, 203, 311, 118, 138],
             [217, 376, 245, 250, 0, 417, 327, 268, 90, 134, 320],
             [452, 174, 190, 318, 417, 0, 119, 150, 405, 330, 187],
             [333, 90, 155, 199, 327, 119, 0, 74, 337, 221, 74],
             [318, 158, 85, 203, 268, 150, 74, 0, 267, 183, 122],
             [304, 403, 217, 311, 90, 405, 337, 267, 0, 194, 349],
             [149, 251, 205, 118, 134, 330, 221, 183, 194, 0, 195],
             [280, 56, 206, 138, 320, 187, 74, 122, 349, 195, 0]]

        for i in range(len(m)-3):
            driver.find_element_by_id('increment_size').click()

        self.set_matrix(m)

        driver.find_element_by_id('calculate').click()

        WebDriverWait(driver, 5).until(
            EC.text_to_be_present_in_element((By.ID, "message"), "OK")
        )

        expected_value = 1372

        assert driver.find_element_by_id("info").get_attribute("innerHTML").endswith(str(expected_value))

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

if __name__ == "__main__":
    unittest.main()