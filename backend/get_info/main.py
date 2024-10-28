from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

def get_info(url):
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        driver.get(url)
        platform_key = url[13].lower()
        timeout = 5  # Reduced timeout for faster response

        info = {}

        # Helper function to handle element fetching with error checks
        def fetch_element(by, value, description):
            try:
                return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, value)))
            except (NoSuchElementException, TimeoutException):
                raise RuntimeError(f"{description.capitalize()} element not found. Ensure platform is supported and URL points to a single item.")
        
        # Platform-specific scraping
        if platform_key == 'n':  # RIDE
            info['name'] = fetch_element(By.XPATH, "//h1[@class='notranslate']", "Name").text
            info['price'] = fetch_element(By.CLASS_NAME, 'normal-price', "Price").text.replace(',', '').replace('$', '')
            info['img'] = fetch_element(By.XPATH, "//img[@alt='1']", "Image").get_attribute('src')

        elif platform_key == 'u':  # BURTON
            info['name'] = fetch_element(By.XPATH, "//h1[@class='product-name text-h2-display']", "Name").text
            info['price'] = fetch_element(By.CLASS_NAME, 'standard-price', "Price").text.replace(',', '').replace('$', '')
            img_div = fetch_element(By.XPATH, "//div[@class='gallery-item']", "Image container")
            info['img'] = img_div.find_element(By.TAG_NAME, 'img').get_attribute('src')

        elif platform_key == 'm':  # SMITH
            info['name'] = 'SMITH ' + fetch_element(By.XPATH, "//h1[@class='product-name']", "Name").text
            info['price'] = fetch_element(By.XPATH, "//span[@class='js-list-price']", "Price").text.replace(',', '').replace('$', '')
            img_div = fetch_element(By.XPATH, "//div[@class='prod-img']", "Image container")
            info['img'] = img_div.find_element(By.TAG_NAME, 'img').get_attribute('src')

        elif platform_key == 'a':  # HALFDAYS
            info['name'] = 'Halfdays ' + fetch_element(By.XPATH, "//h1[@role='heading']", "Name").text
            info['price'] = fetch_element(By.CSS_SELECTOR, "span.price-item.price-item--regular", "Price").get_attribute('innerHTML').strip().replace(',', '').replace('$', '')
            info['img'] = fetch_element(By.XPATH, "//img[@class='photoswipe__image']", "Image").get_attribute('src')

        else:
            raise ValueError(f"Invalid platform key '{platform_key}'. Ensure platform is supported.")

        # Final check to ensure all required fields are present
        if not all(info.values()):
            raise RuntimeError("Failed to extract name, price, and image data from URL.")

        return info

    except WebDriverException:
        raise RuntimeError("The provided URL could not be accessed or is invalid.")
    except Exception as e:
        raise RuntimeError(f"{e}")
    finally:
        driver.quit()

@app.route('/scrape', methods=['POST'])
def scrape():
    try:
        data = request.json
        url = data.get('url', '')
        if not url:
            return jsonify({'error': 'URL is required'}), 400

        result = get_info(url)  # Scraping logic
        response = make_response(jsonify(result), 200)
        
        # Add CORS headers
        response.headers['Access-Control-Allow-Origin'] = '*'  # Allow all origins, adjust for production
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'  # Allow POST and OPTIONS methods
        
        return response

    except Exception as e:
        response = make_response(jsonify({'error': str(e)}), 500)
        # Add CORS headers for error response as well
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS' 
        
        return response

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
