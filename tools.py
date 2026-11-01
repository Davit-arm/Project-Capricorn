from datetime import datetime
import subprocess
import requests
import os
from dotenv import load_dotenv
load_dotenv()

def get_current_time():
    return datetime.now().strftime("%H:%M:%S")

def get_current_date():
    return datetime.now().strftime("%Y-%m-%d")

def open_app(app):
    try:
        subprocess.Popen(app.lower())
    except Exception as e:
        print(f'Error opening {app}: {e}')

def search_web(query: str):
    try:
        response = requests.get('https://api.search.brave.com/res/v1/web/search',
                     headers={'X-Subscription-Token': os.getenv('brave')},
                     params={'q':query,
                             'count':5},
                    timeout=10)
        data = response.json()
        response.raise_for_status()
        results = []
        for item in data.get('web',{}).get('results',[]):
            results.append({
                'title':item['title'],
                'url':item['url'],
                'description':item['description']
            })
        return results
    except Exception as e:
        print(f'Error has occured while searching the web: {e}')

