# Web_math_to_latex

First, install library:

```bash
pip install -r requirement.txt
```

Go to the settings file to adjust your sql

```bash
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': "postgres",
        'USER': "postgres.invkxcjgpflgnbjykuwk", 
        'PASSWORD': "123@gmail.com", 
        'HOST': "aws-0-ap-southeast-1.pooler.supabase.com", 
        'PORT': "5432", 
    }
}
```
Run migretion:

```bash
python manage.py migrate
```

Run web:

```bash
python manage.py runserver
```