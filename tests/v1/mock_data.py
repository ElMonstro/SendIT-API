# Tests Mock data


order = {'order': ['532', '4 5345 343', '4 5343 343', 5, 'In-transit']}
response_data = {"order": { "321": [532, "4 5345 343", "4 5343 343", 5, "Canceled"]}}

users_orders = {
    "orders": {
        "353": [103, "4 5435 324", "6 5356 353", 3, "Delivered" ],
        "813": [103, "4 5435 324", "6 5356 353", 3,  "Delivered"]
    }
}

# Login credentials
admin_login = {'email': 'jratcher@gmail.com',
                    'password': 'ulembaya'}

user_login = {'email': 'abby@gmail.com',
                    'password': 'ulembaya'}

message = 'message'

expired_token =  "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIGlkIjoxMDMsImVtYWlsIjoiYWJieUBnbWFpbC5jb20iLCJpc19hZG1pbiI6ZmFsc2UsImV4cCI6MTU0MTc0MTE0MX0.uckKmwZ3YqQU4M36xhbEcXLx4KQ4B4Ej-Vua4Yw0HCM"
