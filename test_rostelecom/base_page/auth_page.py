from selenium.webdriver.support.ui import WebDriverWait as WDW
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class AuthPage:
    # Конструктор класса. Инициализирует экземпляр класса,
    # принимая объект driver из Selenium, который используется для взаимодействия с браузером.
    # Также определены различные локаторы для веб-элементов (поля ввода, кнопки и т.д.).
    def __init__(self, driver):
        self.driver = driver
        self.entry_field = (By.ID, 'username')
        self.entry_pass = (By.ID, 'password')
        self.button_entry = (By.ID, 'kc-login')
        self.button_registration = (By.ID, 'kc-register')
        self.button_logout = (By.ID, 'logout-btn')
        self.button_forgot_password = (By.ID, 'forgot_password')
        self.check_recovery_with_email = (By.ID, 't-btn-tab-mail')
        self.check_phone_login = (By.ID, "t-btn-tab-phone")
        self.check_email_login = (By.ID, "t-btn-tab-mail")
        self.check_login_in_login = (By.ID, "t-btn-tab-login")
        self.check_personal_account_login = (By.ID, "t-btn-tab-ls")
        self.check_vk_button = (By.ID, "oidc_vk")
        self.check_ok_button = (By.ID, "oidc_ok")
        self.check_mail_button = (By.ID, "oidc_mail")
        self.check_ya_button = (By.ID, "oidc_ya")
        self.check_error_warning_field_login = (By.CLASS_NAME, "rt-input__placeholder")
        self.check_change_color_button_forgot_pass = (By.CLASS_NAME, "rt-link--orange")

    def load(self) -> None:
        #Загружает URL страницы аутентификации веб-сайта с помощью WebDriver.
        self.driver.get(
            "https://b2c.passport.rt.ru/auth/realms/b2c/protocol/openid-connect/auth?client_id=account_b2c&redirect_uri=https://b2c.passport.rt.ru/account_b2c/login&response_type=code&scope=openid&state=28f9c46f-3ab0-43d0-9ecf-a85d003870b5&theme&auth_type")

    def check_load_personal_account(self):
        #Проверяет, успешно ли загружена личная учетная запись пользователя, ожидая появления кнопки "Logout".
        try:
            WDW(self.driver, timeout=5).until(EC.presence_of_element_located(self.button_logout))
            return True
        except:
            return False

    def input_login(self, query: int):
        #Вводит переданный query (имя пользователя или номер телефона) в поле ввода логина на странице.
        input_number_phone = self.driver.find_element(*self.entry_field)
        input_number_phone.clear()
        input_number_phone.send_keys(query)

    def input_password(self, query):
        #Вводит переданный query (пароль) в поле ввода пароля на странице.
        input_valid_password = self.driver.find_element(*self.entry_pass)
        input_valid_password.clear()
        input_valid_password.send_keys(query)

    def click_entry(self) -> None:
        #Кликает на кнопку "Войти" на странице для попытки входа.
        self.driver.find_element(*self.button_entry).click()

    def click_button_forgot_password(self) -> None:
        #Кликает на кнопку "Забыли пароль?" для перехода на страницу восстановления пароля.
        self.driver.find_element(*self.button_forgot_password).click()

    def click_button_registration(self) -> None:
        #Кликает на кнопку "Зарегистрироваться" для перехода на страницу регистрации.
        self.driver.find_element(*self.button_registration).click()

    def check_choice_login(self) -> bool:
        #Проверяет наличие различных вариантов входа (логин через телефон, почту и т.д.) на странице, ожидая появления соответствующих элементов.
        try:
            WDW(self.driver, timeout=5).until(
                EC.presence_of_element_located(self.check_phone_login) and
                EC.presence_of_element_located(self.check_email_login) and
                EC.presence_of_element_located(self.check_login_in_login) and
                EC.presence_of_element_located(self.check_personal_account_login))
            return True
        except:
            return False

    def check_vk_button_to_login(self) -> bool:
        #Проверяет наличие кнопки для входа через VK (Вконтакте) на странице, ожидая появления этой кнопки.
        try:
            WDW(self.driver, timeout=5).until(EC.presence_of_element_located(self.check_vk_button))
            return True
        except:
            return False

    def check_ok_button_to_login(self) -> bool:
        #Проверяет наличие кнопки для входа через OK (Одноклассники) на странице, ожидая появления этой кнопки.
        try:
            WDW(self.driver, timeout=5).until(EC.presence_of_element_located(self.check_ok_button))
            return True
        except:
            return False

    def check_mail_button_to_login(self) -> bool:
        #Проверяет наличие кнопки для входа через Mail (Почта) на странице, ожидая появления этой кнопки.
        try:
            WDW(self.driver, timeout=5).until(EC.presence_of_element_located(self.check_mail_button))
            return True
        except:
            return False

    def check_yandex_button_to_login(self) -> bool:
        #Проверяет наличие кнопки для входа через Yandex (Яндекс) на странице, ожидая появления этой кнопки.
        try:
            WDW(self.driver, timeout=5).until(EC.presence_of_element_located(self.check_ya_button))
            return True
        except:
            return False

    def check_button_logout(self) -> bool:
        #Проверяет наличие кнопки "Logout" на странице, ожидая появления этой кнопки.
        try:
            WDW(self.driver, timeout=5).until(EC.presence_of_element_located(self.button_logout))
            return True
        except:
            return False

    def check_recovery_with_email_on_forgot_em_page(self) -> bool:
        #Проверяет наличие опции для восстановления пароля через электронную почту на странице восстановления пароля.
        try:
            WDW(self.driver, timeout=5).until(EC.presence_of_element_located(self.check_recovery_with_email))
            return True
        except:
            return False

    def check_error_warning_on_field_login(self) -> bool:
        #Проверяет наличие предупреждающего сообщения об ошибке на поле ввода логина на странице.
        try:
            WDW(self.driver, timeout=5).until(EC.presence_of_element_located(self.check_error_warning_field_login))
            return True
        except:
            return False

    def check_change_color_button_forgot_password(self):
        #Проверяет наличие кнопки изменения цвета на странице восстановления пароля.
        try:
            WDW(self.driver, timeout=5).until(EC.presence_of_element_located(self.check_change_color_button_forgot_pass))
            return True
        except:
            return False