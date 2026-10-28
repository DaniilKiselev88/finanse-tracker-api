import requests

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbkBmaW5hbmNlLmNvbSIsInVzZXJfaWQiOjQsImV4cCI6MTc5MzIxNDQ0MX0.lpF5rwRv4R4_y0dxfjsbUum7nZ_wRcCgDGlTze9W6Bw"

url = "http://127.0.0.1:8000/transactions/"
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}
data = {
    "amount": 500,
    "type": "expense",
    "category": None, # Оставляем пустым для ML
    "description": "Купил бургер в KFC"
}

response = requests.post(url, json=data, headers=headers)

print("Статус код:", response.status_code)
print("Ответ:", response.json())