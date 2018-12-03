
# eth-crowdsale
A Solidity crowdsale contract-based web platform 
## Structure
### Truffle 
Folder *./LikeStarterTruffle* contains files useful to operate in Tuffle. In particular *./LikeStarterTruffle/contracts/* contains all the contracts developed in Solidity.
### Django
Folder LikeStarterDjango contains all the files useful to run the web server. In order to run web server is mandatory to install all dependencies (could be done also in a docker container); this is the command to execute in *./LikeStarterDjango/acmeconf/* :
```
pip install -r requirements.txt
```
This is the command to run the server:
```
python manage.py runserver
```
(Require an ethereum blockchain running on localhost:7545)
