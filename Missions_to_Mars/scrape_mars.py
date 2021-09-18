from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time


def scrape_info():
    # Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    #scrape news title and paragraph
    url = 'https://redplanetscience.com/'
    browser.visit(url)
    time.sleep(1)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    title = soup.find_all('div', class_='content_title')
    news_title = title[0].get_text()

    paragraph = soup.find_all('div', class_='article_teaser_body')
    news_p = paragraph[0].get_text()

    #scrape feature image
    url = 'https://spaceimages-mars.com/'
    browser.visit(url)
    time.sleep(1)

    browser.links.find_by_partial_text('FULL IMAGE').click()

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    image = soup.find_all('img', class_='fancybox-image')[0]['src']
    featured_image_url = url + image

    #scrape mars facts table
    url = 'https://galaxyfacts-mars.com/'
    table = pd.read_html(url, header=1)[0]
    facts = table.to_html(classes='table table-striped')

    #scrape hemisphere images
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    hemisphere_image_urls = []
    links = browser.links.find_by_partial_text('Hemisphere Enhanced')

    for link in range(len(links)):
        browser.links.find_by_partial_text('Hemisphere Enhanced')[link].click()
        time.sleep(1)
    
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
    
        title = soup.find('h2', class_= 'title').get_text()
        img_url= soup.find_all('a')[3]['href']
    
    
    
        html_dict = {
            'title':title,
            'img_url':img_url
            }
    
        hemisphere_image_urls.append(html_dict)
    
        browser.back()

    # Store data in a dictionary
    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "facts": facts,
        "cerberus_img": hemisphere_image_urls[0]['img_url'],
        "schiaparelli_img": hemisphere_image_urls[1]['img_url'],
        "syrtis_major_img": hemisphere_image_urls[2]['img_url'],
        "valles_marineris_img": hemisphere_image_urls[3]['img_url'],
        "cerberus_title": hemisphere_image_urls[0]['title'],
        "schiaparelli_title": hemisphere_image_urls[1]['title'],
        "syrtis_major_title": hemisphere_image_urls[2]['title'],
        "valles_marineris_title": hemisphere_image_urls[3]['title']
    }

    # Quite the browser after scraping
    browser.quit()

    # Return results
    return mars_data
