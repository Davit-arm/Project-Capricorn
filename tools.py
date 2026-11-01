from datetime import datetime
import requests
import os
import shutil
from dotenv import load_dotenv
load_dotenv()

START_MENU_DIRS = [
    os.path.expandvars(r"%ProgramData%\Microsoft\Windows\Start Menu\Programs"),
    os.path.expandvars(r"%AppData%\Microsoft\Windows\Start Menu\Programs"),
]

def get_current_time():
    return datetime.now().strftime("%H:%M:%S")

def get_current_date():
    return datetime.now().strftime("%Y-%m-%d")

def find_app(name):
    name = name.lower().strip()
    found = shutil.which(name)
    if found:
        return found
    for DIR in START_MENU_DIRS:
        for root, dirs, files in os.walk(DIR):
            for file in files:
                if file.lower().endswith(('.lnk','.exe')) and name in file.lower():
                    return os.path.join(root, file)

def open_app(app):
    try:
        app_path = find_app(app)
        os.startfile(app_path)
        return f'Opening {app}...'
    except Exception as e:
        print(f'Error opening {app}: {e}')
        return f'Error opening {app}: {e}'

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

