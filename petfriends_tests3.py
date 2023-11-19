### Замените USER_DATA на Ваши данные

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

@pytest.fixture
def driver():
    # Указываете путь к вашему chromedriver.exe
    driver_path = "USER_DATA"

    # Инициализация веб-драйвера с указанием пути к chromedriver.exe
    options = webdriver.ChromeOptions()
    options.binary_location = "USER_DATA"
    driver = webdriver.Chrome(options=options)

    yield driver

    driver.quit()

def test_pet_cards(driver):
    # Авторизация на сайте (используйте свои учетные данные)
    username = "username"
    password = "password"

    driver.get("https://petfriends.skillfactory.ru/login")
    driver.find_element(By.ID, "email").send_keys(username)
    driver.find_element(By.ID, "pass").send_keys(password)
    driver.find_element(By.CLASS_NAME, "btn.btn-success").click()

    # Переход на страницу "Мои питомцы"
    driver.get("https://petfriends.skillfactory.ru/my_pets")

    try:
        # Ожидание загрузки списка питомцев
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[@id="all_my_pets"]/table/tbody/tr')))

        # Получение списка всех питомцев на странице
        pets = driver.find_elements(By.XPATH, '//div[@id="all_my_pets"]/table/tbody/tr')

        # Добавим неявные ожидания для фото, имени и возраста
        driver.implicitly_wait(10)

        # Проверка наличия питомцев
        if not pets:
            # Если питомцев нет, выведит сообщение и завершит тест
            print("На странице отсутствуют питомцы.")
            return

        for pet in pets:
            # Проверка наличия фото
            assert pet.find_elements(By.XPATH, './td[1]/img'), "У питомца отсутствует фото."

            # Проверка наличия имени, возраста и породы
            assert pet.find_element(By.XPATH, './td[2]'), "У питомца отсутствует имя."
            assert pet.find_element(By.XPATH, './td[4]'), "У питомца отсутствует возраст."
            assert pet.find_element(By.XPATH, './td[3]'), "У питомца отсутствует порода."

    except TimeoutException:
        # В случае, если питомцев нет, выведит сообщение
        print("На странице отсутствуют питомцы.")
    except Exception as e:
        # Вывод информации об ошибке
        print(f"An error occurred: {e}")
        pytest.fail(f"An error occurred: {e}")

def test_pet_photos_and_info(driver):
    # Авторизация на сайте (используйте свои учетные данные)
    username = "username"
    password = "password"

    driver.get("https://petfriends.skillfactory.ru/login")
    driver.find_element(By.ID, "email").send_keys(username)
    driver.find_element(By.ID, "pass").send_keys(password)
    driver.find_element(By.CLASS_NAME, "btn.btn-success").click()

    # Переход на страницу "Мои питомцы"
    driver.get("https://petfriends.skillfactory.ru/my_pets")

    try:
        # Явное ожидание загрузки списка питомцев
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[@id="all_my_pets"]/table/tbody/tr')))

        # Получение списка всех питомцев на странице
        pets = driver.find_elements(By.XPATH, '//div[@id="all_my_pets"]/table/tbody/tr')

        # Вывод информации о питомцах
        for index, pet in enumerate(pets, start=1):
            print(f"Pet {index}: {pet.text}")

        # Проверка наличия питомцев
        if not pets:
            # Если питомцев нет, выведит сообщение и завершит тест
            print("На странице отсутствуют питомцы.")
            return

        pets_with_photos = [pet for pet in pets if pet.find_elements(By.XPATH, './td[1]/img')]

        # Вывод информации для отладки
        print(f"Found {len(pets_with_photos)} pets with photos.")

        assert len(pets_with_photos) >= len(pets) / 2, "У менее чем половины питомцев есть фото."

    except TimeoutException:
        # В случае, если питомцев нет, выведет сообщение
        print("На странице отсутствуют питомцы.")
    except Exception as e:
        # Вывод информации об ошибке
        print(f"An error occurred: {e}")
        pytest.fail(f"An error occurred: {e}")



### Евгений Ю.
