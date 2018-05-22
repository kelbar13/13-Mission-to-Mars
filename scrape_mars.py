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
    
    ### NASA Mars News ###
    
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
    
    # Add the news data to list of dictionaries
    mars_data.append({'title': 'Latest Mars News', 'header': news_title, 'paragraph': news_p, 'url': url})
    
    # Exit browser session
    browser.quit()
    
    ### JPL Mars Space Images - Featured Image ###
    
    # Launch chromedriver 
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    
    # URL to scrape
    featured_image_base_url = 'https://www.jpl.nasa.gov'
    featured_image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    
    # Visit the URL
    browser.visit(featured_image_url)
    featured_image_html = browser.html
    
    # Parse html with BeautifulSoup
    featured_image_soup = bs(featured_image_html, 'html.parser')
    
    # Find full version of featured image
    featured_image = featured_image_base_url + featured_image_soup.find(id='full_image')['data-fancybox-href']
    
    # Add the image data to list
    mars_data.append({'title': 'Featured Mars Image', 'image_url': featured_image_url})
    
    # Exit browser session
    browser.quit()
    
    ### Mars Weather ###
    
    # Retrieve requests from Twitter
    twitter_url = 'https://twitter.com/marswxreport?lang=en'
    twitter_html = requests.get(twitter_url)
    
    # Parse with BeautifulSoup
    twitter_soup = bs(twitter_html.text, 'html.parser')
    
    # Find most recent weather tweet
    mars_weather = twitter_soup.find(class_='TweetTextSize--normal')
    
    # Add weather data to list
    mars_data.append({'title': 'Current Weather on Mars', 'paragraph': mars_weather, 'url': twitter_url})
    
    ### Mars Facts ###
    
    # Read html facts    
    facts_url = 'https://space-facts.com/mars/'
    data = pd.read_html(facts_url)
    
    # Convert to pandas dataframe then to html
    facts_df = data[0]
    facts_table = facts_df.to_html()
    
    # Add table to list
    mars_data.append({'title': 'Facts About Mars', 'table': facts_table, 'url': facts_url})
    
    ### Mars Hemispheres ###
    
    # Launch chromedriver
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    
    # URL to scrape
    img_base_url = 'https://astrogeology.usgs.gov'
    img_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    
    # Visit URL
    browser.visit(img_url)
    img_html = browser.html
    
    # Parse with BeautifulSoup
    img_soup = bs(img_html, 'html.parser')

    # Create a list to store results
    mars_hemispheres = []

    hem_img = img_soup.find('div', class_='result-list')
    hemispheres = hem_img .find_all('div', class_='item')

    # Loop to find all hemispheres
    for hemisphere in hemispheres:
        title = hemisphere.find('h3').text
        title = title.replace('Enhanced', '')
        img_url = hemisphere.find('a')['href']
        link_url = 'https://astrogeology.usgs.gov' + img_url    
        browser.visit(link_url)
        html = browser.html
        soup = bs(html, 'html.parser')
        downloads = soup.find('div', class_='downloads')
        img = downloads.find('a')['href']
        mars_hemispheres.append({'title': title, 'img_url': img})

    # Add hemisphere data to dictionary list
    mars_data.append({'title': title, 'url': img_url})
    
    # Exit browser
    browser.quit()
    
    for item in mars_data:
        for key, value in item.items():
            print(key, ': ', value)
            print()

    return(mars_data)
    
    
    
    
    
    

    

