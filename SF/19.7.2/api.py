
import requests
# класс помогающий с multipart-данными
from requests_toolbelt.multipart.encoder import MultipartEncoder

import json

"""api к веб приложению PetFriends"""
class PetFriends:
    def __init__(self):
        self.base_url = "https://petfriends.skillfactory.ru/"

# метод получения auth ключа(запрос к api и возврат статуса и результата в JSON)
    def get_api_key(self, email, password):

        headers = {
            'email': email,
            'password': password
        }
# сохраняем результат запроса в переменную
        res = requests.get(self.base_url + 'api/key', headers=headers)
# статус запроса в статус коде
        status = res.status_code
# резульат либо в текстовом виде, либо можно в JSON
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result
# метод возвращает список питомцев, совпадающий с фильтром
    def get_list_of_pets(self, auth_key: json, filter: str = ""):
        headers = {'auth_key': auth_key['key']}
        filter = {'filter': filter}
# отправляем запрос, который сохраняет переменную результата
        res = requests.get(self.base_url + 'api/pets', headers=headers, params=filter)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

# метод постит на сервер данные о новом питомце и возвращает статус и результат в JSON
    def add_new_pet(self, auth_key: json, name: str, animal_type: str,
                    age: str, pet_photo: str) -> json:

        data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age,
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}

        res = requests.post(self.base_url + 'api/pets', headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        print(result)
        return status, result


# метод удаляет питомца и возвращает статус и результат в JSON
    def delete_pet(self, auth_key: json, pet_id: str) -> json:
        headers = {'auth_key': auth_key['key']}

        res = requests.delete(self.base_url + 'api/pets/' + pet_id, headers=headers)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result


# метод обновляет инфо о питомце и возвращает статус и результат в JSON
    def update_pet_info(self, auth_key: json, pet_id: str, name: str,
                        animal_type: str, age: int) -> json:
        headers = {'auth_key': auth_key['key']}
        data = {
            'name': name,
            'age': age,
            'animal_type': animal_type
        }

        res = requests.put(self.base_url + 'api/pets/' + pet_id, headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result


# метод добавляет новое фото питомца и возвращает статус и результат
    def add_photo_of_pet(self, auth_key: json, pet_id: str, pet_photo: str) -> json:
        data = MultipartEncoder(
            fields={
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'images/jpeg')
            })
        headers = {
            'auth_key': auth_key['key'],
            'Content-Type': data.content_type
        }

        res = requests.post(self.base_url + 'api/pets/set_photo/' + pet_id, headers=headers, data=data)

        status = res.status_code
        result = ''
        try:
            result = res.json()
        except:
            result = res.text
        return status, result


# метод постит данные о питомце статус и результат
    def add_new_pet_simple(self, auth_key: json, name: str, animal_type: str,
                           age: str) -> json:
        data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}

        res = requests.post(self.base_url + 'api/create_pet_simple', headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        print(result)
        return status, result