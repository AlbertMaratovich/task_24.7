import requests


class PetApi:
    def __init__(self):
        self.base_url = "https://petfriends.skillfactory.ru"

    def get_key(self, email, password):
        res = requests.get(self.base_url + "/api/key", headers={"email": email, "password": password})
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def get_list_pets(self, auth_key, filters):
        headers = {"auth_key": auth_key}
        filter = {"filter": filters}
        res = requests.get(self.base_url + "/api/pets", headers=headers, params=filter)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def post_add_new_pet(self, auth_key, name, animal_type, age, pet_photo):
        headers = {"auth_key": auth_key}
        body = {
            "name": name,
            "animal_type": animal_type,
            "age": age
        }
        file = {'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')}
        res = requests.post(self.base_url + "/api/pets", headers=headers, data=body, files=file)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def delete_pet(self, auth_key, pet_id):
        headers = {"auth_key": auth_key}
        res = requests.delete(self.base_url + "/api/pets/" + pet_id, headers=headers)
        status = res.status_code
        return status

    def put_update_pet(self, auth_key, pet_id, name: str, animal_type: str, age: int):
        headers = {"auth_key": auth_key}
        data = {
            "name": name, "animal_type": animal_type, "age": age
        }
        res = requests.put(self.base_url + "/api/pets/" + pet_id, headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def post_add_pet_simple(self, auth_key, name, animal_type, age):
        headers = {"auth_key": auth_key}
        body = {
            "name": name,
            "animal_type": animal_type,
            "age": age
        }
        res = requests.post(self.base_url + "/api/create_pet_simple", headers=headers, data=body)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def post_add_photo_pet(self, auth_key, pet_id, pet_photo):
        headers = {"auth_key": auth_key}
        file = {'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')}
        res = requests.post(self.base_url + "/api/pets/set_photo/" + pet_id, headers=headers, files=file)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result
