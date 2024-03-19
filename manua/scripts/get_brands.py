from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
from manua.models import Brand

# Set up Selenium Chrome WebDriver
chrome_options = Options()
chrome_options.add_argument('--headless')  # Run Chrome in headless mode (without GUI)
driver = webdriver.Chrome(options=chrome_options)

# Function to click on the "nav__more" link to load all brand elements
def click_nav_more():
    try:
        # Load the webpage
        driver.get("https://www.manua.ls/")

        # Find and click on the "nav__more" link
        driver.find_element(By.CLASS_NAME, "nav__more").click()

        # Wait for some time to let the elements load
        time.sleep(2)

    except Exception as e:
        print(f"Error clicking on 'nav__more' link: {e}")

# Function to scrape brand names
def scrape_brands():
    try:
        # Get the page source after clicking on "nav__more" link
        page_source = driver.page_source

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(page_source, "html.parser")

        # Find all <div> tags containing brand names
        brand_divs = soup.find_all('div', class_='smart-image nav__img')
        brand_links_divs = soup.find_all('a', class_='nav__item')

        brand_names = [div['title'] for div in brand_divs]
        brand_links = ['https://www.manua.ls' + div['href'] for div in brand_links_divs]

        return list(zip(brand_names, brand_links))


    except Exception as e:
        print(f"Error scraping brands: {e}")
        return []
    
    finally:    
        # Close the WebDriver
        driver.quit()
        
def run():
    click_nav_more()

    brands = scrape_brands()

    for brand_name, brand_link in brands:
        brand = Brand.objects.create(title=brand_name, link=brand_link)
        brand.save()
        
    print("Brands Saved!")


run()
