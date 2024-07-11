import asyncio
from typing import List
from aiohttp import ClientSession, TCPConnector
from aiofiles import open as aio_open
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import logging
import csv
import ssl
import certifi
import time

logging.basicConfig(level=logging.INFO)

keywords = [
    "Python", "Django", "Flask", "SQL", "NoSQL", "JavaScript",
    "React", "AWS", "Docker", "Kubernetes", "Celery", "Redis",
    "PostgreSQL", "MySQL", "MongoDB", "GraphQL", "REST", "SOAP",
    "Pandas", "NumPy", "SciPy", "TensorFlow", "PyTorch", "Machine Learning",
    "Deep Learning", "NLP", "Computer Vision", "Git", "GitHub", "Bitbucket",
    "CI/CD", "Jenkins", "GitLab", "Ansible", "Terraform", "Linux", "Unix",
    "Agile", "Scrum", "Kanban", "Microservices", "Serverless", "FastAPI",
    "Bottle", "Pyramid", "SQLAlchemy", "Alembic", "Jupyter", "Notebook", "ETL",
    "Hadoop", "Spark", "Airflow", "Azure", "GCP", "Heroku", "OpenShift",
    "Selenium", "BeautifulSoup", "Scrapy", "Pytest", "UnitTest", "Mock",
    "Asyncio", "Multithreading", "Multiprocessing"
]


def load_all_vacancies(url: str) -> str:
    """
    Uses Selenium to load all vacancies by repeatedly clicking the 'Load More' button.

    Args:
        url (str): The URL of the job listing page.

    Returns:
        str: The page source of the fully loaded job listing page.
    """
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    wait = WebDriverWait(driver, 20)
    driver.get(url)

    while True:
        try:
            load_more_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.more-btn > a")))
            driver.execute_script("arguments[0].scrollIntoView(true);", load_more_button)
            if load_more_button.is_displayed() and load_more_button.is_enabled():
                logging.info("Clicking 'Load More' button")
                load_more_button.click()
                time.sleep(2)
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(1)
                wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li.l-vacancy")))
            else:
                logging.info("'Load More' button is not active or visible")
                break
        except Exception as e:
            logging.error(f"Exception: {e}")
            break

    page_source = driver.page_source
    driver.quit()
    return page_source


async def fetch_page(session: ClientSession, url: str) -> str:
    """
    Fetches a web page asynchronously.

    Args:
        session (ClientSession): The aiohttp client session.
        url (str): The URL of the web page to fetch.

    Returns:
        str: The content of the web page.
    """
    async with session.get(url) as response:
        return await response.text()
