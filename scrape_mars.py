# Import dependencies
import time
import requests
from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
from selenium import webdriver

# Create function called 'scrape' to execute all scraping code from mission_to_mars.ipynb
def scrape():
    
    # Create a list to hold scraped data
    mars_data = []
    
    ###NASA Mars News###
    
    # Launch chromedriver
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    
    # URL to scrape
    url = 'https://mars.nasa.gov/news/'
    
    # Retrieve html from URL
    html = browser.html
    
    # Parse html with BeautifulSoup
    soup = bs(html, 'html.parser')
    results = soup.find_all('li', class_='slide')
    news_title = soup.find('div', class_='content_title')
    news_p = soup.find('div', class_='article_teaser_body')
    
    

    

