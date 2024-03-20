import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from manua.models import Product, Manual  
# from pdf_downloader import download_pdf  # Import your PDF downloader function
# Set up Selenium Chrome WebDriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


from manua.scripts.downloader_pdf_ import scrape_pdf
def scrape_and_download_manuals():

    options = webdriver.ChromeOptions()
    options.add_argument('--headless') 
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-blink-features=AutomationControlled')

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

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
                
                if Manual.objects.filter(title=product_name).count() < 1:
                    scrape_pdf(manual_link, product, product_name)
                else:
                    print(f"Manual '{product_name}' for product '{product}' already exists. Skipping.")

        except Exception as e:
            print(f"Error downloading manuals for {product.title}: {e}")

        finally:
            driver.quit()

def run():
    scrape_and_download_manuals()

run()