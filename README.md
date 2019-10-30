# LikeStarter

[LikeStarter: a Smart-contract basedSocial DAO for Crowdfunding](https://ieeexplore.ieee.org/document/8845133)

## Structure

### Truffle

Folder _./LikeStarterContracts_ contains files useful to operate in Tuffle. In particular _./LikeStarterContracts/contracts/_ contains all the contracts developed in Solidity.

### Django

Folder LikeStarterDjango contains all the files useful to run the web server. In order to run web server is mandatory to install all dependencies (could be done also in a docker container); this is the command to execute in _./LikeStarterDjango/acmeconf/_ :

```
pip install -r requirements.txt
```

This is the command to run the server:

```
python manage.py runserver
```

(Require an ethereum blockchain running on localhost:7545, e.g. Ganache)
