from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def filter_req(url: str, func: callable = None, driver: str = None) -> None:
    driver = webdriver.Chrome()

    driver.get(url)

    network_requests_before = driver. \
        execute_script("return window.performance.getEntriesByType('resource')")

    func(driver) if func is not None else None

    network_requests_after = driver. \
        execute_script("return window.performance.getEntriesByType('resource')")

    new_requests = [req for req in network_requests_after if
                    req not in network_requests_before and req['name'].startswith('https://')]

    for req in new_requests:
        print(req['name'])

    driver.quit()


if __name__ == '__main__':
    import time


    def func(driver: webdriver) -> None:
        element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'jsx.read.auto.icon.icon-play')))
        element.click()

        time.sleep(15)


    filter_req(
        url='https://en.openrussian.org/ru/американец',
        func=func,
        driver=None
    )
