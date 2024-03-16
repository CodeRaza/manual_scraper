import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import weasyprint
from django.conf import settings
import os
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

def get_pdf_text(url_, title, output_directory='pdfs/'):
        
    url = url_

    options = webdriver.ChromeOptions()
    options.add_argument('--headless') 
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    # driver = webdriver.Chrome(options=options)
    

    try:
        # driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        
        driver.get(url)

        wait = WebDriverWait(driver, 20)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'page-doc')))

        all_html = ''
        all_text = ''

        while True:

            page_html = driver.find_element(By.CLASS_NAME, 'page-doc').get_attribute('outerHTML')
            all_html += page_html
            
            
            soup = BeautifulSoup(page_html, 'html.parser')
            page_text = soup.get_text('\n', strip=True)
            all_text += page_text

           
            next_button = driver.find_element(By.CLASS_NAME, 'pag-pnext')
            next_button.click()

            wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'page-doc')))

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        if driver:
            driver.quit()

    if all_html and all_text:
        media_root = settings.MEDIA_ROOT
        pdf_path = os.path.join(media_root, output_directory, f'{title}.pdf')

        # Ensure the directory exists, create it if not
        os.makedirs(os.path.join(media_root, output_directory), exist_ok=True)

        weasyprint.HTML(string=all_html).write_pdf(pdf_path)
        return {'text': all_text, "pdf": f'pdfs/{title}.pdf'}

    else:
        print("No HTML content to convert to PDF.")
        return {'text': None, "pdf": None}
