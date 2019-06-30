# Project Simple RestAPI A**E Example

Python 2.7 Flask project demonstrating simple RestAPI Flask framework with MongoDB

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

You need installed docker, with Linux and Darwin it comes together with docker-composer, in Windows you have to install docker-compose additionally

**Debian:**
```
$ sudo apt update
$ sudo apt install apt-transport-https ca-certificates curl gnupg2 software-properties-common
$ curl -fsSL https://download.docker.com/linux/debian/gpg | sudo apt-key add -
$ sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/debian $(lsb_release -cs) stable"
$ sudo apt update
$ apt-cache policy docker-ce
$ sudo apt install docker-ce
$ sudo systemctl status docker
```
**MAC**
* [Docker](https://hub.docker.com/editions/community/docker-ce-desktop-mac) - Download from here

**WINDOWS**
* [Docker](https://hub.docker.com/editions/community/docker-ce-desktop-windows) - Download from here

### Installing

Within the folder with docker-compose.yml on command line:
```
$ docker-compose up build
```
This will install mongoDB and python envrionment in docker machine

## Running the tests
Creating new user:
```
curl -i -X PUT -H "Content-Type:application/json" http://0.0.0.0:8000/user/testuser -d '{"groups":["User Group 1"],"lastname":"User","email":"testuser@example.com","firstname":"Test"}'
```
Fetching all users:
```
curl http://0.0.0.0:8000/users/
```
Updating one user:
```
curl -i -X POST -H "Content-Type:application/json" http://0.0.0.0:8000/user/testuser -d '{"groups":["User Group 1","User Group 2"],"lastname":"User","email":"testuser@example.com","firstname":"Test"}'
```
Deleting one user:
```
curl -i -X DELETE -H "Content-Type:application/json" http://0.0.0.0:8000/user/testuser
```
Fetching all groups:
```
curl http://127.0.0.1:8000/groups/
```
## Author
m0nika.v0s.muelleR
## Acknowledgements
* for demonstration purposes