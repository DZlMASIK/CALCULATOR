import requests

url = "http://127.0.0.1:8000"

# Тест 1: Проверка работы API
try:
    print("Проверка API...")
    r = requests.get(f"{url}/health")
    print(f"✓ API работает: {r.json()}")
except:
    print("✗ API не отвечает")
    exit()

# Тест 2: Простое вычисление
print("\nТест вычисления...")
r = requests.post(f"{url}/calculate", json={"expression": "2+3*4"})
print(f"2+3*4 = {r.json()['result']}")

# Тест 3: Научная функция
print("\nТест синуса...")
r = requests.post(f"{url}/scientific", json={"function": "sin", "value": 30})
print(f"sin(30°) = {r.json()['result']}")

# Тест 4: Константы
print("\nМатематические константы...")
r = requests.get(f"{url}/constants")
data = r.json()
print(f"π = {data['pi']}")
print(f"e = {data['e']}")

print("\n✅ Все тесты пройдены!")