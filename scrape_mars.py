# Import dependencies
import time
import requests
from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
from selenium import webdriver

# Create function called 'scrape' to execute all scraping code from mission_to_mars.ipynb
def scrape():
    
    # Create a dictionary to hold scraped data
    mars_dict = {}
    
    ### NASA Mars News ###
    
    # URL to scrape
    url = 'https://mars.nasa.gov/news/'
    
    # Launch chromedriver
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    browser.visit(url)
    
    # Retrieve html from URL
    html = browser.html
    
    # Parse html with BeautifulSoup
    soup = bs(html, 'html.parser')
    # results = soup.find_all('li', class_='slide')
    news_title = soup.find(class_='content_title').get_text(strip=True)
    news_p = soup.find(class_='article_teaser_body').get_text(strip=True)
    
    # Add the news data dict
    mars_dict['news_title'] = news_title
    mars_dict['news_p'] = news_p
    
    # Exit browser session
    # browser.quit()
    
    ### JPL Mars Space Images - Featured Image ###
    
    # Launch chromedriver 
    # executable_path = {'executable_path': 'chromedriver.exe'}
    # browser = Browser('chrome', **executable_path, headless=False)
    
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
    mars_dict['featured_image'] = featured_image
    
    # Exit browser session
    # browser.quit()
    
    ### Mars Weather ###
    
    # Retrieve requests from Twitter
    twitter_url = 'https://twitter.com/marswxreport?lang=en'
    twitter_html = requests.get(twitter_url)
    
    # Parse with BeautifulSoup
    twitter_soup = bs(twitter_html.text, 'html.parser')
    
    # Find most recent weather tweet
    mars_weather = twitter_soup.find(class_='tweet-text').get_text()
    
    # Add weather data to dictionary
    mars_dict['mars_weather'] = mars_weather
    
    ### Mars Facts ###
    
    # Read html facts    
    facts_url = 'https://space-facts.com/mars/'
    data = pd.read_html(facts_url)
    
    # Convert to pandas dataframe then to html
    facts_df = data[0]
    facts_df.set_index(0, inplace=True)
    facts_df.index.names = [None]
    facts_df.columns = ['']
    facts_table = facts_df.to_html()
    
    # Add table to list
    mars_dict['facts_table'] = facts_table
    
    ### Mars Hemispheres ###
    
    # Launch chromedriver
    # executable_path = {'executable_path': 'chromedriver.exe'}
    # browser = Browser('chrome', **executable_path, headless=False)
    
    # URL to scrape
    img_base_url = 'https://astrogeology.usgs.gov'
    img_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    
    # Visit URL
    browser.visit(img_url)
    img_html = browser.html
    
    # Parse with BeautifulSoup
    img_soup = bs(img_html, 'html.parser')

    # Create a list to store results

    hemispheres = img_soup.select('div.item')
    mars_hemispheres = []


    for hemisphere in hemispheres:
        title = (hemisphere.find('h3').text).replace(' Enhanced', '')
            
        #click the hemisphere
        browser.click_link_by_partial_text(title)
        
        #make new soup of that page
        soup = bs(browser.html, 'html.parser')
        
        #find the full image
        full = soup.find('a', text='Sample')
        
        #get the img url
        img_url = full['href']
        
        #make a dict and append to the list
        mars_hemispheres.append({'title': title, 'img_url': img_url})
        
        #go back 
        browser.back()

    #close browser
    browser.quit()    
                

    # Add hemisphere data to dictionary list
    mars_dict['mars_hemispheres'] = mars_hemispheres


    return(mars_dict)
    
    
    
    
    
    

    

