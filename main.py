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
    access_token = file.read().strip()
    print(access_token)
    

def encode_contents(post_list):
    import base64

    file_contents = ""
    # The contents of the README file as a Python string array
    for post in post_list:
        file_contents_string = post['title'] + "[" + post['link'] + "]\n" 
        # Encode the contents of the file as a base64 encoded string
        file_contents_base64 = base64.b64encode(file_contents_string.encode()).decode()
        file_contents += file_contents_base64
        
    print(file_contents)
    return file_contents


# Replace with the owner and repository name
repo_owner = "yebinleee"
repo_name = "Posts-from-my-TistoryBlog"

# The endpoint for the GitHub API to edit a file in a repository
url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/README.md"

file_contents = "bXkgbmV3IHJlYWRtZSBjb250ZW50Cg=="

# The commit message
commit_message = "Update README - new tistory blog posts"

# The headers for the API request
headers = {
    "Authorization": f"Token {access_token}",
    "Accept": "application/vnd.github+json",
    "Content-Type": "application/json"
}

# The payload for the API request
payload = {
    "message": commit_message,
    "content": file_contents
}

# Make the API request to update the file
response = requests.put(url, headers=headers, json=payload)

# Check the status code of the response
if response.status_code == 200:
    print("Successfully updated the README file!")
else:
    print(f"Failed to update the README file. Response: {response.text}")
