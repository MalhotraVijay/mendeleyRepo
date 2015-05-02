
Dependencies : 

pip install virtualenv
pip install MySQL-python
sudo apt-get install build-essential python-dev libmysqlclient-dev 
sudo apt-get install python-mysqldb
	
App start procedure (1st time)

virtualenv <environment_name>

cd <environment_name>
. bin/activate

pip install Django

django-admin.py startproject <project_name>

cd <project_name>

python manage.py startapp <app_name>

# mendeleyRepo
Mendeley API
