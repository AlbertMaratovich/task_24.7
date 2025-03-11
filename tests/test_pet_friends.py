import requests, pytest, os
from settings import email
from settings import password
from api import PetApi

test1 = PetApi()

"""В этом блоке будет реализована проверка работоспособности API. Каждый тест проверяет только позитивный кейс,
и направлен на выявление работоспособности сервиса"""


def test_get_apikey(email=email, password=password):
    """Позитивная проверка возможности получения ключа авторизации"""
    status, result = test1.get_key(email, password)
    assert status == 200
    assert "key" in result


def test_get_list_pets(filters=""):
    """Позитивная проверка возможности получения списка животных"""
    _, auth_key = test1.get_key(email, password)
    status, result = test1.get_list_pets(auth_key["key"], filters)
    assert status == 200
    assert len(result["pets"]) > 0


def test_add_new_pet(pet_photo="images/Furmark.jpg"):
    """Позитивная проверка возможности добавления животного с фото"""
    _, auth_key = test1.get_key(email, password)
    name = "Зяблик"
    animal_type = "Крыса"
    age = 15
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    status, result = test1.post_add_new_pet(auth_key["key"], name, animal_type, age, pet_photo)
    assert status == 200
    assert name in result.values()


def test_update_pet():
    """Позитивная проверка возможности обновления информации о животном"""
    _, auth_key = test1.get_key(email, password)
    _, list_pets = test1.get_list_pets(auth_key["key"], "my_pets")
    name = "Маруся"
    animal_type = "Корова"
    age = 7
    status, result = test1.put_update_pet(auth_key["key"], list_pets["pets"][0]["id"], name=name, animal_type=animal_type, age=age)
    assert status == 200
    assert name in result["name"]
    

def test_delete_pet():
    """Позитивная проверка возможности удаления животного"""
    _, auth_key = test1.get_key(email, password)
    _, list_pets = test1.get_list_pets(auth_key["key"], "my_pets")
    status = test1.delete_pet(auth_key["key"], list_pets["pets"][0]["id"])
    assert status == 200


def test_add_pet_simple():
    """Позитивная проверка возможности добавления животного без фото"""
    _, auth_key = test1.get_key(email, password)
    name = "Arnold"
    animal_type = "Bull"
    age = 18
    status, result = test1.post_add_pet_simple(auth_key["key"], name, animal_type, age)
    assert status == 200
    assert name in result["name"]


def test_add_photo_pet(pet_photo="images/Furmark.jpg"):
    """Позитивная проверка возможности добавления фото к животному"""
    _, auth_key = test1.get_key(email, password)
    _, list_pets = test1.get_list_pets(auth_key["key"], "my_pets")
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    status, result = test1.post_add_photo_pet(auth_key["key"], list_pets["pets"][0]["id"], pet_photo)
    assert status == 200
    assert list_pets["pets"][0]["id"] in result["id"]


"""Далее буду выполнены позитивные и негативные проверки, направленные на более детальное тестирование сервиса.
Блок относится к заданию 24.7.2 'напишите ещё 10 различных тестов для данного REST API-интерфейса'          """


def test_age_text():
    """Проверка создания карточки животного с вводном текста в поле возраста"""
    _, auth_key = test1.get_key(email, password)
    name = "Arnold"
    animal_type = "Bull"
    age = "Fifty"
    status, result = test1.post_add_pet_simple(auth_key["key"], name, animal_type, age)
    if status == 200 and age in result.values():
        raise Exception("Создана карточка животного с текстом в поле возраста")
    else:
        assert status == 400


def test_add_pet_empty_fields():
    """Проверка создания карточки животного c пустыми полями"""
    _, auth_key = test1.get_key(email, password)
    name = ""
    animal_type = ""
    age = ""
    status, result = test1.post_add_pet_simple(auth_key["key"], name, animal_type, age)
    if status == 200:
        raise Exception("Создана карточка животного с пустями полями")
    else:
        assert status == 400


def test_get_apikey_wrong_pass(email=email, password="12345678"):
    """Проверка получения ключа авторизации с неправильным паролем"""
    status, result = test1.get_key(email, password)
    if status == 200 and "key" in result:
        raise Exception("Получен ключ авторизации с непавильным паролем")
    else:
        assert status == 403


def test_get_apikey_wrong_email(email="hfdhdsj@gdsh.com", password=password):
    """Проверка получения ключа авторизации с неправильной почтой"""
    status, result = test1.get_key(email, password)
    if status == 200 and "key" in result:
        raise Exception("Получен ключ авторизации с непавильной почтой")
    else:
        assert status == 403


def test_add_new_pet_empty_photo(pet_photo="images/wrong_file.xlsx"):
    """Проверка возможности создания карточки животного с некорректным файлом для фото"""
    _, auth_key = test1.get_key(email, password)
    name = "Зяблик"
    animal_type = "Крыса"
    age = 15
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    status, result = test1.post_add_new_pet(auth_key["key"], name, animal_type, age, pet_photo)
    if status == 200 and name in result.values():
        raise Exception("Создана карточка животного, при использовании некорректного файла")
    else:
        assert status == 400


def test_add_new_pet_negative_number(pet_photo="images/Furmark.jpg"):
    """Проверка возможности добавления животного с фото с отрицательным числом в поле возраста"""
    _, auth_key = test1.get_key(email, password)
    name = "Potato"
    animal_type = "Vegetable"
    age = -8
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    status, result = test1.post_add_new_pet(auth_key["key"], name, animal_type, age, pet_photo)
    if status == 200 and str(age) == result["age"]:
        raise Exception("Создана карточка животного, при использовании отрицательного числа в поле возраста")
    else:
        assert status == 400


def test_update_pet_wrong_key():
    """Проверка возможности обновления карточки животного с некорректным ключом авторизации"""
    auth_key_wrong = "33b2eed5178feb7276b0d3d475568469e4ed426d749e6ed7cdd97cfa"
    _, auth_key = test1.get_key(email, password)
    _, list_pets = test1.get_list_pets(auth_key["key"], "my_pets")
    name = "Маруся"
    animal_type = "Корова"
    age = 7
    status, result = test1.put_update_pet(auth_key_wrong, list_pets["pets"][0]["id"], name=name, animal_type=animal_type, age=age)
    if status == 200 and name in result.values():
        raise Exception("Карточка животного обновлена с некорректным ключом авторизации")
    else:
        assert status == 403


def test_update_pet_empty_fields():
    """Проверка возможности обновления информации о животном c незаполненными полями"""
    _, auth_key = test1.get_key(email, password)
    _, list_pets = test1.get_list_pets(auth_key["key"], "my_pets")
    name = ""
    animal_type = ""
    age = 0
    status, result = test1.put_update_pet(auth_key["key"], list_pets["pets"][0]["id"], name=name, animal_type=animal_type, age=age)
    assert name in result["name"]
    if status == 200:
        raise Exception("Карточка животного обновлена пустыми полями")
    else:
        assert status == 400


def test_delete_pet_other_user(filters=""):
    """Проверка возможности удаления животного другого пользователя.
    В данном кейсе удаляется последняя карточка всего списка животных,
    важно чтобы эта карточка была создана не текущим юзером"""
    _, auth_key = test1.get_key(email, password)
    _, list_pets = test1.get_list_pets(auth_key["key"], filters)
    status = test1.delete_pet(auth_key["key"], list_pets["pets"][-1]["id"])
    if status == 200:
        raise Exception("Удалена карточка животного другого пользователя")
    else:
        assert status == 403


def test_add_wrong_photo_pet(pet_photo="images/wrong_file.xlsx"):
    """Проверка возможности добавления некорректного файла к карточке животного"""
    _, auth_key = test1.get_key(email, password)
    _, list_pets = test1.get_list_pets(auth_key["key"], "my_pets")
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    status, result = test1.post_add_photo_pet(auth_key["key"], list_pets["pets"][0]["id"], pet_photo)
    if status == 200:
        raise Exception("Добавлен некорректный формат файла вместо фото животного")
    else:
        assert status == 400
    """Комментарий ментору. В данном кейсе появляется ошибка с кодом 500, считаю, что это также баг,
    так как по документации предусмотрена ошибка 400 для некорректных данных, а серверных ошибок быть не должно"""
