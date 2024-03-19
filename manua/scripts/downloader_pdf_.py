from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import img2pdf
import os
from manua.models import Manual  # Import the Manual model from your app
from django.core.files import File

from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

options = webdriver.ChromeOptions()
options.add_argument('--headless') 
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

def scrape_pdf(base_url, product, manual_name):
    try:
        page_number = 1
        screenshots = []

        while True:

            current_url = f"{base_url}?p={page_number}"
            print(current_url)
            driver.get(current_url)

            iframes = driver.find_elements(By.TAG_NAME, 'iframe')
            for iframe in iframes:
                driver.execute_script("arguments[0].style.display = 'none';", iframe)

            pdf_div = driver.find_element(By.CSS_SELECTOR, '.viewer-page.viewer-container.active')

            driver.set_window_size(1920, 2000)

            screenshot_file = f"page_{page_number}.png"
            pdf_div.screenshot(screenshot_file)
            screenshots.append(screenshot_file)
                
            page_number += 1

            if driver.current_url == base_url:
                break

        with open(f"{manual_name}.pdf", "wb") as pdf_file:
            pdf_file.write(img2pdf.convert([open(img, "rb") for img in screenshots]))

        print(f"Generated PDF: {manual_name}.pdf")
        
        manual = Manual.objects.create(
            product=product,
            title=manual_name,  # Assuming title is a field in your Product model
            # text=product.description,  # Assuming description is a field in your Product model
        )
        
        with open(f"{manual_name}.pdf", "rb") as f:
            manual.pdf.save(f'{manual_name}.pdf', File(f))

        for screenshot_file in screenshots:
            os.remove(screenshot_file)
            print(f"Deleted screenshot: {screenshot_file}")

        os.remove(f"{manual_name}.pdf")
        
        return True
    
    except Exception as e:
        print(f"Error scraping PDF: {e}")
        return False

    finally:
        driver.quit()

