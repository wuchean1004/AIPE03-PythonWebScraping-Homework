from __future__ import annotations

import argparse
import time
from pathlib import Path

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


BOOK_URL = "https://www.mangaz.com/book/detail/157901"
DEFAULT_OUTPUT_DIR = "downloaded_manga"
WAIT_SECONDS = 10
PAGE_LOAD_SECONDS = 2

FREE_READ_SELECTOR = "button.open-viewer.book-begin.ga"
PAGE_IMAGE_SELECTOR = "div.page_image img.image"
NEXT_PAGE_SELECTOR = "div.flip.flip-left"
READ_NOW_TEXT = "すぐに読む"
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/121.0.0.0 Safari/537.36"
)


def create_driver() -> webdriver.Chrome:
    options = Options()
    options.add_argument('--start-maximized')
    options.add_argument('--incognito')
    options.add_argument('--disable-popup-blocking')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument(f"user-agent={USER_AGENT}")
    options.add_argument("--disable-blink-features=AutomationControlled")
    return webdriver.Chrome(options=options)


def open_book_page(driver: webdriver.Chrome, url: str = BOOK_URL) -> None:
    driver.get(url)
    print("Page Title:", driver.title)


def enter_reader(driver: webdriver.Chrome, timeout: int = WAIT_SECONDS) -> None:
    wait = WebDriverWait(driver, timeout)
    original_windows = set(driver.window_handles)

    button = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, FREE_READ_SELECTOR))
    )
    button.click()

    wait.until(
        lambda current_driver: len(current_driver.window_handles) > len(original_windows)
    )
    new_windows = [
        handle for handle in driver.window_handles if handle not in original_windows
    ]
    driver.switch_to.window(
        new_windows[-1] if new_windows else driver.window_handles[-1]
    )

    read_now = wait.until(
        EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, READ_NOW_TEXT))
    )
    read_now.click()


def download_pages(
    driver: webdriver.Chrome,
    output_dir: str | Path = DEFAULT_OUTPUT_DIR,
    timeout: int = WAIT_SECONDS,
    page_load_seconds: int = PAGE_LOAD_SECONDS,
) -> int:
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    wait = WebDriverWait(driver, timeout)
    total_image_count = 0

    while True:
        wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, PAGE_IMAGE_SELECTOR))
        )
        image_elements = driver.find_elements(By.CSS_SELECTOR, PAGE_IMAGE_SELECTOR)

        for image_element in image_elements:
            if image_element.is_displayed():
                file_path = output_path / f"manga_page_{total_image_count:03}.png"
                image_element.screenshot(str(file_path))
                print(f"成功擷取頁面並儲存為: {file_path}")
                total_image_count += 1

        try:
            next_page = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, NEXT_PAGE_SELECTOR))
            )
            next_page.click()
            print("已點擊下一頁，等待畫面載入...")
            time.sleep(page_load_seconds)
        except TimeoutException:
            print("【系統提示】找不到下一頁按鈕，已達最後一頁，結束爬取迴圈。")
            break

    return total_image_count


def parse_args() -> argparse.Namespace:
    """Parse command-line options for the scraper."""
    parser = argparse.ArgumentParser(
        description="Download Mangaz manga pages with Selenium screenshots."
    )
    parser.add_argument(
        "--url",
        default=BOOK_URL,
        help="Mangaz book detail URL.",
    )
    parser.add_argument(
        "--output-dir",
        default=DEFAULT_OUTPUT_DIR,
        help="Folder for downloaded manga screenshots.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    driver = create_driver()

    try:
        open_book_page(driver, args.url)
        enter_reader(driver)
        image_count = download_pages(driver, args.output_dir)
        print(f"下載完成，共儲存 {image_count} 張圖片。")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
