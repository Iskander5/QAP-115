from selenium.webdriver.support.ui import WebDriverWait as WDW
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class RegistrationPage:
    ## Конструктор класса. Инициализирует экземпляр класса,
    # принимая объект driver из Selenium, который используется для взаимодействия с браузером.
    # Также определены различные локаторы для веб-элементов (поля ввода, кнопки и т.д.).
    def __init__(self, driver):
        self.driver = driver
        self.field_name = (By.NAME, 'firstName')
        self.field_surname = (By.NAME, 'lastName')
        self.field_region = (By.XPATH, '//*[@id="page-right"]/div/div/div/form/div[2]/div/div/input')
        self.field_login = (By.ID, 'address')
        self.field_password = (By.ID, 'password')
        self.field_password_confirm = (By.ID, 'password-confirm')
        self.button_registration = (By.NAME, 'register')
        self.button_terms_of_use = (By.LINK_TEXT, 'пользовательского соглашения')
        self.select_list_cities_item = (By.CLASS_NAME, 'rt-scroll-container')
        self.warning_invalid_password = (By.CLASS_NAME, "rt-input-container__meta--error")
        self.account_exist_window = (By.CLASS_NAME, 'card-modal__card')
        self.button_account_exist_go_to_login = (By.NAME, 'gotoLogin')
        self.button_account_exist_reset_password = (By.ID, 'reg-err-reset-pass')
        self.warning_text = (By.XPATH,
                             '//*[@id="page-right"]/div/div/div/form/div[1]/div[1]/span[text()="Необходимо заполнить поле кириллицей. От 2 до 30 символов."]')
        self.warning_text_login = (By.XPATH,
                                   '//*[@id="page-right"]/div/div/div/form/div[3]/div/span[text()="Введите телефон в формате +7ХХХХХХХХХХ или +375XXXXXXXXX, или email в формате example@email.ru"]')
        self.warning_text_password = (By.XPATH,
                                      '//*[@id="page-right"]/div/div/div/form/div[4]/div[2]/span[text()="Длина пароля должна быть не менее 8 символов"]')

    def load(self) -> None:
        # Загружает URL страницы аутентификации веб-сайта с помощью WebDriver.
        self.driver.get(
            'https://b2c.passport.rt.ru/auth/realms/b2c/login-actions/registration?client_id=account_b2c&tab_id=ecOBowTFdIs')

    def check_registration_page(self):
        # Проверяет наличие элементов на странице регистрации, ожидая появления всех обязательных элементов
        try:
            WDW(self.driver, timeout=5).until(
                EC.presence_of_element_located(self.field_name) and
                EC.presence_of_element_located(self.field_surname) and
                EC.presence_of_element_located(self.field_region) and
                EC.presence_of_element_located(self.field_login) and
                EC.presence_of_element_located(self.field_password) and
                EC.presence_of_element_located(self.field_password_confirm) and
                EC.presence_of_element_located(self.button_registration) and
                EC.presence_of_element_located(self.button_terms_of_use)
            )
            return True
        except:
            return False

    def check_warning_invalid_password(self):
        # Проверяет наличие предупреждения об ошибке при вводе некорректного пароля в поле ввода пароля.
        try:
            WDW(self.driver, timeout=5).until(EC.presence_of_element_located(self.warning_invalid_password))
            return True
        except:
            return False

    def check_account_exist_window(self):
        # Проверяет наличие окна с сообщением о существующей учетной записи на странице.
        try:
            WDW(self.driver, timeout=5).until(EC.presence_of_element_located(self.account_exist_window))
            return True
        except:
            return False

    def check_account_exist_window_with_buttons(self):
        # Проверяет наличие окна с сообщением о существующей учетной записи и кнопок "Войти" и "Восстановить пароль".
        try:
            WDW(self.driver, timeout=5).until(
                EC.presence_of_element_located(self.account_exist_window) and
                EC.presence_of_element_located(self.button_account_exist_go_to_login) and
                EC.presence_of_element_located(self.button_account_exist_reset_password)
            )
            return True
        except:
            return False

    def check_registration_page_url(self):
        # Проверяет, соответствует ли текущий URL ожидаемому URL страницы регистрации.
        try:
            expected_partial_url = "https://b2c.passport.rt.ru/auth/realms/b2c/login-actions/registration"
            actual_url = self.driver.current_url
            return expected_partial_url in actual_url
        except:
            return False

    def city_selection(self) -> None:
        # Выбирает город из списка на странице регистрации.
        try:
            WDW(self.driver, timeout=5).until(
                EC.presence_of_element_located(self.field_region)
            )
            self.driver.find_element(*self.field_region).click()

            WDW(self.driver, timeout=5).until(
                EC.presence_of_element_located(self.select_list_cities_item)
            )
            self.driver.find_elements(*self.select_list_cities_item)[0].click()
        except Exception as e:
            print(f"Error occurred while selecting the city: {str(e)}")

    def invalid_password_lower_register(self, query):
        # Вводит переданный query (некорректный пароль) в поле ввода пароля на странице.
        input_password = self.driver.find_element(*self.field_password)
        input_password.clear()
        input_password.send_keys(query)

    def valid_password_registration(self, query):
        # Вводит переданный query (корректный пароль) в поле ввода пароля на странице.
        input_password = self.driver.find_element(*self.field_password)
        input_password.clear()
        input_password.send_keys(query)

    def valid_password_confirm(self, query):
        #Вводит переданный query (подтверждение корректного пароля) в поле подтверждения пароля на странице.
        input_password_confirm = self.driver.find_element(*self.field_password_confirm)
        input_password_confirm.clear()
        input_password_confirm.send_keys(query)

    def click_button_registration(self) -> None:
        # Kликает на кнопку "Зарегистрироваться" на странице.
        self.driver.find_element(*self.button_registration).click()

    def all_input_field(self, name, surname, login, password, password_confirm):
        #Заполняет все поля на странице регистрации (имя, фамилия, логин, пароль и подтверждение пароля) переданными значениями.
        input_name = self.driver.find_element(*self.field_name)
        input_name.clear()
        input_name.send_keys(name)

        input_surname = self.driver.find_element(*self.field_surname)
        input_surname.clear()
        input_surname.send_keys(surname)

        input_login = self.driver.find_element(*self.field_login)
        input_login.clear()
        input_login.send_keys(login)

        input_password = self.driver.find_element(*self.field_password)
        input_password.clear()
        input_password.send_keys(password)

        input_password_confirm = self.driver.find_element(*self.field_password_confirm)
        input_password_confirm.clear()
        input_password_confirm.send_keys(password_confirm)

    def find_errors(self):
        # Проверяет наличие предупреждающих сообщений об ошибках при некорректном заполнении полей формы регистрации.
        try:
            WDW(self.driver, timeout=5).until(
                EC.presence_of_element_located(self.warning_text) and
                EC.presence_of_element_located(self.warning_text_login) and
                EC.presence_of_element_located(self.warning_text_password)
            )
            return True
        except:
            return False
