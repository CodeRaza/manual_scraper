import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from manua.models import Product  
# from pdf_downloader import download_pdf  # Import your PDF downloader function
from manua.scripts.downloader_pdf_ import scrape_pdf
def scrape_and_download_manuals():
    # Set up Selenium Chrome WebDriver
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Run Chrome in headless mode (without GUI)
    driver = webdriver.Chrome(options=chrome_options)

    # Get all saved products
    products = Product.objects.all()

    # Iterate over each product
    for product in products:
        try:
            driver.get(product.link)
            time.sleep(2)
            print(f"Going into the {product.title} & {product.link}")

            manual_links = driver.find_elements(By.CSS_SELECTOR, '.d-flex.w-100.text-dark.text-decoration-none')

            for link_element in manual_links:
                manual_link = link_element.get_attribute('href')
                product_name_element = link_element.find_element(By.TAG_NAME, 'h5')
                product_name = product_name_element.text.strip()
                scrape_pdf(manual_link, product, product_name)

        except Exception as e:
            print(f"Error downloading manuals for {product.title}: {e}")

    driver.quit()

def run():
    scrape_and_download_manuals()

run()