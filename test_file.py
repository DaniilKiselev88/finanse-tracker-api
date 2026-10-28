import requests

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbkBmaW5hbmNlLmNvbSIsInVzZXJfaWQiOjQsImV4cCI6MTc5MzEzNTM4M30.mBKM2ojgSaTjF8BsDgxfoR3ev3j-zZb0qD7sfOjMZW4"

url = "http://127.0.0.1:8000/transactions/"
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}
data = {
    "amount": 5000,
    "type": "income",
    "category": "Зарплата",
    "description": "Первая транзакция"
}

response = requests.post(url, json=data, headers=headers)

print("Статус код:", response.status_code)
print("Ответ:", response.json())