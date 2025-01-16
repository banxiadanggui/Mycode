import requests

url='https://api.github.com/search/repositories?q=language:python&sort=stars'
r=requests.get(url)
print("start code:",r.status_code)

response_dict=r.json()
print("total repositories:",response_dict['total_count'])

repo_dicts=response_dict['items']
print("repositiories returned:",len(repo_dicts))

repo_dict=repo_dicts[0]
print("\nkeys:",len(repo_dict))
for key in sorted(repo_dict.keys()):
    print(key)

print(response_dict.keys())