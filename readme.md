for install the project

git init 
git remote add origin https://github.com/ayoubHam2000/Lab-management.git
git pull origin master


py -m pip install virtualenv
virtualenv env
activate
py -m pip install -r requirement.txt
pip install -U python-dotenv

create .env file for email server
copy and past these lines to .env

export EMAIL_HOST=smtp.gmail.com
export EMAIL_HOST_USER=gmail
export EMAIL_HOST_PASSWORD=password
