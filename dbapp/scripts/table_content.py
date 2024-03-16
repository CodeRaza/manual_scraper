from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

def get_table_content(url_):
        
    options = webdriver.ChromeOptions()
    options.add_argument('--headless') 
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    # driver = webdriver.Chrome(options=options)
    # driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    # driver = webdriver.Chrome("/usr/bin/chromedriver", options=options)


    try:
        url = url_
        driver.get(url)

        manual_header_title = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.manual-header__title-wrap h1'))
        )

        h1_text = manual_header_title.text

        button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, 'modal-toc2'))
        )

        button.click()

        modal_content = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'simplebar-content'))
        )
        
        modal_html = """
            <style>
                .ppp__caption__misc {
                    display: none;
                }
            </style>
        """
        
        modal_html += modal_content.get_attribute('outerHTML')

        modal_html = driver.execute_script("""
            var links = document.querySelectorAll('.simplebar-content a');
            links.forEach(function(link) {
                link.setAttribute('href', '#');
            });
            return document.querySelector('.simplebar-content').outerHTML;
        """)

        modal_html = f"""
            <style>
                .ppp__caption__misc {{
                    display: none !important;
                }}
            </style>
            {modal_html}
        """
        
        print(modal_content)    
        
        return {
            'content_table': modal_html,
            'title': h1_text
        }
        
    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        driver.quit()
