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
        platform_key = url[13]
        timeout = 10

        # Initialize variables
        name, price, img = None, None, None
        
        if platform_key.lower() == 'n':  # RIDE
            try:
                name_element = WebDriverWait(driver, timeout).until(
                    EC.presence_of_element_located((By.XPATH, "//h1[@class='notranslate']"))
                )
                name = name_element.text
            except (NoSuchElementException, TimeoutException):
                name = None  # Element not found

            try:
                price_element = WebDriverWait(driver, timeout).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'normal-price'))
                )
                price = price_element.text.replace(',', '').replace('$', '')
            except (NoSuchElementException, TimeoutException):
                price = None  # Element not found

            try:
                img_element = WebDriverWait(driver, timeout).until(
                    EC.presence_of_element_located((By.XPATH, "//img[@alt='1']"))
                )
                img = img_element.get_attribute('src')
            except (NoSuchElementException, TimeoutException):
                img = None  # Element not found

        elif platform_key.lower() == 'u':  # BURTON
            try:
                name_element = WebDriverWait(driver, timeout).until(
                    EC.presence_of_element_located((By.XPATH, "//h1[@class='product-name text-h2-display']"))
                )
                name = name_element.text.replace("\u00ae", "")
            except (NoSuchElementException, TimeoutException):
                name = None

            try:
                price_element = WebDriverWait(driver, timeout).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'standard-price'))
                )
                price = price_element.text.replace(',', '').replace('$', '')
            except (NoSuchElementException, TimeoutException):
                price = None

            try:
                img_div = WebDriverWait(driver, timeout).until(
                    EC.presence_of_element_located((By.XPATH, "//div[@class='gallery-item']"))
                )
                if img_div:
                    img_element = img_div.find_element(By.TAG_NAME, 'img')
                    img = img_element.get_attribute('src')
            except (NoSuchElementException, TimeoutException):
                img = None

        elif platform_key.lower() == 'm':  # SMITH
            try:
                name_element = WebDriverWait(driver, timeout).until(
                    EC.presence_of_element_located((By.XPATH, "//h1[@class='product-name']"))
                )
                name = 'SMITH ' + name_element.text
            except (NoSuchElementException, TimeoutException):
                name = None

            try:
                price_element = WebDriverWait(driver, timeout).until(
                    EC.presence_of_element_located((By.XPATH, "//span[@class='js-list-price']"))
                )
                price = price_element.text.replace(',', '').replace('$', '')
            except (NoSuchElementException, TimeoutException):
                price = None

            try:
                img_div = WebDriverWait(driver, timeout).until(
                    EC.presence_of_element_located((By.XPATH, "//div[@class='prod-img']"))
                )
                if img_div:
                    img_element = img_div.find_element(By.TAG_NAME, 'img')
                    img = img_element.get_attribute('src')
            except (NoSuchElementException, TimeoutException):
                img = None

        elif platform_key.lower() == 'a':  # HALFDAYS
            try:
                name_element = WebDriverWait(driver, timeout).until(
                    EC.presence_of_element_located((By.XPATH, "//h1[@role='heading']"))
                )
                name = 'Halfdays ' + name_element.text
            except (NoSuchElementException, TimeoutException):
                name = None

            try:
                price_element = WebDriverWait(driver, timeout).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "span.price-item.price-item--regular"))
                )
                price = price_element.get_attribute('innerHTML').strip().replace(',', '').replace('$', '')
            except (NoSuchElementException, TimeoutException):
                price = None

            try:
                img_element = WebDriverWait(driver, timeout).until(
                    EC.presence_of_element_located((By.XPATH, "//img[@class='photoswipe__image']"))
                )
                img = img_element.get_attribute('src')
            except (NoSuchElementException, TimeoutException):
                img = None

        else: # Invalid platform key
            raise ValueError(f"Invalid platform key '{platform_key}'. Ensure platform is supported.")
        
        if not price or not img or not name:
            raise RuntimeError("Failed to extract some or all data from URL. Ensure platform is supported.")
        
        info = {
            'name': name,
            'price': price,
            'img': img
        }
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

        result = get_info(url)  # Your scraping logic here
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

'''if __name__ == "__main__":
    url = "https://www.halfdays.com/products/johnson-top-peony"  # Hardcoded for testing
    info = get_info(url)
    print(info)'''