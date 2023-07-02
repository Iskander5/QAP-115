import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture(autouse=True)
def testing():
    pytest.driver = webdriver.Chrome('C:/DriverChrome/chromedriver.exe')
    pytest.driver.implicitly_wait(5)  # Неявное ожидание всех элементов в течение 5 секунд
    # Переходим на страницу авторизации
    pytest.driver.get('http://petfriends.skillfactory.ru/login')

    yield

    pytest.driver.quit()


def test_show_my_pets():
    # Вводим email
    email_input = pytest.driver.find_element(By.ID, "email")
    email_input.send_keys('vasya@mail.com')
    # Вводим пароль
    pass_input = pytest.driver.find_element(By.ID, "pass")
    pass_input.send_keys('12345')
    # Нажимаем на кнопку входа в аккаунт
    submit_button = pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
    submit_button.click()
    # Проверяем, что мы оказались на главной странице пользователя
    assert pytest.driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"
    pytest.driver.get('https://petfriends.skillfactory.ru/my_pets')

    # Явное ожидание элементов на странице
    WebDriverWait(pytest.driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/th')))
    WebDriverWait(pytest.driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td[2]')))
    WebDriverWait(pytest.driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td[3]')))
    WebDriverWait(pytest.driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td[4]')))
    WebDriverWait(pytest.driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr')))

    pet_images = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/th')
    pet_names = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td[2]')
    pet_breeds = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td[3]')
    pet_ages = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td[4]')
    pet_rows = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr')

    # Присутствуют все питомцы
    num_pets_text = pytest.driver.find_element(By.XPATH, '/html/body/div[1]/div/div[1]').text
    num_pets = int(num_pets_text.split(':')[1].split('\n')[0].strip())

    assert len(pet_rows) == num_pets

    # Хотя бы у половины питомцев есть фото
    num_pets_with_photo = sum(1 for img in pet_images if img.get_attribute('src') != '')
    assert num_pets_with_photo >= num_pets / 2

    # У всех питомцев есть имя, порода и возраст
    assert len(pet_names) == num_pets
    assert len(pet_breeds) == num_pets
    assert len(pet_ages) == num_pets

    # У всех питомцев разные имена
    unique_names = set(name.text for name in pet_names)
    assert len(unique_names)== num_pets


def test_pet_cards():
    # Вводим email
    email_input = pytest.driver.find_element(By.ID, "email")
    email_input.send_keys('vasya@mail.com')
    # Вводим пароль
    pass_input = pytest.driver.find_element(By.ID, "pass")
    pass_input.send_keys('12345')
    # Нажимаем на кнопку входа в аккаунт
    submit_button = pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
    submit_button.click()
    # Проверяем, что мы оказались на главной странице пользователя
    assert pytest.driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"
    pytest.driver.get('https://petfriends.skillfactory.ru/my_pets')

    # Неявное ожидание всех элементов в течение 2 секунд
    pytest.driver.implicitly_wait(2)


    pet_rows = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr')

    pet_images = []
    pet_names = []
    pet_ages = []

    for row in pet_rows:
        pet_image = row.find_element(By.TAG_NAME, 'th')
        pet_name = row.find_element(By.XPATH, 'td[2]')
        pet_age = row.find_element(By.XPATH, 'td[4]')
        pet_images.append(pet_image)
        pet_names.append(pet_name)
        pet_ages.append(pet_age)

    # Присутствуют все питомцы
    num_pets_text = pytest.driver.find_element(By.XPATH, '/html/body/div[1]/div/div[1]').text
    num_pets = int(num_pets_text.split(':')[1].split('\n')[0].strip())

    assert len(pet_rows) == num_pets

    # Хотя бы у половины питомцев есть фото
    num_pets_with_photo = sum(1 for img in pet_images if img.get_attribute('src') != '')
    assert num_pets_with_photo >= num_pets / 2

    # У всех питомцев есть имя, возраст и порода
    assert len(pet_names) == num_pets
    assert len(pet_ages) == num_pets

    # У всех питомцев разные имена
    unique_names = set(name.text for name in pet_names)
    assert len(unique_names) != num_pets
