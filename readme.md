# pour installer le projet 

créer un dossier pour votre projet
ouvrir un **bash** terminal 
utilisez **cmder** ou n'importe quel terminal bash 
to download cmder : https://cmder.net/

# bien sûr, vous devez installer python v3 >

# utilisez git ou téléchargez simplement le projet depuis  https://github.com/ayoubHam2000/Lab-management.git

git init 
git remote add origin https://github.com/ayoubHam2000/Lab-management.git
git pull origin master

# installer des bibliothèques 

py -m pip install virtualenv
virtualenv env
activate
py -m pip install -r requirement.txt
pip install -U python-dotenv
py -m pip install django-widget-tweaks

create .env file for email server
copy and past these lines to .env

# les configuration de serveur d'email
export EMAIL_HOST=smtp.gmail.com
export EMAIL_HOST_USER=gmail

export EMAIL_HOST_PASSWORD=gmail_password


# pour exécuter et configurer le serveur pour la première fois 
bash reset.sh 
# pour exécuter le serveur ultérieurement
py manage.py runserver


**you can change the password and email of the super admin in reset.sh --21**

pour utiliser le vrai serveur de email, vous devez commenter cette ligne sur  labManagement/settings.py

# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

et libérez ces lignes 
# config = dotenv_values(".env")
# EMAIL_HOST = config['EMAIL_HOST']
# EMAIL_HOST_USER = config['EMAIL_HOST_USER']
# EMAIL_USE_TLS = True
# EMAIL_PORT = 587
# EMAIL_HOST_PASSWORD = config['EMAIL_HOST_PASSWORD']
# DEFAULT_FROM_EMAIL = config['EMAIL_HOST_USER']

sinon l'e-mail sera affiché dans le terminal 



