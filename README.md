# SendIT-API

[![Build Status](https://travis-ci.org/ElMonstro/SendIT-API.svg?branch=ft-admin-get-all-orders-161700246)](https://travis-ci.org/ElMonstro/SendIT-API)
[![Test Coverage](https://api.codeclimate.com/v1/badges/7afda6c46de2f7995949/test_coverage)](https://codeclimate.com/github/ElMonstro/SendIT-API/test_coverage)
[![Maintainability](https://api.codeclimate.com/v1/badges/7afda6c46de2f7995949/maintainability)](https://codeclimate.com/github/ElMonstro/SendIT-API/maintainability)

The sendIT app is built using flask to make RESTful APIs to achieve basic functionalities for the app 

## RESTful API Endpoints for sendIT parcel delivery service


| Method        |       Endpoint                        |         Description                           |
| ------------- |       -------------                   |         -------------                         |
| `POST`        | `/api/v1/parcels`                     |   Create a new parcel order                   |
| `GET`         | `/api/v1/parcels`                     |   Get a all parcel delivery orders            |
| `GET`         | `/api/v1/parcels/<parcel-id>`         |   Get a single delivery order by id           |
| `POST`        | `/api/v1/login`                      |   log a user into account                     |
| `PUT`         | `/api/v1/parcels/<parcel-id>/cancel`  |   Cancel a specific parcel delivery order     |
| `PUT`         | `/api/v1/parcels/<parcel-d>`          |   Change specific delivery order to delivered |

# Development Environment
**Note: This instructions are for ubuntu operating distro but are compatible with debian based linux distros**

- Ensure that you have python3.6,
if not install it with:
```
 sudo apt update
 sudo apt install python3.6 
```
- Then install pip3 if not present with:
 ```
 sudo apt install pip3
 ```
- Install virtualenv if not present with:
 ```
 sudo apt install virtualenv
 ```
- Install git if not present with:
```
sudo apt install git
```
- Install postman by downloading it from here:
https://www.getpostman.com/



## Initialize a virtual python Environment to House all your Dependencies

create the virtual environment

```
python3 -p virtualenv venv 
```
activate the environment before cloning the project from github

```
source venv/bin/activate
```

## Clone and Configure a the sendIT flask Project

Provided you have a github account, login before entering the command to create a local copy of the repo

```
git clone https://github.com/ElMonstro/SendIT-API.git
```
then:
```
cd SendIT-API
```

Next, install the requirements by typing:

```
pip install -r requirements.txt
```

## Testing
# Manual Testing
To test the endpointsensure that the following tools are available the follow steps below
   ### Tools:
     Postman
  - Run the project with:
  ```
  python run.py
  ```
  - Start sending above written requests from postman
      
  
     
### Automatic Testing
  The application was tested using `pytest` and coveralls.
     
     pytest --cov=app
