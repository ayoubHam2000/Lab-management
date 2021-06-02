## pour installer le projet 

créer un dossier pour votre projet
ouvrir un **bash** terminal 
utilisez **cmder** ou n'importe quel terminal bash 
to download cmder : https://cmder.net/

## bien sûr, vous devez installer python v3 >

## utilisez git ou téléchargez simplement le projet depuis  https://github.com/ayoubHam2000/Lab-management.git

git init <br/>
git remote add origin https://github.com/ayoubHam2000/Lab-management.git <br/>
git pull origin master <br/>

## installer des bibliothèques 

py -m pip install virtualenv <br/>
virtualenv env <br/>
activate <br/>
py -m pip install -r requirement.txt <br/>
pip install -U python-dotenv <br/>
py -m pip install django-widget-tweaks <br/>

create .env file for email server <br/>
copy and past these lines to .env <br/>

## les configuration de serveur d'email
export EMAIL_HOST=smtp.gmail.com <br/>
export EMAIL_HOST_USER=gmail <br/>

export EMAIL_HOST_PASSWORD=gmail_password <br/>


## pour exécuter et configurer le serveur pour la première fois 
bash reset.sh <br/>
## pour exécuter le serveur ultérieurement
py manage.py runserver <br/>


**you can change the password and email of the super admin in reset.sh --21**

pour utiliser le vrai serveur de email, vous devez commenter cette ligne sur  labManagement/settings.py <br/>

## EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

et libérez ces lignes <br/>
### config = dotenv_values(".env")
### EMAIL_HOST = config['EMAIL_HOST'] 
### EMAIL_HOST_USER = config['EMAIL_HOST_USER']
### EMAIL_USE_TLS = True
### EMAIL_PORT = 587
### EMAIL_HOST_PASSWORD = config['EMAIL_HOST_PASSWORD']
### DEFAULT_FROM_EMAIL = config['EMAIL_HOST_USER']

sinon l'e-mail sera affiché dans le terminal <br/>



