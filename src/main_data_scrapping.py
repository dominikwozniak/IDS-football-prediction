from selenium import webdriver
import os
from xG_data_scrapping import YEARS
import time

SEASON_AMOUNT = len(YEARS)
MAIN_DATA_PATH = os.path.join('..', 'main_data')
PAGE_ADDRESS = "https://www.football-data.co.uk/englandm.php"
PATH_TO_CHROME_DRIVER = os.path.join('..', 'chrome_driver', 'chromedriver.exe')
DOWNLOAD_LINK_TEXT = "Premier League"
DOWNLOAD_DEFAULT_DIRECTORY = os.environ.get("DOWNLOAD_DEFAULT_DIRECTORY")

# TODO 1
#  Add try except statements in case of website code changes, etc.

# TODO 2
#  Optimize scraper in the same way as with xG_data_scraper

# TODO 3
#  Make this script run periodically (every week ?)


def download_data(download_dir: str, page_address: str):

    driver = webdriver.Chrome(PATH_TO_CHROME_DRIVER)

    # get request to target the site
    driver.get(page_address)

    # finding all links with text "Premier League" on page
    links = driver.find_elements_by_link_text(DOWNLOAD_LINK_TEXT)

    print(f"Downloading started")
    for counter in range(SEASON_AMOUNT):
        print(f"Downloading dataset [{counter + 1} / {SEASON_AMOUNT}]")
        links[counter].click()
        href = links[counter].get_attribute("href")

        # getting filename from href attribute of link
        file_name = href[href.rfind('/')+1:]
        old_file_path = os.path.join(DOWNLOAD_DEFAULT_DIRECTORY, file_name)

        # Wait maximum 10 seconds until csv is downloaded to default download directory
        for _ in range(10):
            if not os.path.exists(os.path.join(DOWNLOAD_DEFAULT_DIRECTORY, old_file_path)):
                time.sleep(1)
            else:
                break
        new_file_path = os.path.join(download_dir, file_name)

        # moving data from default download directory to main_data directory
        os.rename(old_file_path, new_file_path)

        # renaming file
        new_file_name = f"season_{YEARS[SEASON_AMOUNT - counter - 1]}.csv"
        os.rename(new_file_path, os.path.join(MAIN_DATA_PATH, new_file_name))

    print(f"Downloading finished successfully")
    driver.close()


if __name__ == "__main__":
    if os.path.exists(MAIN_DATA_PATH):
        os.rmdir(MAIN_DATA_PATH)
    os.mkdir(MAIN_DATA_PATH)
    download_data(MAIN_DATA_PATH, PAGE_ADDRESS)
