from selenium import webdriver
from selenium.webdriver.common.by import By


class Test404page():
  def setup_method(self, method):
    self.driver = webdriver.Chrome('./chromedriver')
  
  def teardown_method(self, method):
    self.driver.quit()
  
  def test_404page(self):
    self.driver.get("http://localhost:8000/type_anything")
    self.driver.set_window_size(1280, 729)
    assert self.driver.find_element(By.CSS_SELECTOR, ".title").text == "404"
    assert self.driver.find_element(By.LINK_TEXT, "Go to homepage").text == "Go to homepage"
    self.driver.find_element(By.LINK_TEXT, "Go to homepage").click()
    assert self.driver.title == "BC COVID-19 Updates"