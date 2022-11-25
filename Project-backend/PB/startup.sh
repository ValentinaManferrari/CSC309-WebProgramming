# !/bin/sh
# python3 -m pip install virtualenv
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 backend_TFC_group_9233/manage.py migrate

export DJANGO_SUPERUSER_EMAIL=test@test.com
export DJANGO_SUPERUSER_PASSWORD=test
python3 ./backend_TFC_group_9233/manage.py createsuperuser --username test --no-input

echo "An account with the following credentials has been created"
echo "username: test"
echo "password: test"
echo
echo "If that is not the case, please create your own superuser"