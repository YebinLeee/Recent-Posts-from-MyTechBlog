import requests
from bs4 import BeautifulSoup
import json
import base64

# Reference: https://docs.github.com/ko/rest/repos/contents?apiVersion=2022-11-28#create-or-update-file-contents
# Reference: https://truman.tistory.com/108

# Make a request to the website
response = requests.get('https://dream-and-develop.tistory.com')

# Parse the HTML content of the page
soup = BeautifulSoup(response.content, 'html.parser')

post_titles = soup.find_all('strong', class_='tit_post')
post_links = soup.find_all('a', class_='link_post')
post_protected = soup.find_all('p', class_='txt_post')
    
# Create a list to store the post title and link
post_list = []

# Iterate over both lists of post titles and links
for title, link, protected in zip(post_titles, post_links, post_protected):
    post = {
        'title': title.text,
        'link': 'https://dream-and-develop.tistory.com' + str(link.get('href')),
        'protected': protected.text,
    }
    post_list.append(post)


with open('data', 'r') as file:
    access_token = file.read().strip()
    print(access_token)
    

def encode_contents(post_list):
    file_contents = ""
   
    for post in post_list:
        if '보호되어 있는 글입니다.' in str(post['protected']):
            print(post['protected'])
            continue
        file_contents_string = "- [" + post['title'] + "]" + "(" + post['link'] + ")\n" 
        
        file_contents += file_contents_string
        
    file_contents_base64 = base64.b64encode(file_contents.encode()).decode()
    return file_contents_base64


# Replace with the owner and repository name
repo_owner = "yebinleee"
repo_name = "Posts-from-my-TistoryBlog"
file_name = "README.md"

# The endpoint for the GitHub API to edit a file in a repository
endpoint = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_name}"
url = f"https://api.github.com/repos/{repo_name}/contents/{file_name}"



def get_file_sha():
    headers_for_get = {
        "Authorization": f"Token {access_token}",
    }

    # Make the GET request to get the file
    get_response = requests.get(endpoint, headers=headers_for_get)
    print(get_response.status_code)

    # Check if the request was successful
    if get_response.status_code == 200:
        # Get the SHA of the file
        previous_file_contents = get_response.json()
        print(previous_file_contents)
        
        # Get the SHA of the file
        file_sha = previous_file_contents["sha"]

        # print("SHA of file:", file_sha)
        print('successfully got sha of the file')
    else:
        print("Failed to get file")
        # print("Response status code:", response.status_code)
        # print("Response text:", response.text)
        
    return file_sha



def put_new_contents():
    file_contents = encode_contents(post_list)
    
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
    response = requests.put(endpoint, headers=headers, json=payload)

    # Check the status code of the response
    if response.status_code == 200:
        print("Successfully updated the README file!")
    else:
        print(f"Failed to update the README file. Response: {response.text}")
    
def patch_new_contents():
    file_contents = encode_contents(post_list)

    # The commit message
    commit_message = "Update README - new tistory blog posts"

    # The headers for the API request
    headers = {
        "Authorization": f"Token {access_token}",
        "Accept": "application/vnd.github+json",
        "Content-Type": "application/json"
    }
    
    file_sha = get_file_sha()

    # The payload for the API request
    payload = {
        "message": commit_message,
        "content": file_contents,
        "sha": file_sha
    }

    # Make the API request to update the file
    # patch_response = requests.patch(url, headers=headers, data=json.dumps(payload))
    patch_response = requests.put(endpoint, headers=headers, json=payload)

    # Check the status code of the response
    if patch_response.status_code == 200:
        print("File successfully updated")
    else:
        print("Failed to update file")
        print("Response status code:", patch_response.status_code)
        print("Response text:", patch_response.text)
        
        
        
patch_new_contents()