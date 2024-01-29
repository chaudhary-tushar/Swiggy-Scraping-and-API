import time
from classes import folders as fols
import pandas as pd
from classes import seldriver as sd
from bs4 import BeautifulSoup
from selenium.common.exceptions import (
    TimeoutException, NoSuchElementException,
    WebDriverException, StaleElementReferenceException,
    ElementNotInteractableException, ElementNotSelectableException,
    ElementNotVisibleException, NoAlertPresentException,
    NoSuchFrameException, NoSuchWindowException,
    SessionNotCreatedException)

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class Restaurant_finder:
    '''This class is to crawl through all the city links
    from city.csv and print them in their named folder'''

    def rest_list(self, urq):
        '''This function takes url as an argument and outputs
        csv files containing: restaurant details/links/prenames'''
        url = urq

        hname_ind = urq.rfind('/')
        hname = urq[hname_ind+1:]
        hname = hname.replace("\n", "")
        H_name = hname.capitalize()
        Driver = sd.Sel_Driver()
        driver = Driver.get_driver()
        print(f"working on {H_name}")
        try:
            driver.get(url)
        except (TimeoutException, NoSuchElementException,
                WebDriverException, StaleElementReferenceException,
                ElementNotInteractableException, ElementNotSelectableException,
                ElementNotVisibleException, NoAlertPresentException,
                NoSuchFrameException, NoSuchWindowException,
                SessionNotCreatedException) as e:
            print(f"{H_name} restaurants not listed 1st")
            driver.quit()
            exp_msg = type(e).__name__
            fault = f"{H_name} + {exp_msg}"
            return fault

        wait = WebDriverWait(driver, 5)

        # wait for the element to be clickable
        # updated on 15 march 2023 since swiggy update changing the label to class
        try:
            element = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='sc-beySbM clsZsT style__TextContainerMain-sc-btx547-3 fObFec']")))   # noqa
        except (TimeoutException, NoSuchElementException,
                WebDriverException, StaleElementReferenceException,
                ElementNotInteractableException, ElementNotSelectableException,
                ElementNotVisibleException, NoAlertPresentException,
                NoSuchFrameException, NoSuchWindowException,
                SessionNotCreatedException) as e:
            print(f"{H_name} restaurants not listed 2nd")
            driver.quit()
            exp_msg = type(e).__name__
            fault = f"{H_name} + {exp_msg}"
            return fault

        # click the element
        element.click()
        try:
            wait = WebDriverWait(driver, 15)
            search_box = driver.find_element(By.XPATH, "//input[@placeholder='Search for area, street name...']")   # noqa
            search_box.send_keys(H_name)
        except (TimeoutException, NoSuchElementException,
                WebDriverException, StaleElementReferenceException,
                ElementNotInteractableException, ElementNotSelectableException,
                ElementNotVisibleException, NoAlertPresentException,
                NoSuchFrameException, NoSuchWindowException,
                SessionNotCreatedException) as e:
            print(f"{H_name} restaurants not listed  3rd")
            driver.quit()
            exp_msg = type(e).__name__
            fault = f"{H_name} + {exp_msg}"
            return fault

        try:
            wait = WebDriverWait(driver, 5)
            results = wait.until(EC.element_to_be_clickable((By.XPATH, "//body[1]/div[1]/main[1]/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/div[2]/div[2]/div[1]")))   # noqa
            results.click()
        except (TimeoutException, NoSuchElementException,
                WebDriverException, StaleElementReferenceException,
                ElementNotInteractableException, ElementNotSelectableException,
                ElementNotVisibleException, NoAlertPresentException,
                NoSuchFrameException, NoSuchWindowException,
                SessionNotCreatedException) as e:
            print(f"{H_name} restaurants not listed 4th")
            driver.quit()
            exp_msg = type(e).__name__
            fault = f"{H_name} + {exp_msg}"
            return fault
        try:
            wait = WebDriverWait(driver, 15)
            element = wait.until(EC.presence_of_element_located((By.XPATH, "//h2[normalize-space()='Popular restaurants near me']")))   # noqa

        except (TimeoutException, NoSuchElementException,
                WebDriverException, StaleElementReferenceException,
                ElementNotInteractableException, ElementNotSelectableException,
                ElementNotVisibleException, NoAlertPresentException,
                NoSuchFrameException, NoSuchWindowException,
                SessionNotCreatedException) as e:
            print(f"{H_name} restaurants not listed  5th")
            driver.quit()
            exp_msg = type(e).__name__
            fault = f"{H_name} + {exp_msg}"
            return fault

        else:
            scroll_pause_time = 1  # You can set your own pause time
            i = 1

            toscroll = True
            while toscroll is True :
                time.sleep(scroll_pause_time)
                try:
                    wait = WebDriverWait(driver, 5)
                    more = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'Show more')]"))) # noqa
                    more.click()
                    toscroll = True
                except: # noqa
                    toscroll = False
                
            # Wait for the search results to load and get the HTML content of the page

            html = driver.page_source
            driver.quit()
            print(f"{H_name} parsed")
            soup = BeautifulSoup(html, 'html.parser')

            # Find all the restaurant names on the page and print them to the console
            fp = fols.Folder()
            link_elements = soup.find_all('a', class_='RestaurantList__RestaurantAnchor-sc-1d3nl43-3 kcEtBq') # noqa
            names = []
            links = []
            for linkd in link_elements:
                links.append(linkd.get('href'))
                names.append(linkd.find('div', class_='sc-beySbM cwvucc').text.strip())
            print(H_name, len(names), len(links))
            file_path1 = fp.getdbfile("det_links", H_name)
            data_dict = {"Details": names, "Links": links}

            # Create a pandas DataFrame from the dictionary
            df = pd.DataFrame(data_dict)

            # Check if the CSV file already exists
            try:
                existing_df = pd.read_csv(file_path1)
            except FileNotFoundError:
                existing_df = pd.DataFrame()

            # Check for duplicate values based on
            # the "Details" and "Links" columns
            existing_names = set(existing_df["Details"]) \
                if not existing_df.empty else set()
            existing_links = set(existing_df["Links"]) \
                if not existing_df.empty else set()
            new_names = set(df["Details"])
            new_links = set(df["Links"])
            new_names_and_links = new_names.union(new_links)
            duplicate_names = new_names_and_links.intersection(existing_names)
            duplicate_links = new_names_and_links.intersection(existing_links)

            # If there are duplicate values, remove them from the new DataFrame
            if len(duplicate_names) > 0 or len(duplicate_links) > 0:
                df = df[~df["Details"].isin(duplicate_names)]
                df = df[~df["Links"].isin(duplicate_links)]

            # Append the new DataFrame to the existing one
            df.to_csv(file_path1, mode="a",
                      index=False, header=existing_df.empty)
