from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import html2text


def page_has_loaded(page):
    page_state = page.execute_script('return document.readyState;')
    return page_state == 'complete'

def find_captcha(page):
    for iframe in page.find_elements_by_tag_name('iframe'):
        try:
            if "google.com/recaptcha/api2/anchor" in iframe.get_attribute('src'):
                return iframe
        except:
            pass
    return None

def captcha_check(page):
    while not page_has_loaded(page):
        print("page is loading")
        time.sleep(1)

    captcha = find_captcha(page)
    while captcha is not None:
        time.sleep(1)
        print("Still have captcha")
        captcha = find_captcha(page)


chromedriver = '/home/shoegaze_boi/chromedriver'
delay = 10000
options = webdriver.ChromeOptions()
options.add_argument('headless')
browser = webdriver.Chrome(executable_path=chromedriver, chrome_options=options)
browser.get('https://www.onetwotrip.com/ru/')


html = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.TAG_NAME, 'html')))
captcha_check(browser)

directions = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'P9BrH')))

deals = WebDriverWait(browser, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-locator="Deals"]')))
actions = ActionChains(browser)
actions.move_to_element(deals).perform()



while 0==0:
    try:
        captcha_check(browser)
        moreBtn = WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.CLASS_NAME, '_1uflg')))
        moreBtn.click()
    except:
        print("Can't find any more buttons.")
        break

airlines = []
dates = []


def way(btn, index):
    options = webdriver.ChromeOptions()
    # options.add_argument('headless')
    new_page = webdriver.Chrome(executable_path=chromedriver, chrome_options=options)

    captcha_check(new_page)
    new_page.get(btn[index].get_attribute('href'))

    captcha_check(new_page)
    new_page.find_element_by_tag_name('html').send_keys(Keys.END)

    print("Работает! Двигаемся дальше. {}".format(index) + ' номер элемента списка.')

    captcha_check(new_page)
    airlines_on_page = WebDriverWait(new_page, delay).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'airlineName')))

    for idx, x in enumerate(airlines_on_page):
        airlines_on_page[idx]= x.text


    captcha_check(new_page)
    dates_on_page = WebDriverWait(new_page, delay).until(EC.presence_of_all_elements_located((By.CLASS_NAME, '_1EF6M')))

    dates_on_page[0] = dates_on_page[0].text.split(' ')

    captcha_check(new_page)

    airlines.append(airlines_on_page)
    print(dates_on_page[0][3])
    dates.append(dates_on_page[0][3])

    new_page.close()



captcha_check(browser)
buttons = WebDriverWait(browser, delay).until(EC.presence_of_all_elements_located((By.CLASS_NAME, '_3b-MW')))

len_button = len(buttons) - 1
index = 0

while index <= len_button:
    print(dates)

    if index == len(buttons):
        break

    way(buttons, index)
    index += 1

