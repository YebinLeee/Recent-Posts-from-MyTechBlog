import requests

headers = {
    'Authorization': 'TOKEN',
    'Content-Type': 'application/json'
}

data = {
    'message': 'Update README with latest post title',
    'content': post_list.encode('base64')
}

response = requests.put('https://api.github.com/repos/yebinleee/posts-from-my-tistory-blog/contents/README.md', headers=headers, json=data)
print(response)