# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    
    news_title, news_paragraph = mars_news(browser)
    
    # Run all scraping functions and store results in dictionary
    data = {
      "news_title": news_title,
      "news_paragraph": news_paragraph,
      "featured_image": featured_image(browser),
      "facts": mars_facts(),
      "last_modified": dt.datetime.now(),
      "hemispheres": hemi_data(browser)  
    }

    # Stop webdriver and return data
    browser.quit()
    return data

def mars_news(browser):
    
    # Scrape Mars News
    # Visit the Mars news site
    url = 'https://redplanetscience.com'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    
    except AttributeError:
        return None, None
    
    return news_title, news_p

def featured_image(browser):

    # Scrape Mars images
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    
    except AttributeError:
        return None
 
    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    
    return img_url

def mars_facts():
    # Add try/except for error handling
    try:
        # use 'read_html' to scrape the facts table into a DataFrame
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)
    print("Done with Mars facts")

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html(classes="table table-striped")


def hemi_data(browser):
    
    # Scrape hemisphere title and image url
    # Visit the main page URL 
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    # Parse the resulting html with soup
    html = browser.html
    hemisphere_main_page = soup(html, 'html.parser')
    
    # Create a list to hold the images and titles.
    hemisphere_image_urls = []
    
    
    # Retrieve the image urls and titles for each hemisphere.
    hemisphere_links = hemisphere_main_page.select("div.item [href]")
    hemisphere_urls = [link['href'] for link in hemisphere_links]
    
    # Since each link appears twice in the element, we will only use every other one
    for i in range(1, len(hemisphere_urls), 2):
        #visit_and_pull_page(hemisphere_links[i]['href'])
        hemisphere = {}
        full_url = url + hemisphere_urls[i]
        browser.visit(full_url)
        hemisphere_obj = soup(browser.html, 'html.parser')
        hemi_hi_res_url = hemisphere_obj.find('a',href=True,text='Sample').get('href')
        hemisphere_title = hemisphere_obj.find('h2', class_ = 'title').text
        hemisphere["img_url"] = url + hemi_hi_res_url
        hemisphere["title"] = hemisphere_title
        hemisphere_image_urls.append(hemisphere)
        browser.back()
    
    # Print the list that holds the dictionary of each image url and title.
    return hemisphere_image_urls


if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())


