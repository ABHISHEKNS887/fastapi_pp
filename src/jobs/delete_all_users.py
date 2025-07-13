import requests
import os

permission = input("Do you have admin access to delete all users. type (Y/N): " )
if permission == 'Y':
    url = "http://localhost:8000/users/delete_all"
    headers = {"Autorization": "Bearer f{ADMIN_TOCKEN}"}
    try:
        response = requests.delete(url, headers=headers)
        print(response.json())
    except Exception as e:
        raise e