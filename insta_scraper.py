from selenium import webdriver
import time, urllib.request, requests, os
# launch Chrome and navigate to Instagram page
driver = webdriver.Chrome()
driver.get("https://www.instagram.com/funnywhimsical/")
# scroll to the bottom of the page
lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
match=False
while(match==False):
    lastCount = lenOfPage
    time.sleep(3)
    lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    if lastCount==lenOfPage:
        match=True
# find all links on the page and if they match '/p' append to list named posts
posts = []
links = driver.find_elements_by_tag_name('a')
for link in links:
    post = link.get_attribute('href')
    if '/p/' in post:
      posts.append( post )
print( posts )
# create download directory
if not os.path.exists('Downloads'):
    os.makedirs('Downloads')
# get url of image or video
download_url = ''
for post in posts:
    headers = {'User-Agent': 'Mozilla'}
    r = requests.get('{}?__a=1'.format( post ), headers=headers)
    data = r.json()['graphql']['shortcode_media']
    shortcode = data['shortcode']
    is_video = data['is_video']
    if is_video:
        download_url = data['video_url']
        urllib.request.urlretrieve(download_url, 'Downloads/{}.mp4'.format(shortcode))
    else:
        download_url = data['display_url']
        urllib.request.urlretrieve(download_url, 'Downloads/{}.jpg'.format(shortcode))
    print(download_url)