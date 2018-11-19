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

bad_name = { 
 "weight": 3,
 "recepient_name": "Ma",
 "recepient_no": 726404622,
 "pickup": 13456708,
 "dest": 1234678 
}


user_register = {
    'username': 'Eminem',
    'email': 'emm@gmail.com',
    'password': 'P@ssw1rds'
}

bad_passwords = ['fssa', 'VEVEVFA$E', '@sfsfsfvs', 'fngGfeHs', 'Good5stuff', 'Jratcher$ f34']
good_password = 'Josh!elmon5tr0'

user_details = {
    'emails': ['jratcher@gmail.com', 'abby@gmail.com'],
    'usernames': ['admin', 'jay', 'abby']
}

# mock usernames
registered_username = 'admin'
number_first_usern = '4gasv'
symbol_usern = 'vsgs$s'
less_char = 'sg'
space_usernm = 'dfa affa'
# mock emails
reg_email = 'jratcher@gmail.com'
bad_email = 'j.com'






# Login credentials
admin_login = {'username': 'admin',
                    'password': 'password'}

user_login = {'username': 'dan',
                    'password': 'password'}

message = 'message'

expired_token =  "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIGlkIjoxMDMsImVtYWlsIjoiYWJieUBnbWFpbC5jb20iLCJpc19hZG1pbiI6ZmFsc2UsImV4cCI6MTU0MTc0MTE0MX0.uckKmwZ3YqQU4M36xhbEcXLx4KQ4B4Ej-Vua4Yw0HCM"



mock_data = {
    'space_usnm': space_usernm,
    'user_dets': user_details,
    'reg_usernm': registered_username,
    'no_first': number_first_usern,
    'sym_user': symbol_usern,
    'reg_email': reg_email,
    'bad_email': bad_email,
    'order': order,
    'expired': expired_token,
    'admin': admin_login,
    'user': user_login,
    'bad_key': bad_key,
    'less': less_keys,
    'invalid_data': invalid_data,
    'invalid_addr': invalid_addr,
    'invalid_tel': invalid_tel,
    'bad_name': bad_name,
    'register': user_register,
    'bad_pass': bad_passwords,
    'good_pass': good_password,
}