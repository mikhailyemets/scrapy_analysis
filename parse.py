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
