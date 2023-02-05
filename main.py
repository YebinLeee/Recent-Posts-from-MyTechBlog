import requests
from bs4 import BeautifulSoup

# Reference: https://truman.tistory.com/108

# Make a request to the website
response = requests.get('https://dream-and-develop.tistory.com')

# Parse the HTML content of the page
soup = BeautifulSoup(response.content, 'html.parser')

# Find all elements with the tag name "tit_post"
post_titles = soup.find_all('strong', class_='tit_post')

# Find all elements with the tag name "link_post"
post_links = soup.find_all('a', class_='link_post')

# Create a list to store the post title and link
post_list = []

# Iterate over both lists of post titles and links
for title, link in zip(post_titles, post_links):
    post = {
        'title': title.text,
        'link': 'https://dream-and-develop.tistory.com' + str(link.get('href'))
    }
    post_list.append(post)

# Print the list of post titles and links
print(post_list)

for post in post_list:
    print(post['title'])
    print(post['link'], end='\n\n')


latest_post = post_list[0]['title']

with open('data', 'r') as file:
    secret_key = file.read().strip()
    print(secret_key)
    
headers = {
    'Authorization': secret_key,
    'Content-Type': 'application/json'
}

data = {
    'message': 'Update README with latest post title',
    'content': latest_post
}

response = requests.put('https://api.github.com/repos/YebinLeee/Posts-from-my-TistoryBlog/README.md', headers=headers, json=data)
print(response)