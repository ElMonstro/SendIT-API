# Tests Mock data


order = {
    "weight": 3,
    "recepient_name": "Moracha",
    "recepient_no": 726404622,
    "pickup": 'Kisii',
    "dest": 'Nairobi'
}

bad_keys = {
    "weiht": 3,
    "reepent_name": "Moracha",
    "recepnt_no": 726404622,
    "pip": 'Kisii',
    "dst": 'Nairobi'
}

less_keys = {
    "recepient_name": "Moracha",
    "recepient_no": 726404622,
    "pickup": 'Kisii',
    "dest": 'Nairobi'
}

invalid_data ={ 
 "weight": "",
 "recepient_name": "Moracha",
 "recepient_no": 72764422,
 "pickup": "",
 "dest": ""
}

bad_data_types = { 
 "weight": 4,
 "recepient_name": 555,
 "recepient_no": "jkbjnjkmhb",
 "pickup": 243,
 "dest": 45
}

bad_data_types_r ={
    "message": "Unsuccessful, recepient number must be an integer, recepient name must be a string, pickup location must be a string, destination location must be a string, pickup must have letters, destination must have letters, phone number must have nine digits, receipient name must be in letters"
}

user_register = {
    'username': 'Eminem',
    'email': 'emm@gmail.com',
    'password': 'P@ssw1rds'
}

bad_usern_register = {
    'username': 'nem',
    'email': 'emm@gmail.com',
    'password': 'Psw1rds'
}

bad_email_user_register = {
    'username': 'Eminem',
    'email': 'emmgmail.com',
    'password': 'P@ssw1rds'
}

invalid_data_r ={
    "message": "Unsuccessful, weight must be an integer, pickup must have letters, destination must have letters, phone number must have nine digits"
}
bad_keys_response = {
    "message": "Unsuccessful, the object must have a 'dest' key, the object must have a 'pickup' key, the object must have a 'weight' key, the object must have a 'recepient_name' key, the object must have a 'recepient_no' key"
}

bad_passwords = ['fssa', 'VEVEVFA$E', '@sfsfsfvs',
                 'fngGfeHs', 'Good5stuff', 'Jratcher$ f34']
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

expired_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIGlkIjoxMDMsImVtYWlsIjoiYWJieUBnbWFpbC5jb20iLCJpc19hZG1pbiI6ZmFsc2UsImV4cCI6MTU0MTc0MTE0MX0.uckKmwZ3YqQU4M36xhbEcXLx4KQ4B4Ej-Vua4Yw0HCM"


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
    'bad_keys': bad_keys,
    'less': less_keys,
    'register': user_register,
    'bad_pass': bad_passwords,
    'good_pass': good_password,
    'bad_data_type': bad_data_types,
    'bad_email_r': bad_email_user_register,
    'bad_usern_r': bad_usern_register,
    'badkeys_r': bad_keys_response,
    'invalid_data_r': invalid_data_r,
    'bad_data_type_r': bad_data_types_r,
    'invalid_data': invalid_data
}
