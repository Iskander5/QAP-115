from selenium.common import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait as WDW
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class MainPage:
    # Kонструктор класса.
    # Инициализирует экземпляр класса, принимая объект driver из Selenium,
    # который используется для взаимодействия с браузером.
    # Также определены различные локаторы для веб-элементов (поля ввода, кнопки и т.д.).
    def __init__(self, driver):

        self.driver = driver
        self.check_entry_field = (By.ID, "address")
        self.enry_field = (By.ID, "otp_get_code")
        self.wait_page_0 = (By.ID, "rt-code-0")
        self.wait_page_1 = (By.ID, "rt-code-1")
        self.wait_page_2 = (By.ID, "rt-code-2")
        self.wait_page_3 = (By.ID, "rt-code-3")
        self.wait_page_4 = (By.ID, "rt-code-4")
        self.wait_page_5 = (By.ID, "rt-code-5")
        self.check_invalid_number = (By.CLASS_NAME, "rt-input-container__meta--error ")
        self.check_email_is_visible = (By.CLASS_NAME, "register-confirm-form-container__desc")
        self.button_change_login = (By.NAME, "otp_back_phone")
        self.button_recode = (By.NAME, "otp_resend_code")
        self.timer_return_code = (By.CLASS_NAME, "code-input-container__timeout")
        self.form_error_message = (By.ID, "form-error-message")

    def load(self) -> None:
        # Загружает URL главной страницы веб-сайта с помощью WebDriver.
        self.driver.get("https://b2c.passport.rt.ru/auth/realms/b2c/protocol/openid-connect/auth?client_id=lk_decosystems&redirect_uri=https://start.rt.ru/&response_type=code&scope=openid&theme=light")

    def is_loaded(self) -> bool:
        # Проверяет, успешно ли загружена главная страница, ожидая появления поля ввода otp_get_code
        try:
            WDW(self.driver, timeout=5).until(EC.presence_of_element_located(self.enry_field))
            return True
        except:
            return False

    def input_number(self, query: int):
        # Вводит переданный query (номер телефона) в поле ввода на странице и кликает на кнопку для получения кода.
        input_number_phone = self.driver.find_element(*self.check_entry_field)
        input_number_phone.clear()
        input_number_phone.send_keys(query)
        self.driver.find_element(*self.enry_field).click()

    def input_code(self, number_1: int, number_2: int, number_3: int, number_4: int, number_5: int, number_6: int):
        # Ожидание появления первого поля ввода
        input_number_1 = WDW(self.driver, timeout=10).until(
            EC.presence_of_element_located(self.wait_page_0)
        )
        input_number_1.send_keys(number_1)

        # Ожидание появления второго поля ввода
        input_number_2 = WDW(self.driver, timeout=10).until(
            EC.presence_of_element_located(self.wait_page_1)
        )
        input_number_2.send_keys(number_2)

        # Ожидание появления третьего поля ввода
        input_number_3 = WDW(self.driver, timeout=10).until(
            EC.presence_of_element_located(self.wait_page_2)
        )
        input_number_3.send_keys(number_3)

        # Ожидание появления четвертого поля ввода
        input_number_4 = WDW(self.driver, timeout=10).until(
            EC.presence_of_element_located(self.wait_page_3)
        )
        input_number_4.send_keys(number_4)

        # Ожидание появления пятого поля ввода
        input_number_5 = WDW(self.driver, timeout=10).until(
            EC.presence_of_element_located(self.wait_page_4)
        )
        input_number_5.send_keys(number_5)

        # Ожидание появления шестого поля ввода
        input_number_6 = WDW(self.driver, timeout=10).until(
            EC.presence_of_element_located(self.wait_page_5)
        )
        input_number_6.send_keys(number_6)

    def check_button_change_login_is_visible(self):
        # Проверяет, видима ли кнопка.
        try:
            WDW(self.driver, timeout=5).until(EC.presence_of_element_located(self.button_change_login))
            return True
        except:
            return False

    def check_error_message_code(self):
        # Проверяет, есть ли сообщение об ошибке ввода кода (form_error_message) на странице.
        try:
            WDW(self.driver, timeout=5).until(EC.presence_of_element_located(self.form_error_message))
            return True
        except:
            return False

    def check_button_recode_is_visible(self):
        # Проверяет, видимы ли кнопка "Отправить код повторно" (otp_resend_code)
        # или таймер обратного отсчета для повторной отправки кода (code-input-container__timeout) на странице.
        try:
            button_recode = WDW(self.driver, timeout=5).until(EC.presence_of_element_located(self.button_recode))
            if button_recode.is_displayed():
                return True
        except TimeoutException:
            pass  # Обрабатываем исключение, если кнопка не найдена или не отображается

        try:
            timer_return_code = WDW(self.driver, timeout=5).until(
                EC.presence_of_element_located(self.timer_return_code))
            if timer_return_code.is_displayed():
                return True
        except TimeoutException:
            pass  # Обрабатываем исключение, если таймер не найден или не отображается

        return False


    def check_email_is_visible_completely(self):
        # Проверяет, видимо ли полное описание email (register-confirm-form-container__desc) на странице.
        try:
            WDW(self.driver, timeout=5).until(EC.presence_of_element_located(self.check_email_is_visible))
            return True
        except:
            return False

    def check_fild_code(self):
        # Проверяет, появилось ли поле ввода кода на странице, ожидая появления первого поля ввода (wait_page_0)
        try:
            WDW(self.driver, timeout=5).until(EC.presence_of_element_located(self.wait_page_0))
            return True
        except:
            return False

    def check_invalid_number_under_field(self):
        # Проверяет, появилось ли сообщение об ошибке недопустимого номера под полем ввода на странице.
        try:
            WDW(self.driver, timeout=5).until(EC.presence_of_element_located(self.check_invalid_number))
            return True
        except:
            return False
