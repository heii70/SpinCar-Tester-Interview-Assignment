from time import sleep
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest
#import traceback


@pytest.mark.incremental
class Test360Manager:

    @pytest.fixture(scope='class')
    def assets(self):
    ## Setup
        # Login Data and Webdriver Instantiation
        self.webUrl = "https://test-selenium-manager.spincar.com"
        self.username = "tester1@spincar.com"
        self.password = "password"
        self.driver = webdriver.Chrome()

        # Configurations
        self.driver.set_page_load_timeout(30)
        self.wait = WebDriverWait(self.driver, 10)

        # Test Data
        self.new_customer_name = None
        self.new_folder = None
        self.new_test_value = "test"
        self.max_size = "640"
        self.pano_max_size = "1712"
        self.vbwa_num_frames = "64"
        #self.navbar = None

        yield self
    ## Teardown
        sleep(5)
        self.driver.quit()

    ## Classic Setup-Teardown Class Method

    # def setup_class(self):
    #     self.username = "tester1@spincar.com"
    #     self.password = "password"
    #     self.driver = webdriver.Chrome()
    #
    #     self.driver.set_page_load_timeout(30)
    #     self.wait = WebDriverWait(self.driver, 10)

    # def teardown_class(self):
    #     self.driver.quit()

    # Test Homepage and Login
    def test_homepage_login(self, assets):
        try:
            # open url
            assets.driver.get(assets.webUrl)

            # wait for homepage to load
            assets.wait.until(
                EC.presence_of_element_located((By.NAME, "login_user_form"))
            )

            # Login Activity
            assets.driver.find_element_by_id("email").send_keys(assets.username)
            assets.driver.find_element_by_id("password").send_keys(assets.password)
            assets.driver.find_element_by_id("submit").click()

            # wait for dashboard to load
            assets.wait.until(
                EC.presence_of_element_located((By.ID, "navbar"))
            )
        except (NoSuchElementException, TimeoutException) as e:
            print(e)
            assert 0

    def test_create_new_customer(self, assets, getNewCustomer):
        try:
            # go to Onboard
            self.navbar = assets.driver.find_element_by_id("navbar")
            self.navbar.find_element(By.XPATH, "//ul[1]/li[3]/a[normalize-space(text())='Admin']").click()
            assets.driver.find_element_by_link_text("Onboard").click()

            # wait for Onboard page to load
            assets.wait.until(
                EC.presence_of_element_located((By.ID, "form-create"))
            )

            # clear test fields as a precaution and submit
            assets.driver.find_element_by_id("lastpass-disable-search-u").clear()
            assets.driver.find_element_by_id("lastpass-disable-search-s").clear()
            assets.driver.find_element_by_xpath("//input[@type='submit' and @value='Create Customer']").click()

            # wait error block to be visible
            assets.wait.until(
                EC.visibility_of_element_located((By.ID, "errors"))
            )

            # verify error messages
            error_block = assets.driver.find_element_by_id("errors")
            error_list = error_block.find_elements_by_tag_name("li")

            assert error_list[0].text == "Customer name required"
            assert error_list[1].text == "S3 folder required"
            assert error_list[2].text == "Invalid email address"

            # get new customer info using getNewCustomer fixture and complete form
            assets.new_customer_name, assets.new_folder = getNewCustomer
            assets.driver.find_element_by_id("lastpass-disable-search-u").send_keys(assets.new_customer_name)
            assets.driver.find_element_by_id("lastpass-disable-search-s").send_keys(assets.new_folder)
            #assets.driver.find_element_by_id("lastpass-disable-search-ne").send_keys(assets.new_test_value)
            #assets.driver.find_element_by_id("lastpass-disable-search-ni").send_keys(assets.new_test_value)
            assets.driver.find_element_by_xpath("//input[@type='submit' and @value='Create Customer']").click()

            # wait for config page to load
            assets.wait.until(
                EC.presence_of_element_located((By.XPATH, "//*[@id='content']/div/form[1]/input[@type='submit' and @value='Select Config']"))
            )
        except (NoSuchElementException, TimeoutException) as e:
            print(e)
            assert 0

    def test_verify_customer_created(self, assets):
        try:
            # go to Customers
            self.navbar = assets.driver.find_element_by_id("navbar")
            self.navbar.find_element(By.XPATH, "//ul[1]/li[2]/a[normalize-space(text())='Customers']").click()
            assets.driver.find_element_by_link_text("List").click()

            # wait for Customers page to loaf
            self.sorted_table = assets.wait.until(
                EC.presence_of_element_located((By.XPATH, "//*[@id='content']/div[2]/table"))
            )

            # keep clicking id header until id is sorted in descending order
            while True:
                try:
                    if self.sorted_table.find_element_by_xpath("//thead/tr/th[1]/span").get_attribute("class") == "fa fa-lg fa-caret-down":
                        break
                    else:
                        self.sorted_table.find_element_by_xpath("//thead/tr/th[1]").click()
                except NoSuchElementException:
                    self.sorted_table.find_element_by_xpath("//thead/tr/th[1]").click()

            # click on the newly created customer hyperlink
            self.sorted_table.find_element_by_xpath("//tbody/tr[1]/td[1]/a").click()

            # wait for Edit page to Load
            assets.wait.until(
                EC.presence_of_element_located((By.ID, "form"))
            )

            # verify the new customer's data
            assert assets.driver.find_element_by_name("name").get_attribute("value") == assets.new_customer_name
            assert assets.driver.find_element_by_name("s3_folder").get_attribute("value") == assets.new_folder

            assert assets.driver.find_element_by_name("max_size").get_attribute("value") == assets.max_size
            assert assets.driver.find_element_by_name("pano_max_size").get_attribute("value") == assets.pano_max_size
            assert assets.driver.find_element_by_name("vbwa_num_frames").get_attribute("value") == assets.vbwa_num_frames
            assert assets.driver.find_element_by_name("is_spin_customer").is_selected()
        except (NoSuchElementException, TimeoutException) as e:
            print(e)
            assert 0
