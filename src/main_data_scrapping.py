from selenium import webdriver
import os
from xG_data_scrapping import YEARS
import time
import shutil

SEASON_AMOUNT = len(YEARS)
MAIN_DATA_PATH = os.path.join('..', 'main_data')
PAGE_ADDRESS = "https://www.football-data.co.uk/englandm.php"
PATH_TO_CHROME_DRIVER = os.path.join('..', 'chrome_driver', 'chromedriver.exe')
DOWNLOAD_LINK_TEXT = "Premier League"
DOWNLOAD_DEFAULT_DIRECTORY = os.environ.get("DOWNLOAD_DEFAULT_DIRECTORY")


def delete_data(data_dir: str, last_season_counter: int):
    script_path = os.getcwd()
    os.chdir(MAIN_DATA_PATH)

    print("Deleting latest datasets ...")
    for x in range(last_season_counter, SEASON_AMOUNT):
        year = YEARS[x]
        for file_name in os.listdir(data_dir):
            if year in file_name:
                print(f"Deleting dataset [{x-last_season_counter+1}/{SEASON_AMOUNT-last_season_counter}]")
                os.remove(file_name)
                break

    os.chdir(script_path)
    print("Deleting finished successfully")


def find_last_season(path: str) -> str:
    years = list(map(lambda x: x[7:11], os.listdir(path)))
    return max(years)


def download_data(download_dir: str, page_address: str, last_season_counter: int = 0):

    driver = webdriver.Chrome(PATH_TO_CHROME_DRIVER)

    # get request to target the site
    driver.get(page_address)

    # finding all links with text "Premier League" on page
    links = driver.find_elements_by_link_text(DOWNLOAD_LINK_TEXT)

    print(f"Downloading started")

    # range(last_season_counter, SEASON_AMOUNT) takes care of downloading only new season if main_data file is not empty
    # else script downloads all season (last_season_counter = 0 by default)
    for counter in range(SEASON_AMOUNT-last_season_counter):
        print(f"Downloading dataset [{counter + 1} / {SEASON_AMOUNT-last_season_counter}]")
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


def main():
    if os.path.exists(MAIN_DATA_PATH):
        last_season = find_last_season(MAIN_DATA_PATH)
        last_season_counter = YEARS.index(last_season)
        delete_data(MAIN_DATA_PATH, last_season_counter)
        download_data(MAIN_DATA_PATH, PAGE_ADDRESS, last_season_counter)
    else:
        script_path = os.getcwd()
        os.chdir("..")
        os.mkdir("main_data")
        os.chdir(script_path)
        download_data(MAIN_DATA_PATH, PAGE_ADDRESS)


if __name__ == "__main__":
    main()

