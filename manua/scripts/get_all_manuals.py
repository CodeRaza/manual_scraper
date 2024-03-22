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
from manua.scripts.get_specifications import scrape_manual_details
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from manua.scripts.downloader_pdf_ import scrape_pdf
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)

from urllib.parse import urlsplit, urlunsplit

def remove_fragment_from_url(url):
    # Split the URL into its components
    parsed_url = urlsplit(url)
    
    # Remove the fragment from the URL
    cleaned_url = parsed_url._replace(fragment='').geturl()
    
    return cleaned_url

def scrape_and_download_manuals():
    try:
        # options.add_argument('--headless') 
        # options.add_argument('--no-sandbox')
        # options.add_argument('--disable-dev-shm-usage')
        # options.add_argument('--disable-blink-features=AutomationControlled')

        # driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        # Get all saved products
        products = Product.objects.all()

        # Iterate over each product
        for product in products:
            try:

                driver.get(remove_fragment_from_url(product.link))
                print(f"Going into the {product.title} & {product.link}")

                iframes = driver.find_elements(By.TAG_NAME, 'iframe')
                
                for iframe in iframes:
                    driver.execute_script("arguments[0].style.display = 'none';", iframe)
                    
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.d-flex.w-100.text-dark.text-decoration-none')))

                manual_links = driver.find_elements(By.CSS_SELECTOR, '.d-flex.w-100.text-dark.text-decoration-none')

                time.sleep(2)

                for link_element in manual_links:
                    manual_link = link_element.get_attribute('href')
                    # print(manual_link)
                    product_name_element = link_element.find_element(By.TAG_NAME, 'h5')
                    product_name = product_name_element.text.strip()
                    # print(product_name)
                    if Manual.objects.filter(title=product_name).count() < 1:
                        # scrape_pdf(manual_link, product, product_name)
                        scrape_manual_details(manual_link, product, product_name)
                    else:
                        print(f"Manual '{product_name}' for product '{product}' already exists. Skipping.")

            except Exception as e:
                print(f"Error downloading manuals for {product.title}: {e}")

    except Exception as e:
        print(f"Error initializing WebDriver: {e}")

    finally:
        if 'driver' in locals():
            driver.quit()

def run():
    scrape_and_download_manuals()

run()