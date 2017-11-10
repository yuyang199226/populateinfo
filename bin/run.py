import os
import sys
import json
from src import q_authors,q_poem
import requests
from conf import settings


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath('__file__')))

sys.path.append(BASE_DIR)

if __name__ == '__main__':
    authors_path = os.path.join(BASE_DIR, 'db/authors.json')
    poem_path = os.path.join(BASE_DIR, 'db/poem.json')
    # author_data = q_authors.main()
    # author_data = json.dumps(author_data)
    poem_message = q_poem.get_save_poem()
    # 
    # with open(authors_path,'w',encoding='utf-8') as f:
    #     f.write(author_data)
    # with open(authors_path,'rb',encoding='utf-8') as f:
    #     author_data=json.load(f)
    # try:
    #     res = requests.post(url=settings.API,json=author_data)
    # except:
    #     print(res.status_code)
    # requests.post(url=settings.API,json={"aaa":111})

    with open(poem_path, 'w', encoding='utf8')as f:
        f.write(json.dumps(poem_message))