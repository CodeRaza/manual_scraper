from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
from manua.models import Brand, Product
# Set up Selenium Chrome WebDriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

def scrape_products(brand_link):
    try:
        base_url = "https://www.manua.ls"
        # Set up Selenium Chrome WebDriver
        options = webdriver.ChromeOptions()
        options.add_argument('--headless') 
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

        # Click on the "show more" button to load all product elements
        driver.get(brand_link)
        driver.find_element(By.CLASS_NAME, "link.nav__more.blue").click()
        time.sleep(2)  # Wait for some time to let the elements load

        # Get the page source after clicking on "show more" button
        page_source = driver.page_source

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(page_source, "html.parser")

        # Find all <a> tags containing product names and links
        product_links = soup.find_all('a', class_='nav__item')
        products = [(link.find('span').text.strip(), base_url + link['href']) for link in product_links]

        return products

    except Exception as e:
        print(f"Error scraping products: {e}")
        return []

    finally:
        # Close the WebDriver
        driver.quit()

# Example usage:

def run():
    brands = Brand.objects.all()
    
    for brand in brands: 
        products = scrape_products(brand.link)

        for product_name, product_link in products:
            product, created_product = Product.objects.get_or_create(brand=brand, title=product_name, link=product_link)
            
            if created_product:
                product.save()
                print(f"Product Created! {product_name}")
            else: 
                print(f"Product {product_name} Already Exists!")
            
        print(f"All Products Created for Brand: {brand.title}")
            
run()
