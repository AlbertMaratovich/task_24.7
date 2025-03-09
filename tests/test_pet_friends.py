import requests, pytest, os
from settings import email
from settings import password
from api import PetApi

test1 = PetApi()


def test_get_apikey(email=email, password=password):
    status, result = test1.get_key(email, password)
    assert status == 200
    assert "key" in result


def test_get_list_pets(filters=""):
    _, auth_key = test1.get_key(email, password)
    status, result = test1.get_list_pets(auth_key["key"], filters)
    assert status == 200
    assert len(result["pets"]) > 0


def test_add_new_pet(pet_photo="images/Furmark.jpg"):
    _, auth_key = test1.get_key(email, password)
    name = "Зяблик"
    animal_type = "Крыса"
    age = 15
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    status, result = test1.post_add_new_pet(auth_key["key"], name, animal_type, age, pet_photo)
    assert status == 200
    assert name in result.values()


def test_update_pate():
    _, auth_key = test1.get_key(email, password)
    _, list_pets = test1.get_list_pets(auth_key["key"], "my_pets")
    name = "Маруся"
    animal_type = "Корова"
    age = 7
    status, result = test1.put_update_pet(auth_key["key"], list_pets["pets"][0]["id"], name=name, animal_type=animal_type, age=age)
    assert status == 200
    assert name in result["name"]
    

def test_delete_pet():
    _, auth_key = test1.get_key(email, password)
    _, list_pets = test1.get_list_pets(auth_key["key"], "my_pets")
    status = test1.delete_pet(auth_key["key"], list_pets["pets"][0]["id"])
    assert status == 200

