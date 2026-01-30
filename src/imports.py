from playwright.sync_api import sync_playwright
from lxml import html
from bs4 import BeautifulSoup
import feedparser
import yaml
import requests
import json
from typing import TypedDict, List
from groq import Client
import os
import dotenv


class Article(TypedDict):
    title: str
    link: str
    Category: List[str]
    published: str
    summary: str
    content: str
    ai_content: str
