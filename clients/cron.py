import kronos
import requests


@kronos.register('* * * * *')
def import_hackers_data():
    response = requests.get("http://127.0.0.1:8000/clients/hackers/import")
    print(response)
