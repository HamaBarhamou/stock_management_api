import django_heroku

# Définition des paramètres de configuration pour Heroku
# ...

# Activer la prise en charge des fichiers statiques pour Heroku
django_heroku.settings(locals(), staticfiles=True, static_root='staticfiles')
