import requests

url = "https://pan-card-verification1.p.rapidapi.com/v3/tasks/sync/verify_with_source/ind_pan"

def verify(pan):
    payload = {
        "task_id": "74f4c926-250c-43ca-9c53-453e87ceacd1",
        "group_id": "8e16424a-58fc-4ba4-ab20-5bc8e7c3c41e",
        "data": { "id_number": pan }
    }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": "327fd8beb9msh8a441504790e80fp142ea8jsnf74b9208776a",
        "X-RapidAPI-Host": "pan-card-verification1.p.rapidapi.com"
    }

    response = requests.post(url, json=payload, headers=headers)

    print(response.json())

    return response.json()