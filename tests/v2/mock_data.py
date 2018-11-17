# Tests Mock data


order = { 
 "weight": 3,
 "recepient_name": "Moracha",
 "recepient_no": 726404622,
 "pickup": 13456708,
 "dest": 1234678 
}

bad_key = { 
 "weight": 3,
 "reepient_name": "Moracha",
 "recepient_no": 726404622,
 "pikup": 13456708,
 "dest": 1234678 
}

less_keys = { 
 "recepient_name": "Moracha",
 "recepient_no": 726404622,
 "pickup": 13456708,
 "dest": 1234678 
}

invalid_data = { 
 "weight": '3',
 "recepient_name": "Moracha",
 "recepient_no": 726404622,
 "pickup": 13456708,
 "dest": '1234678' 
}

invalid_tel = { 
 "weight": 3,
 "recepient_name": "Moracha",
 "recepient_no": 72644622,
 "pickup": 13456708,
 "dest": 1234678 
}

invalid_addr = { 
 "weight": 3,
 "recepient_name": "Moracha",
 "recepient_no": 726404622,
 "pickup": 1356708,
 "dest": 1234678 
}







# Login credentials
admin_login = {'email': 'jratcher@gmail.com',
                    'password': 'ulembaya'}

user_login = {'email': 'abby@gmail.com',
                    'password': 'ulembaya'}

message = 'message'

expired_token =  "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIGlkIjoxMDMsImVtYWlsIjoiYWJieUBnbWFpbC5jb20iLCJpc19hZG1pbiI6ZmFsc2UsImV4cCI6MTU0MTc0MTE0MX0.uckKmwZ3YqQU4M36xhbEcXLx4KQ4B4Ej-Vua4Yw0HCM"



mock_data = {
    'order': order,
    'expired': expired_token,
    'admin': admin_login,
    'user': user_login,
    'bad_key': bad_key,
    'less': less_keys,
    'invalid_data': invalid_data,
    'invalid_addr': invalid_addr,
    'invalid_tel': invalid_tel
}