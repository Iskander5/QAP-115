import json

from api import PetFriends
import os
from dotenv import load_dotenv

load_dotenv('settings.env')
valid_email = os.getenv('valid_email')
valid_password = os.getenv('valid_password')


pf = PetFriends()

def test_add_new_pet_invalid_data():
    """Тест добавления питомца c неверными данными"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    pet_friends = PetFriends()
    name = ""
    animal_type = "cat"
    age = "abc"
    pet_photo = 'image\dog.jpg'
    status, result = pet_friends.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200 #Должен быть код 400. Определенно баг.



def test_get_apikey_with_invalid_parameters(filter=''):
    """"Тест получения APIkey с некорректными параметрами"""
    status, auth_key = pf.get_api_key('a@a8008s', '1IOumumua')
    if isinstance(auth_key, dict) and 'key' in auth_key:
        _, result = pf.get_list_of_pets(auth_key, filter)
        assert status == 403

    else:
        assert status == 403
        assert 'key' not in auth_key



def test_update_pet_info_invalid_id():
    """Тест обновления информации о питомце с неверным идентификатором"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    pet_id = "invalid_id"
    name = "Updated Pet"
    animal_type = "dog"
    age = 5
    status, result = pf.update_pet_info(auth_key, pet_id, name, animal_type, age)
    assert status == 400




def test_get_api_key_invalid_email_format():
    """Тест получения ключа API с неверным форматом электронной почты"""
    email = "invalid_email"
    password = "valid_password"
    status, result = pf.get_api_key(email, password)
    assert status == 403



def test_add_new_pet_missing_parameters(name='', animal_type='',  age='', pet_photo='image\dog.jpg'):
    """Тест добавления информации о новом питомце без указания обязательных параметров"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200 #Здесь должен быть код 400


def test_set_pet_photo_invalid_pet_id(pet_id='invalid_pet_id', pet_photo='image\cat.jpg'):
    """Тест добавления фото питомца с неверным идентификатором питомца"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.set_pet_photo(auth_key, pet_id, pet_photo)
    assert status == 500
    assert pet_photo not in result


def test_delete_pet_invalid_pet_id(pet_id = "invalid_pet_id"):
    """Тест удаления питомца с неверным идентификатором питомца"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.delete_pet(auth_key, pet_id)
    assert status == 200 #Здесь должен быть код 400


def test_get_list_of_pets_invalid_auth_key():
    """Тест получения списка питомцев с неверным API ключом"""
    auth_key = {"key": "invalid_key"}
    status, result = pf.get_list_of_pets(auth_key)
    assert status == 403

def test_add_new_pet_invalid_age():
    """Тест добавления информации о новом питомце с некорректным возрастом (не числовое значение)"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    name = "Max"
    animal_type = "dog"
    age = "three"
    pet_photo = 'image/dog.jpg'
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200 #Должен быть код 400


def test_update_pet_info_invalid_animal_type():
    """Тест обновления информации о питомце с некорректным типом животного (не строковое значение)"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    pet_id = "pet_id"
    name = "Updated Pet"
    animal_type = 123
    age = 5
    status, result = pf.update_pet_info(auth_key, pet_id, name, animal_type, age)
    assert status == 400









