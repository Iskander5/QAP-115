import pytest
import requests
from pydantic import ValidationError
from MODUL28_booking.serializers.booking_serializer import BookingResponseModel, CreateBookingRequest, BookingResponse
from MODUL28_booking.serializers.booking_serializer_auth import AuthRequestModel
from MODUL28_booking.api.booking_api import BookingAPI

booking_api = BookingAPI()

# Тест для проверки авторизации
@pytest.mark.auth
@pytest.mark.parametrize(
    "username, password, headers",
    [
        ("admin", "password123", {"Content-Type": "application/json"}),  # Допустимые данные, позитивный тест
        ("admin", "password123", {"Content-Type": ""}),  # Недопустимое значение Content-Type (пустое), негативный тест
        ("admin", "password123", {}),  # Отсутствие заголовков, негативный тест
        ("", "", {"Content-Type": "application/json"}),  # Отсутствие данных, негативный тест
        ("dsaqwe", "asd123", {"Content-Type": "application/json"}),  # Недопустимые данные, негативный тест
    ],
)
def test_auth_request(username, password, headers):
    url = "https://restful-booker.herokuapp.com/auth"

    try:
        data = AuthRequestModel(username=username, password=password)
    except ValidationError as e:
        if username == "" and password == "":
            assert (
                str(e)
                == "2 ошибки проверки для модели AuthRequestModel:\n - поле username обязательно (тип=value_error.missing)\n - поле password обязательно (тип=value_error.missing)")
        else:
            pytest.fail(f"Не удалось проверить данные запроса: {e}")

    response = requests.post(url, headers=headers, json=data.dict())

    assert (
        response.status_code == 200
    ), f"Запрос завершился с кодом статуса {response.status_code}"
    if "reason" in response.json() and response.json()["reason"] == "Bad credentials":
        assert "token" not in response.json(), "Ответ содержит токен для недопустимых учетных данных"
    else:
        assert "token" in response.json(), "Ответ не содержит токен"



# Тест для получения информации о бронировании

@pytest.mark.without_token
@pytest.mark.parametrize(
    "booking_id, expected_status, headers",
    [
        (1, 200, {"Accept": "application/json"}),  # Допустимый booking_id и заголовки, позитивный тест
        (0, 404, {"Accept": "application/json"}),  # Недопустимый booking_id, негативный тест
        (-1, 404, {"Accept": "application/json"}),  # Недопустимый booking_id, негативный тест
        ("a", 404, {"Accept": "application/json"}),  # Недопустимый booking_id, негативный тест
        (1, 418, {"Accept": ""}),  # Недопустимое значение Accept (пустое), негативный тест
        (1, 200, None),  # Отсутствие заголовков, негативный тест
    ],
)
def test_get_booking(booking_id, expected_status, headers):
    url = f"https://restful-booker.herokuapp.com/booking/{booking_id}"

    response = requests.get(url, headers=headers)

    assert (
        response.status_code == expected_status
    ), f"Запрос завершился с кодом статуса {response.status_code}"

    if expected_status == 200:
        try:
            data = response.json()
            booking = BookingResponseModel(**data)
        except (ValidationError, TypeError) as e:
            pytest.fail(f"Не удалось проверить данные бронирования: {e}")

        assert booking.firstname != "", "Отсутствует имя"


# Тест для создания бронирования
@pytest.mark.xfail
@pytest.mark.without_token
@pytest.mark.parametrize('headers, request_body, expected_status', [
    ({"Content-Type": "application/json", "Accept": "application/json"},
     {"firstname": "Jim", "lastname": "Brown", "totalprice": 111, "depositpaid": True,
      "bookingdates": {"checkin": "2018-01-01", "checkout": "2019-01-01"},
      "additionalneeds": "Breakfast"}, 200),  # Валидные данные, позитивный тест
    ({"Content-Type": "text/plain", "Accept": "text/plain"},
     {"firstname": "Jim", "lastname": "Brown", "totalprice": 111, "depositpaid": True,
      "bookingdates": {"checkin": "2018-01-01", "checkout": "2019-01-01"},
      "additionalneeds": "Breakfast"}, 415),  # Неверные заголовки, негативный тест
    (None, {"firstname": "Jim", "lastname": "Brown", "totalprice": 111, "depositpaid": True,
            "bookingdates": {"checkin": "2018-01-01", "checkout": "2019-01-01"},
            "additionalneeds": "Breakfast"}, 200)])  # Отсутствие заголовков, негативный тест
def test_create_booking(headers, request_body, expected_status):
    url = "https://restful-booker.herokuapp.com/booking"

    try:
        request_data = CreateBookingRequest(**request_body)
    except ValidationError as e:
        pytest.fail(f"Не удалось провалидировать данные запроса: {e}")

    response = requests.post(url, headers=headers, json=request_data.dict())

    assert response.status_code == expected_status, f"Запрос завершился с ошибкой {response.status_code}"

    if expected_status == 200:
        try:
            response_data = response.json()
            booking_response = BookingResponse(**response_data)
        except (ValidationError, TypeError) as e:
            pytest.fail(f"Не удалось провалидировать данные о бронировании: {e}")

        assert booking_response.bookingid is not None and isinstance(booking_response.bookingid, int), \
            "Отсутствует или неверный идентификатор бронирования"
        assert isinstance(booking_response.booking, CreateBookingRequest), \
            "Отсутствуют или неверные данные о бронировании"


# Тест для обновления бронирования
@pytest.mark.required_token
@pytest.mark.parametrize('booking_id, expected_status, headers', [
    (1, 403, {"Content-Type": "application/json", "Accept": "application/json"}),
    # Валидный идентификатор бронирования и заголовки, позитивный тест
    (0, 403, {"Content-Type": "application/json", "Accept": "application/json"}),  # Неверный идентификатор, негативный тест
    (-1, 403, {"Content-Type": "application/json", "Accept": "application/json"}),  # Неверный идентификатор, негативный тест
    ('a', 403, {"Content-Type": "application/json", "Accept": "application/json"}),  # Неверный идентификатор, негативный тест
    (1, 403, {"Content-Type": "", "Accept": ""}),  # Неверные заголовки (пустые значения), негативный тест
    (1, 403, None)])  # Отсутствие заголовков, негативный тест
def test_update_booking(booking_id, expected_status, headers):
    url = f"https://restful-booker.herokuapp.com/booking/{booking_id}"
    request_body = {
        "firstname": "John",
        "lastname": "Doe",
        "totalprice": 150,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2023-06-22",
            "checkout": "2023-06-25"
        },
        "additionalneeds": "Lunch"
    }

    response = requests.put(url, headers=headers, json=request_body)

    assert response.status_code == expected_status, f"Запрос завершился с ошибкой {response.status_code}"

    if expected_status == 200:
        try:
            data = response.json()
            booking = BookingResponseModel(**data)
        except (ValidationError, TypeError) as e:
            pytest.fail(f"Не удалось провалидировать данные о бронировании: {e}")

        assert booking.firstname == request_body["firstname"], "Имя не соответствует"
        assert booking.lastname == request_body["lastname"], "Фамилия не соответствует"
        assert booking.totalprice == request_body["totalprice"], "Общая стоимость не соответствует"
        assert booking.depositpaid == request_body["depositpaid"], "Depositpaid не соответствует"
        assert booking.bookingdates["checkin"] == request_body["bookingdates"]["checkin"], "Дата заезда не соответствует"
        assert booking.bookingdates["checkout"] == request_body["bookingdates"][
            "checkout"], "Дата выезда не соответствует"


# # Тест для удаления бронирования
# @pytest.mark.required_token
# @pytest.mark.parametrize('booking_id, expected_status, headers', [
#     (1, 201, {"Content-Type": "application/json", "Accept": "application/json"}),
#     # Валидный идентификатор бронирования и заголовки, позитивный тест
#     (0, 403, {"Content-Type": "application/json", "Accept": "application/json"}),  # Неверный идентификатор, негативный тест
#     (-1, 403, {"Content-Type": "application/json", "Accept": "application/json"}),  # Неверный идентификатор, негативный тест
#     ('a', 403, {"Content-Type": "application/json", "Accept": "application/json"}),  # Неверный идентификатор, негативный тест
#     (1, 403, {"Content-Type": "", "Accept": ""}),  # Неверные заголовки (пустые значения), негативный тест
#     (1, 403, None)])  # Отсутствие заголовков, негативный тест
# def test_delete_booking(booking_id, expected_status, headers):
#     url = f"https://restful-booker.herokuapp.com/booking/{booking_id}"
#
#     response = requests.delete(url, headers=headers)
#
#     assert response.status_code == expected_status, f"Запрос завершился с ошибкой {response.status_code}"
#
#     if expected_status == 201:
#         try:
#             data = response.json()
#             assert data == str(booking_id), "Идентификатор удаленного бронирования не соответствует"
#         except (ValidationError, TypeError) as e:
#             pytest.fail(f"Не удалось провалидировать данные о удаленном бронировании: {e}")
#
#
# if __name__ == '__main__':
#     pytest.main(['-v', '--html=report.html'])  # Запуск тестов и сохранение отчета в формате HTML


