
# Order statuses
canceled = 'Canceled'
delivered = 'Delivered'
in_transit = 'In-transit'
# Admin statuses
admin = True
not_admin = False

# Dummy orders
orders = {
   #id   userid  pickup addr  dest address kg  status
    321: [532, '4 5345 343', '4 5343 343', 5, 'In-transit'],
    453: [352, '4 5435 324', '6 5356 353', 3, 'Delivered'],
    133: [254, '5 6535 453', '8 5465 742', 6, 'Canceled'],
    301: [686, '4 5345 343', '4 5343 343', 5, 'In-transit'],
    353: [103, '4 5435 324', '6 5356 353', 3, 'Delivered'],
    633: [345, '5 6535 453', '8 5465 742', 6, 'Canceled'],
    365: [140, '4 5345 343', '4 5343 343', 5, 'In-transit'],
    495: [675, '4 5435 324', '6 5356 353', 3, 'Delivered'],
    127: [109, '5 6535 453', '8 5465 742', 6, 'Canceled'],
    249: [140, '4 5345 343', '4 5343 343', 5, 'In-transit'],
    132: [619, '4 5435 324', '6 5356 353', 3, 'Delivered'],
    808: [805, '5 6535 453', '8 5465 742', 6, 'Canceled'],
    809: [532, '4 5345 343', '4 5343 343', 5, 'In-transit'],
    810: [352, '4 5435 324', '6 5356 353', 3, 'Delivered'],
    811: [254, '5 6535 453', '8 5465 742', 6, 'Canceled'],
    812: [686, '4 5345 343', '4 5343 343', 5, 'In-transit'],
    813: [103, '4 5435 324', '6 5356 353', 3, 'Delivered'],
    814: [345, '5 6535 453', '8 5465 742', 6, 'Canceled'],
    815: [140, '4 5345 343', '4 5343 343', 5, 'In-transit'],
    816: [675, '4 5435 324', '6 5356 353', 3, 'Delivered'],
    817: [109, '5 6535 453', '8 5465 742', 6, 'Canceled'],
    818: [140, '4 5345 343', '4 5343 343', 5, 'In-transit'],
    819: [619, '4 5435 324', '6 5356 353', 3, 'Delivered'],
    820: [805, '5 6535 453', '8 5465 742', 6, 'Canceled']
}

users = {
 # userid  email                 password   isadmin
    100: ['jratcher@gmail.com', 'ulembaya', admin],
    102: ['dan@gmail.com', 'ulembaya', not_admin],
    103: ['abby@gmail.com', 'ulembaya', not_admin],
    104: ['totodi@gmail.com', 'ulembaya', not_admin],
    105: ['milly@gmail.com', 'ulembaya', not_admin],
    350: ['callen@gmail.com', 'ulembaya', not_admin], 
}

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
