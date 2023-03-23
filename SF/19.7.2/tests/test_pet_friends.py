from api import PetFriends

#добавляем регистрационные данные
from settings import valid_email, valid_password, invalid_email, invalid_password
import os

pf = PetFriends()

#проверка что запрос api ключа возвращает 200 и в результате есть слово key
def test_get_api_key_for_valid_user(email = valid_email, password = valid_password):
    # делаем вызов метода и сохр полученные результаты
    status, result = pf.get_api_key(email, password)
    #сверяем ФР с ОР
    assert status == 200
    assert 'key' in result

# проверка, что запрос всех питомцев возвращает не пустой список
def test_get_all_pets_with_valid_key(filter=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0

# проверка, что можно добавить питомца с корректными данными
def test_add_new_pet_with_valid_data(name='Fil', animal_type='manul_king',
                                     age='1', pet_photo='images/manul.jpg'):
    # получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # cверяем ответ с ОР
    assert status == 200
    assert result['name'] == name

# проверка возможности удаления питомца
def test_successful_delete_self_pet():
    # получаем auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # проверяем - если список своих питомцев пустой, то добавляем нового и повторно запрашиваем
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Fil", "manul_king", "1", "images/manul.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # повторно запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # проверка что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()

# проверка возможности обновления инфо о питомце
def test_update_self_pet_info(name='Bill', animal_type='dog', age=2):
    # получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # проверяем что статус ответа = 200 и имя питомца соответствует
        assert status == 200
        assert result['name'] == name

# проверка добавления питомца без фото
def test_add_pet_simple(name='Dill', animal_type='bird', age='3'):
    # запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # добавляем питомца
    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)

    # Сверяем ФР с ОР
    assert status == 200
    assert result['name'] == name

# проверка добавления новой фото питомца
def test_add_photo_at_pet(pet_photo='images/manul2.jpeg'):

    # получаем полный путь изображения и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    if len(my_pets['pets']) > 0:
        status, result = pf.add_photo_of_pet(auth_key, my_pets['pets'][0]['id'], pet_photo)

        _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

        # сверяем ФР с ОР
        assert status == 200
        assert result['pet_photo'] == my_pets['pets'][0]['pet_photo']
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

# проверка запроса с невалидным password и валидным email
def test_get_api_key_unvalid_password_and_valid_mail(email=valid_email, password=invalid_password):
    status, result = pf.get_api_key(email, password)

    assert status == 403
    assert 'key' not in result

# проверка запроса с валидным password и невалидным email
def test_get_api_key_valid_mail_and_unvalid_password(email=valid_email, password=invalid_password):
    status, result = pf.get_api_key(email, password)

    assert status == 403
    assert 'key' not in result

# проверка запроса с невалидным password и невалидным email
def test_get_api_key_unvalid_email_and_unvalid_password(email=invalid_email, password=invalid_password):
    status, result = pf.get_api_key(email, password)

    assert status == 403
    assert 'key' not in result

# проверка запроса с пустыми password и email
def test_add_pet_valid_data_empty_field():
    name = ''
    animal_type = ''
    age = ''
    #  запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # добавляем питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    # сверяем ФР с ОР
    assert status == 200
    assert result['name'] == name

# проверка добавления питомца с отриц. возрастом
def test_add_pet_negative_age(name='Griz', animal_type='bear', age='-1', pet_photo='images/enot.jpg'):
    # получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    #  запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # сверяем ФР с ОР
    assert status == 200
    assert result['age'] == age

# проверка добавления питомца со спец символами в name
def test_add_pet_with_special_in_name(name='C@t', animal_type = 'dog', age='3',
                                                                 pet_photo='images/enot.jpeg'):
    # получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    #  запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # сверяем ФР с ОР
    assert status == 400

# проверка добавления питомца с трехначным возрастом
def test_add_pet_three_number(name='Chill', animal_type = 'cat', age='666',pet_photo='images/enot.jpeg'):
    # получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # сверяем ФР с ОР
    assert status == 200
    assert result['age'] == age

# проверка поля порода с большим значением
def test_add_pet_big_animal_type(name='Killy', age='1', pet_photo='images/manul.jpeg'):
    animal_type = 'CiIfcIJHCTtYdMSzrTLSgiWgERFCCZ'
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    list_animal_type = result['animal_type']#.split()
    symbol_count = len(list_animal_type)

    # сверяем ФР с ОР
    assert status == 200
    assert symbol_count > 25








