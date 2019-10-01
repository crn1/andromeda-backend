python3 -m venv venv

echo "" >> ./venv/bin/activate
echo "export FLASK_ENV=development" >> ./venv/bin/activate
echo "export FLASK_APP=andromeda-backend:app" >> ./venv/bin/activate

echo "" >> ./venv/bin/activate.fish
echo "export FLASK_ENV=development" >> ./venv/bin/activate.fish
echo "export FLASK_APP=andromeda-backend:app" >> ./venv/bin/activate.fish

python3 -c 'import os; print("secret_key = ", str(os.urandom(32)))' >> ./andromeda-backend/secrets.py

. ./venv/bin/activate
pip install -r requirements.txt
