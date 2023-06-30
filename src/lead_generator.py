import asyncio
import logging
import os
import re

import django
from django.contrib.auth import get_user_model

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.app.settings')
django.setup()

import time
from typing import Iterator
from contextlib import suppress
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver import Keys, ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from django.db import DatabaseError
from lead_generator.models import Lead
from channels.db import database_sync_to_async
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor
from itertools import chain


User = get_user_model()


class Scraper:

    def __init__(self, keyword: str, location: str) -> None:
        self.keyword = keyword
        self.location = location
        self.chrome_options = Options()
        # self.chrome_options.add_argument("--headless")
        self.chrome_options.add_argument('--start-maximized')
        self.driver = webdriver.Chrome(
            options=self.chrome_options,
            service=ChromeService(
                executable_path=ChromeDriverManager().install())
        )
        self.url = 'https://www.google.com/maps'
        self.xpath = '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]'

    def collection_leads(self) -> Iterator:
        """Collection of leads"""
        self.driver.get(self.url)
        logging.info('Starting collection leads')
        try:

            search_input = self.driver.find_element(By.ID, 'searchboxinput')
            search_input.clear()
            search_input.send_keys(self.keyword + ' ' + self.location)
            search_input.send_keys(Keys.ENTER)
            time.sleep(1)

            actions = ActionChains(self.driver)
            actions.move_by_offset(50, 200).perform()
            time.sleep(2)
            actions.click().perform()

            elements = []
            for _ in range(0, 10):
                self.driver.find_element(By.XPATH, self.xpath).send_keys(Keys.END)
                elements.extend(self.driver.find_elements(By.CLASS_NAME, 'hfpxzc'))

            elements = [element.get_attribute('href') for element in elements][:4]

            with ThreadPoolExecutor(max_workers=3) as executor:
                results = executor.map(self.concurrent_poll, [elements[:len(elements)//2], elements[len(elements)//2:]])
                return results

        finally:
            self.driver.quit()

    def concurrent_poll(self, elements: list) -> list:
        results = []

        for element in tqdm(elements):
            dict_results = {}
            self.driver.get(element)
            time.sleep(3)

            dict_results['name'] = self.driver.find_element(By.CLASS_NAME, 'DUwDvf').text.strip()
            dict_results['keyword'] = self.keyword
            dict_results['location'] = self.location

            sub_elements = [item.text for item in self.driver.find_elements(By.CLASS_NAME, 'rogA2c')]
            url = [item.get_attribute('href') for item in self.driver.find_elements(By.CLASS_NAME, 'CsEnBe')
                   if item.get_attribute('href')]
            sub_elements.extend(url)

            for index, sub_element in enumerate(sub_elements):
                if sub_element.startswith('http'):
                    dict_results['url'] = sub_elements.pop(index)
                if re.search(r'\d{5}$', sub_element):
                    dict_results['address'] = sub_elements.pop(index)

                if re.findall(r'\d+\s+\d+', sub_element):
                    dict_results['phone_number'] = sub_elements.pop(index)

            results.append(dict_results)

        return results

    def save_database(self):
        """Save the information in database"""

        leads = self.collection_leads()

        for lead in chain(*leads):
            with suppress(DatabaseError):
                Lead.objects.create(
                    **lead
                )
        logging.info('Leads saved successfully')


if __name__ == '__main__':
    logging.basicConfig(
        level='INFO'.upper(),
        format='%(asctime)s | %(levelname)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    async def scrape_and_save(scraper):
        await database_sync_to_async(scraper.save_database)()

    @database_sync_to_async
    def users():
        return list(User.objects.filter(is_active=True).values())

    async def main():
        queryset = await users()
        setting = set((qs['keyword'], qs['location']) for qs in queryset)

        scrapers = [Scraper(keyword, location) for keyword, location in setting if keyword is not None]

        if scrapers:
            tasks = [
                asyncio.create_task(scrape_and_save(scraper)) for scraper in scrapers
            ]

            await asyncio.gather(*tasks)

    asyncio.run(main())
