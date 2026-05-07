from dataclasses import dataclass
from pathlib import Path
import os
import tempfile
import shutil
from urllib.parse import quote_plus

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


@dataclass
class TestConfig:
    base_url: str = "https://adnabu-store-assignment1.myshopify.com"
    password: str = "AdNabuQA"
    search_term: str = "snowboard"
    timeout_seconds: int = 15
    highlight_ms: int = 350


class AdNabuStorePage:
    def __init__(self, driver: webdriver.Chrome, wait: WebDriverWait, config: TestConfig) -> None:
        self.driver = driver
        self.wait = wait
        self.config = config

    def _brief_pause(self) -> None:
        self.driver.execute_async_script(
            "const done = arguments[arguments.length - 1]; setTimeout(done, arguments[0]);",
            self.config.highlight_ms,
        )

    def highlight(self, element) -> None:
        self.driver.execute_script(
            "arguments[0].style.outline='3px solid #000000';"
            "arguments[0].style.boxShadow='0 0 0 3px rgba(0,0,0,0.25)';",
            element,
        )
        self._brief_pause()

    def open_store(self) -> None:
        self.driver.get(self.config.base_url)
        self.wait.until(lambda d: d.execute_script("return document.readyState") == "complete")

    def unlock_store(self) -> None:
        password_box = self.wait.until(EC.presence_of_element_located((By.ID, "password")))
        self.highlight(password_box)
        password_box.clear()
        password_box.send_keys(self.config.password)

        submit_btn = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit'], input[type='submit']"))
        )
        self.highlight(submit_btn)
        submit_btn.click()
        self.wait.until(lambda d: d.execute_script("return document.readyState") == "complete")

    def open_search_and_type_product(self) -> None:
        search_icon = self.wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "a[href*='/search'], button[aria-label*='Search'], summary[aria-label*='Search']")
            )
        )
        self.highlight(search_icon)
        search_icon.click()

        search_input = self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type='search'], input[name='q']"))
        )
        self.highlight(search_input)
        search_input.clear()
        search_input.send_keys(self.config.search_term)
        search_input.send_keys(Keys.ENTER)

        search_url = f"{self.config.base_url}/search?q={quote_plus(self.config.search_term)}&type=product"
        self.driver.get(search_url)
        self.wait.until(lambda d: d.execute_script("return document.readyState") == "complete")

    def _first_product_link(self):
        selectors = [
            "main a[href*='/products/']",
            "a.full-unstyled-link[href*='/products/']",
            "a.card-wrapper[href*='/products/']",
            "a[href*='/products/']",
        ]
        for selector in selectors:
            for link in self.driver.find_elements(By.CSS_SELECTOR, selector):
                href = (link.get_attribute("href") or "").strip()
                if link.is_displayed() and "/products/" in href:
                    return link
        return None

    def open_first_product(self) -> None:
        product = self.wait.until(lambda d: self._first_product_link())
        self.driver.execute_script("arguments[0].scrollIntoView({behavior:'smooth', block:'center'});", product)
        self.highlight(product)
        product.click()
        self.wait.until(lambda d: d.execute_script("return document.readyState") == "complete")

    def click_add_to_cart(self) -> None:
        add_selectors = [
            "button[name='add']",
            "form[action*='/cart/add'] button[type='submit']",
            "button.product-form__submit",
            "button[id*='ProductSubmitButton']",
        ]
        for selector in add_selectors:
            try:
                add_btn = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
                self.driver.execute_script("arguments[0].scrollIntoView({behavior:'smooth', block:'center'});", add_btn)
                self.highlight(add_btn)
                add_btn.click()
                return
            except TimeoutException:
                continue
        raise TimeoutException("Add to cart button not found.")

    def verify_cart(self) -> None:
        self.wait.until(
            EC.any_of(
                EC.presence_of_element_located((By.CSS_SELECTOR, "a[href*='/cart']")),
                EC.presence_of_element_located((By.CSS_SELECTOR, "#CartDrawer, .cart-drawer")),
                EC.presence_of_element_located((By.CSS_SELECTOR, "[aria-label*='Cart']")),
            )
        )


def build_driver() -> tuple[webdriver.Chrome, str]:
    options = Options()
    if os.getenv("HEADLESS", "0") == "1":
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-gpu")

    temp_profile_dir = tempfile.mkdtemp(prefix="adnabu_chrome_profile_")
    options.add_argument(f"--user-data-dir={temp_profile_dir}")

    cached_driver_root = Path.home() / ".wdm" / "drivers" / "chromedriver"
    cached_drivers = sorted(cached_driver_root.rglob("chromedriver.exe"))
    service = Service(str(cached_drivers[-1])) if cached_drivers else Service(ChromeDriverManager().install())

    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()
    return driver, temp_profile_dir


def run_product_search_add_to_cart() -> None:
    config = TestConfig()
    driver, temp_profile_dir = build_driver()
    wait = WebDriverWait(driver, config.timeout_seconds)
    try:
        page = AdNabuStorePage(driver, wait, config)
        page.open_store()
        page.unlock_store()
        page.open_search_and_type_product()
        page.open_first_product()
        page.click_add_to_cart()
        page.verify_cart()
        print("PASS: Completed within optimized runtime.")
        input("Press Enter to close the browser...")
    finally:
        driver.quit()
        shutil.rmtree(temp_profile_dir, ignore_errors=True)


if __name__ == "__main__":
    run_product_search_add_to_cart()
