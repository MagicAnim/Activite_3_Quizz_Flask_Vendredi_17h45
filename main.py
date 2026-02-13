# Importation de Flask
# render_template
# et le module random pour l'aléatoire
from flask import Flask, render_template, request
from random import choice
# On crée l'application = instance de la classe Flask
app = Flask(__name__)


# On crée le route pour la page d'accueil avec le décorateur @app
#  @app.route() associe une adresse URL à une fonction
# "/" pour la page d'accueil
@app.route("/")
def index():
    return render_template("index.html")



####################################
#  TOUJOURS A LA FIN DU CODE       #
####################################
# Lancement de l'application
# HOST : précise qui a accès au serveur Flask (0.0.0.0 = toutes les adresses de la machines )
# Port d'entrée au serveur via le port 81
app.run(host="0.0.0.0", port = 81)