from api import PetFriends
from settings import valid_email, unvalid_password, valid_password
import os

pf = PetFriends()


def test_get_api_key_for_unvalid_user(email=valid_email, password=unvalid_password):
    """ Проверяем что запрос api ключа c неверным паролем возвращает статус 403 и в результате не содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403
    assert 'key' not in result


def test_add_new_pet_with_unvalid_data(name='Барбоскин', animal_type='567453',
                                       age='4', pet_photo='images/dog.jpg'):
    """Проверяем, что можно добавить питомца с некорректными данными -  в тип питомца ставим числа """

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200  # на данный момент  в приложении баг
    assert result['name'] == name


def test_add_new_pet_with_unvalid_data(name='Барбоскин', animal_type='двортерьер',
                                       age='-4', pet_photo='images/dog.jpg'):
    """Проверяем, что можно добавить питомца с некорректными данными - отрицательным значением обязательного парамера - возраста """

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200  # на данный момент  в приложении баг
    assert result['name'] == name


def test_add_new_pet_with_unvalid_data(name='Барбоскин', animal_type='двортерьер',
                                       age='999', pet_photo='images/dog.jpg'):
    """Проверяем, что можно добавить питомца с некорректными данными - очень большим  значением возраста """

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200  # на данный момент  в приложении баг
    assert result['name'] == name


def test_add_new_pet_with_unvalid_data(name='Барбоскинннннкаомриормиормыорморормиочсмиомиомиомиомиосмиомриомриормисормиормиломиомиормиормиомиосмиолмклмимичсмчсмормисмосимчсшоимчсмчомичсмышпаыгаршомосчмичсомиочсрмисчормочмимрышапыомросмиырпыомомпарышооморимрирчмиымиыиимищагкнзфосышмрыамлркеглнпщаыпмар', animal_type='двортерьер',
                                       age='4', pet_photo='images/dog.jpg'):
    """Проверяем, что можно добавить питомца с некорректными данными - большим  количеством символов в имени - 256 букв """

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200  # на данный момент  в приложении баг
    assert result['name'] == name

def test_get_all_pets_with_unvalid_filter(filter='your_pets'):
    """ Проверяем, что сервер не может обработать запрос на получение питомцев при передаче  в filter неверного значения .
    Доступное значение параметра filter - 'my_pets' либо '' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 500


def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца с некоррекным (отрицательным) номером питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/dog.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id -8 питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][-8]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200 # на данный момент в приложении баг
    assert pet_id not in my_pets.values()

def test_successful_update_self_pet_info(name='Мурзик', animal_type='Котэ', age=5):
    """Проверяем возможность обновления информации о питомце c указанием некорректного (отрицателного) номера питомца """

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Еслди список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][-11]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200 # в приложении  данный момент баг
    else:
        assert result['name'] == name
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

def test_add_new_pet_without_photo_with_valid_data(name='Барбоскин', animal_type='двортерьер',
                                     age='4'):
    """Проверяем что можно добавить питомца с корректными  данными без добавления фото """

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name

def test_add_photo_of_pet(pet_photo='images/dog.jpg'):
    """Проверяем, что можно по указаному ID добавить фото питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем добавить фото
    if len(my_pets['pets']) > 0:
        status, result = pf.add_photo_of_pet(auth_key, my_pets['pets'][0]['id'], pet_photo)

        # Проверяем что статус ответа = 200
        assert status == 200

def test_add_photo_of_pet(pet_photo='images/dogs.txt'):
    """Проверяем, что нельзя по указаному ID добавить вместо фото питомца текстовый файл"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем добавить некорректный файл
    if len(my_pets['pets']) > 0:
        status, result = pf.add_photo_of_pet(auth_key, my_pets['pets'][0]['id'], pet_photo)

        # Проверяем, что сервер не может обработать запрос и что статус ответа = 500
        assert status == 500








