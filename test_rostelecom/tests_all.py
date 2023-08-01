import pytest

from test_rostelecom.base_page.main_page import MainPage
from test_rostelecom.base_page.auth_page import AuthPage
from test_rostelecom.base_page.registration_page import RegistrationPage

from time import sleep


@pytest.mark.auth
def test_code_page(driver):
    """Тест проверки поля ввода кода на главной странице."""
    main_page = MainPage(driver)
    main_page.load()
    sleep(5)
    main_page.input_number(73243241245)
    assert main_page.check_fild_code()
    sleep(5)


@pytest.mark.auth
def test_invalid_number(driver):
    """Тест  сообщения об ошибке при вводе недопустимого номера на главной странице."""
    main_page = MainPage(driver)
    main_page.load()
    sleep(5)
    main_page.input_number(1234)
    assert main_page.check_invalid_number_under_field()
    sleep(5)


@pytest.mark.auth
def test_auth_with_numer(driver, login, password):
    """Тест входа с использованием номера телефона на странице аутентификации."""
    auth_page = AuthPage(driver)
    auth_page.load()
    sleep(5)
    auth_page.input_login(79297212514)
    auth_page.input_password('4Q7-Ngj-dg2-wzW')
    auth_page.click_entry()
    assert auth_page.check_button_logout()
    sleep(3)


@pytest.mark.auth
def test_auth_with_email(driver):
    """Тест входа с использованием электронной почты на странице аутентификации."""
    auth_page = AuthPage(driver)
    auth_page.load()
    sleep(5)
    auth_page.input_login('alyadgarov3417@gmail.com')
    auth_page.input_password('4Q7-Ngj-dg2-wzW')
    auth_page.click_entry()
    assert auth_page.check_button_logout()
    sleep(3)


@pytest.mark.recovery_password
def test_recovery_password(driver):
    """Тест восстановления доступа через электронную почту на странице аутентификации."""
    auth_page = AuthPage(driver)
    auth_page.load()
    sleep(5)
    auth_page.click_button_forgot_password()
    assert auth_page.check_recovery_with_email_on_forgot_em_page()
    sleep(3)


@pytest.mark.registration
def test_visible_form_registration_with_agreement(driver):
    """Тест видимости формы регистрации с соглашением."""
    registration_page = RegistrationPage(driver)
    auth_page = AuthPage(driver)
    auth_page.load()
    sleep(5)
    auth_page.click_button_registration()

    assert registration_page.check_registration_page()
    assert registration_page.check_registration_page_url()
    sleep(3)


@pytest.mark.registration
def test_region_selection(driver):
    """Тест выбора региона при регистрации."""
    registration_page = RegistrationPage(driver)
    auth_page = AuthPage(driver)
    auth_page.load()
    sleep(5)
    auth_page.click_button_registration()
    sleep(3)
    registration_page.city_selection()
    assert registration_page.check_registration_page()
    sleep(3)


@pytest.mark.registration
def test_password_field_registration_without_upper_letter(driver):
    """Тест поля пароль без заглавной буквы на странице регистрации."""
    registration_page = RegistrationPage(driver)
    auth_page = AuthPage(driver)
    auth_page.load()
    sleep(5)
    auth_page.click_button_registration()
    sleep(3)
    registration_page.invalid_password_lower_register('qwerty46')
    registration_page.click_button_registration()
    assert registration_page.check_warning_invalid_password()
    sleep(3)


@pytest.mark.registration
def test_password_field_registration_without_latin_letter(driver):
    """Тест поля пароля без латинской буквы на странице регистрации."""
    registration_page = RegistrationPage(driver)
    auth_page = AuthPage(driver)
    auth_page.load()
    sleep(5)
    auth_page.click_button_registration()
    sleep(3)
    registration_page.invalid_password_lower_register('кириллица12')
    registration_page.click_button_registration()
    assert registration_page.check_warning_invalid_password()
    sleep(3)


@pytest.mark.registration
def test_unique_email(driver):
    """Тест регистрации с уникальным адресом электронной почты."""
    registration_page = RegistrationPage(driver)
    auth_page = AuthPage(driver)
    auth_page.load()
    sleep(5)
    auth_page.click_button_registration()
    sleep(3)
    registration_page.all_input_field('Имечко', 'Дулин', 'alyadgarov3417@gmail.com', '4Q7-Ngj-dg2-wzW',
                                      '4Q7-Ngj-dg2-wzW')
    registration_page.click_button_registration()
    assert registration_page.check_account_exist_window()


@pytest.mark.registration
def test_form_of_an_existing_elements(driver):
    """Тест наличия элементов в форме сущ.уч.зап.."""
    registration_page = RegistrationPage(driver)
    auth_page = AuthPage(driver)
    auth_page.load()
    sleep(5)
    auth_page.click_button_registration()
    sleep(3)
    registration_page.all_input_field('Имечко', 'Дулин', 'alyadgarov3417@gmail.com', '4Q7-Ngj-dg2-wzW',
                                      '4Q7-Ngj-dg2-wzW')
    registration_page.click_button_registration()
    assert registration_page.check_account_exist_window_with_buttons()


@pytest.mark.registration
def test_visible_form_on_registration_page(driver):
    """Тест видимости формы сущ.уч.зап.."""
    registration_page = RegistrationPage(driver)
    auth_page = AuthPage(driver)
    auth_page.load()
    sleep(5)
    auth_page.click_button_registration()
    sleep(3)
    assert registration_page.check_registration_page()


@pytest.mark.registration
def test_input_different_password(driver):
    """Тест валидации несовпадения паролей на странице регистрации."""
    registration_page = RegistrationPage(driver)
    auth_page = AuthPage(driver)
    auth_page.load()
    sleep(5)
    auth_page.click_button_registration()
    sleep(3)
    registration_page.valid_password_registration('4Q7-Ngj-dg2-wzW')
    registration_page.valid_password_confirm('4Q7-Ngj-dg2-000')
    registration_page.click_button_registration()
    assert registration_page.check_warning_invalid_password()
    sleep(3)


@pytest.mark.registration
def test_page_email_confirmation(driver):
    """Тест страницы подтверждения электронной почты после успешной регистрации."""
    registration_page = RegistrationPage(driver)
    auth_page = AuthPage(driver)
    main_page = MainPage(driver)
    auth_page.load()
    sleep(5)
    auth_page.click_button_registration()
    sleep(3)
    registration_page.all_input_field('Имечко', 'Дулин', 'venik@gmail.com', 'aDgJl44208',
                                      'aDgJl44208')
    registration_page.click_button_registration()
    assert main_page.check_fild_code()
    assert main_page.check_email_is_visible_completely()
    assert main_page.check_button_change_login_is_visible()
    assert main_page.check_button_recode_is_visible()


@pytest.mark.registration
def test_re_request_code(driver):
    """Тест повторного запроса кода на главной странице."""
    registration_page = RegistrationPage(driver)
    auth_page = AuthPage(driver)
    main_page = MainPage(driver)
    auth_page.load()
    sleep(5)
    auth_page.click_button_registration()
    sleep(3)
    registration_page.all_input_field('Имечко', 'Дулин', 'venik@gmail.com', 'aDgJl44208',
                                      'aDgJl44208')
    registration_page.click_button_registration()
    main_page.input_code(4, 2, 4, 8, 5, 7)
    assert main_page.check_error_message_code()


@pytest.mark.auth
def test_check_choice_login_in_auth_page(driver):
    """Тест наличия элемента "Выберите способ входа" на странице аутентификации."""
    auth_page = AuthPage(driver)
    auth_page.load()
    sleep(5)
    assert auth_page.check_choice_login()



@pytest.mark.auth
def test_check_social_networks(driver):
    """Тест доступности кнопок входа через социальные сети на странице аутентификации."""
    auth_page = AuthPage(driver)
    auth_page.load()
    sleep(5)
    assert auth_page.check_vk_button_to_login()
    assert auth_page.check_mail_button_to_login()
    assert auth_page.check_ok_button_to_login()
    assert auth_page.check_yandex_button_to_login()


@pytest.mark.auth
def test_error_warning_under_login_with_empty_field(driver):
    """Тест сообщения об ошибке при входе с пустыми полями на странице аутентификации."""
    auth_page = AuthPage(driver)
    auth_page.load()
    sleep(5)
    auth_page.input_login(' ')
    auth_page.input_password(' ')
    auth_page.click_entry()
    assert auth_page.check_error_warning_on_field_login()


@pytest.mark.registration
@pytest.mark.parametrize("first_name, last_name, email, password, confirm_password", [
    ('Имечко', 'Дулин', 'tor@heroes.com', '111111111', '22222222222'),
    ('Иван', ' ', 'ivan@example.com', 'qwerty46', 'qwerty46'),
    ('Петр', 'Петров', 'petr@example.com', 'aDgJl44208', 'aDgJl44208'),
    (' ', ' ', ' ', ' ', ' ')
])
def test_errors_warning_with_empty_registration_page(driver, first_name, last_name, email, password, confirm_password):
    """Негативный тест сообщений об ошибках при попытке регистрации с пустыми и неверными значениями  полями на
    странице регистрации."""
    registration_page = RegistrationPage(driver)
    auth_page = AuthPage(driver)

    auth_page.load()
    sleep(5)
    auth_page.click_button_registration()
    sleep(3)
    registration_page.all_input_field(first_name, last_name, email, password, confirm_password)
    registration_page.click_button_registration()

    assert registration_page.check_warning_invalid_password()
    assert registration_page.find_errors()


@pytest.mark.auth
def test_change_color_with_invalid_data(driver):
    """Тест изменения цвета кнопки "Забыли пароль" при входе с неверными данными на странице аутентификации."""
    auth_page = AuthPage(driver)
    auth_page.load()
    sleep(5)
    auth_page.input_login('loshadka@ya.ru')
    auth_page.input_password('getPPP904joy')
    auth_page.click_entry()
    assert auth_page.check_change_color_button_forgot_password()


@pytest.mark.auth
@pytest.mark.parametrize("login, password", [
    (79297212111, '4Q7-Ngj-dg2-wzW'),
    (76541286542, '4Q7-Ngj-dg2-wzW')])
def test_auth_with_numer(driver, login, password):
    """ Негативный тест входа с использованием номера телефона на странице аутентификации."""
    auth_page = AuthPage(driver)
    auth_page.load()
    sleep(5)
    auth_page.input_login(login)
    auth_page.input_password(password)
    auth_page.click_entry()
    assert auth_page.check_error_warning_on_field_login()
    assert auth_page.check_change_color_button_forgot_password()

    sleep(3)