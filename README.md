# Patient Management System basic crud operations fastapi

```bash
# create virtual envirionment (linux)
python3 -m venv .venv

# activat the envirionment
source .venv/bin/activate

# install dependencies
pip install -r requirements.txt

# make sure you have the .env
cp code/sample.env code/.env

# run dev code
cd code
uvicorn main:app --port 8000 --reload

# Make sure settings are added .env
# Running alembic migrations
cd code
alembic upgrade heads

```
