import requests
import fake_useragent
import time
import re
import json as JSON
from bs4 import BeautifulSoup

agent = fake_useragent.UserAgent().random
session = requests.Session()

session.get("https://www.elmenus.com/")

cookies = session.cookies.get_dict()
headers = {

    "Authorization": f"Bearer {cookies['Authorization']}",
    "Content-Type": "application/json",
    "User-Agent": agent,
    "Accept": "application/json",
    "Referer": "https://www.elmenus.com/",   

    "Client-Model": "WEB",
    "Client-Version": "5",

    "Device-ID": cookies['payload'],
    "Device-Model": agent,

    "X-Client-Id": "0417b144-0f3f-11e8-87cc-0242ac110002",
    "X-Device-Id": cookies['payload'],

    "lang": "EN",
    "userarea": "",
    "userCompany": "",
    "userzone": "",
}


def _extract_js_object(js_code):
    cnt = 0
    flag = False 
    json_string = []

    for i in js_code:
        if i == '{':
            cnt += 1
            flag = True
        elif i == '}':
            cnt -= 1
        
        if flag:
            json_string.append(i)

        if flag and cnt == 0:
            break

    return ''.join(json_string)

def fetch_categories_and_regions():
    
    r = session.get("https://www.elmenus.com/cairo/delivery/sheikh-zayed/dish-koshary/features-order-online", headers=headers)

    if r.status_code != 200:
        return r
    
    soup = BeautifulSoup(r.text, 'html.parser')
    script = soup.find(id='script-should-remove')
    if not script:
        r.status_code = -1
        return r
    
    js_data = _extract_js_object(script.text).split('\n')

    json_string = js_data[5][24:-1] 
    json = JSON.loads(json_string)

    with open("dataset/categories.json", 'w') as categories_file:
       JSON.dump({'categories': json}, categories_file, indent=4, ensure_ascii=False)

    json_string = js_data[4][16:-1]    
    json = JSON.loads(json_string)
    
    with open("dataset/regions.json", 'w') as regions_file:
       JSON.dump({'regions': json}, regions_file, indent=4, ensure_ascii=False)

    return r

def fetch_zone_restaurants(category_id, area_id, zone_id,
                       page=1, page_size=10):

    return session.get("https://www.elmenus.com/2.0/discovery/delivery/search", 
                        headers=headers,
                        params={
                            'page': page,
                            'pageSize': page_size,
                            'category': category_id,
                            'sort': "POPULAR",
                            'area': area_id,
                            'zone': zone_id
                            })
    
def fetch_menu(restaurant_branch_code):
    
    return session.get(f"https://www.elmenus.com/api/steering/restaurant/v1/branches/{restaurant_branch_code}/menu",
                        headers=headers)

