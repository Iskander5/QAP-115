import requests
from MODUL28_booking.serializers.booking_serializer import BookingResponse
from MODUL28_booking.serializers.booking_serializer_auth import AuthResponse


class BookingAPI:
    def __init__(self):
        self.base_url = "https://restful-booker.herokuapp.com"

    def create_booking(self):
        data = {
            'firstname': 'Jim',
            'lastname': 'Brown',
            'totalprice': 111,
            'depositpaid': True,
            'bookingdates': {
                'checkin': '2018-01-01',
                'checkout': '2019-01-01'
            },
            'additionalneeds': 'Breakfast'
        }
        headers = {'Content-Type': 'application/json'}
        res = requests.post(self.base_url + '/booking', headers=headers, json=data)
        response_data = BookingResponse(**res.json())
        return response_data.bookingid


    # def get_booking(self):
    #     res = requests.get(self.base_url + '/booking')
    #     response = res.json()
    #     return response

    def get_api_key(self):
        data = {
            'username': 'admin',
            'password': 'password123'
        }
        headers = {'Content-Type': 'application/json'}
        res = requests.post(self.base_url + '/auth', headers=headers, json=data)
        response_data = AuthResponse(**res.json())
        return response_data

#     def del_booking(self):
#         Authorization = self.get_api_key()
#         headers = {'Content-Type': 'application/json', 'Cookie': f'{Authorization}'}
#         res = requests.delete(self.base_url + f'/booking/1468', headers=headers)
#         response_data = BookingDelResponse(http=res.status_code)
#         return response_data

