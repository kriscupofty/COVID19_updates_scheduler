import re
from selenium import webdriver
from selenium.webdriver.common.by import By


class TestIndexPage():
  def setup_method(self, method):
    self.driver = webdriver.Chrome('./chromedriver')
  
  def teardown_method(self, method):
    self.driver.quit()
  
  def test_index_age(self):
    self.driver.get("http://localhost:8000/")
    self.driver.set_window_size(1280, 729)
    assert self.driver.title == "BC COVID-19 Updates"

    assert self.driver.find_element(By.CSS_SELECTOR, ".toolbar > span").text == "Welcome"
    
    elements = self.driver.find_elements(By.CSS_SELECTOR, ".fa")
    assert len(elements) == 1
    
    assert self.driver.find_element(By.CSS_SELECTOR, "h2").text == "Latest BC COVID-19 Update"
    
    pattern = re.compile(r'Number\sof\snew\scases:\s\d+\sNote:\sData\sis\sonly\savailable\son\sa\sbusiness\sday\.\sNew\scases\son\snon-business\sdays\swill\sbe\sadded\sto\sthe\snext\sbusiness\sday\.')
    assert pattern.match(self.driver.find_element(By.CSS_SELECTOR, "h3").text)
    
    pattern = re.compile(r'Date:\s2020-(\d{2})-(\d{2})')
    assert pattern.match(self.driver.find_element(By.CSS_SELECTOR, "h4").text)

    pattern = re.compile(r'Last\supdated:\s.+')
    assert pattern.match(self.driver.find_element(By.CSS_SELECTOR, "h5").text)

    self.driver.find_element(By.LINK_TEXT, "Kristy").click()
    assert self.driver.title == "kriscupofty (Kristy Siu) · GitHub"