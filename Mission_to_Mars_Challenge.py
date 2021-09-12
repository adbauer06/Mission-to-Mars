#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


# In[2]:


# Set the executable path and initialize Splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# ### Visit the NASA Mars News Site

# In[3]:


# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# In[4]:


# Convert the browser html to a soup object
html = browser.html
news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('div.list_text')


# In[5]:


slide_elem.find('div', class_='content_title')


# In[6]:


# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# In[7]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### JPL Space Images Featured Image

# In[8]:


# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# In[9]:


# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[10]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')
img_soup


# In[11]:


# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# In[12]:


# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# ### Mars Facts

# In[13]:


df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df


# In[14]:


df.to_html()


# ## D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres

# In[15]:


# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'
browser.visit(url)

hemisphere_main_page = soup(browser.html, 'html.parser')
hemisphere_main_page


# In[16]:


# # This takes in a partial url (link, which is relative to global variable url) and pulls all the data we need from that page...
# def visit_and_pull_page(link):
#     hemisphere = {}
#     full_url = url + link
#     browser.visit(full_url)
#     hemisphere_obj = soup(browser.html, 'html.parser')
#     hemisphere_title = hemisphere_obj.find('h2', class_ = 'title').text
#     hemisphere_url = hemisphere_obj.find('a',href=True,text='Sample').get('href')
#     hemisphere["img_url"] = url + hemisphere_url
#     hemisphere["title"] = hemisphere_title
#     hemisphere_image_urls.append(hemisphere)
#     #print(hemisphere)


# In[17]:


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []
    
# 3. Write code to retrieve the image urls and titles for each hemisphere.
#hemisphere_links = hemisphere_main_page.select('.itemLink')
hemisphere_links = hemisphere_main_page.select("div.item [href]")
hemisphere_urls = [link['href'] for link in hemisphere_links]
print(hemisphere_urls)

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
    


# In[18]:


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# In[19]:


# 5. Quit the browser
browser.quit()


# In[ ]:





# In[ ]:




