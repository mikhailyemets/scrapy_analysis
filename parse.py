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
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options
    )
    wait = WebDriverWait(driver, 20)
    driver.get(url)

    while True:
        try:
            load_more_button = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "div.more-btn > a"))
            )
            driver.execute_script(
                "arguments[0].scrollIntoView(true);", load_more_button
            )
            if load_more_button.is_displayed() and load_more_button.is_enabled():
                logging.info("Clicking 'Load More' button")
                load_more_button.click()
                time.sleep(2)
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(1)
                wait.until(
                    EC.presence_of_all_elements_located(
                        (By.CSS_SELECTOR, "li.l-vacancy")
                    )
                )
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


def extract_technologies(text: str) -> List[str]:
    """
    Extracts a list of technologies mentioned in a given text.

    Args:
        text (str): The text to search for technologies.

    Returns:
        list: A list of technologies found in the text.
    """
    keywords_found = []
    for keyword in keywords:
        if keyword.lower() in text.lower():
            keywords_found.append(keyword)
    return keywords_found


async def parse_job_details(session: ClientSession, job_link: str) -> List[str]:
    """
    Fetches and parses job details from a job listing page asynchronously.

    Args:
        session (ClientSession): The aiohttp client session.
        job_link (str): The URL of the job listing page.

    Returns:
        list: A list of technologies mentioned in the job listing.
    """
    page_source = await fetch_page(session, job_link)
    soup = BeautifulSoup(page_source, "html.parser")
    vacancy_description = soup.get_text()
    if vacancy_description:
        technologies = extract_technologies(vacancy_description)
        logging.info(f"Technologies for {job_link}: {technologies}")
        return technologies
    else:
        logging.warning(f"No description found for {job_link}")
        return []


async def main():
    """
    Main function to orchestrate the loading, fetching, and processing of job listings.
    """
    start_url = "https://jobs.dou.ua/vacancies/?category=Python"
    page_source = load_all_vacancies(start_url)
    soup = BeautifulSoup(page_source, "html.parser")

    job_links = [a["href"] for a in soup.select("a.vt")]
    logging.info(f"Found {len(job_links)} job links")

    ssl_context = ssl.create_default_context(cafile=certifi.where())
    async with ClientSession(connector=TCPConnector(ssl=ssl_context)) as session:
        async with aio_open(
            "vacancies_technologies.csv", "w", newline="", encoding="utf-8"
        ) as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=["technologies"])
            await writer.writeheader()

            tasks = [parse_job_details(session, job_link) for job_link in job_links]
            results = await asyncio.gather(*tasks)

            for technologies in results:
                if technologies:
                    await writer.writerow({"technologies": technologies})

        logging.info(
            f"Technologies for all vacancies written to vacancies_technologies.csv"
        )


if __name__ == "__main__":
    asyncio.run(main())
