# Importation de Flask
# render_template
# et le module random pour l'aléatoire
from flask import Flask, render_template, request, session, redirect
from questions import questions
from resultats import resultats, noms

from os import urandom

# On crée l'application = instance de la classe Flask
app = Flask(__name__)
# On définit la secret_key de l'app Flask pour pouvoir créer des cookies
# Sans cette clef on a une erreur quand on utilise session
# Cette clef permet de SIGNER les cookies de session => SECURISE LE SITE
app.secret_key = urandom(32)
# Secret Key est aussi utilisé pour les flash msg et pour les tokens

# On crée le route pour la page d'accueil avec le décorateur @app
#  @app.route() associe une adresse URL à une fonction
# "/" pour la page d'accueil
@app.route("/")
def index():
    # Cookie pour savoir quelle est la question actuelle
    session["numero_question"] = 0
    # Cookie pour stoker les scores = les réponses de l'utilisateur
    session["score"] =  {"J":0 , "V":0, "M":0, "C":0}
    # On affiche notre page d'accueil
    return render_template("index.html")


# On crée le route pour les questions
#  @app.route() associe une adresse URL à une fonction
# "/" pour la page d'accueil
@app.route("/question")
def question():
    # Permet de réaliser des modifications à questions de manière global
    global questions 
    # On récupère grâce au cookie le numéro de la question actuelle
    numero = session["numero_question"]

    # On vérifie qu'il reste des questions
    if numero < len(questions):
        # On récupère l'énoncé
        enonce_question = questions[numero]["enonce"]
        # On copie le dictionnaire de question
        symboles_et_reponses = questions[numero].copy()

        #POUR COMPTER LES SCORES ET AFFICHER LES REPONSES POSSIBLES
        # On retire l'enonce du dictionnaire de la question
        symboles_et_reponses.pop("enonce")
        # On crée une liste des reponses (les valeurs du dictionnaire)
        reponses = list(symboles_et_reponses.values())
        # On crée une liste des symboles = nom des perso  (les clefs du dictionnaire)
        symboles = list(symboles_et_reponses.keys())
        # On stocke les symboles et leur ordre dans un cookie
        session["symboles"] = symboles
        # On affiche notre page de la question  
        return render_template("question.html", enonce = enonce_question, reponses = reponses, symboles = symboles )
    # S'il n'y a plus de questions on affiche le resultat
    else :
        # On recupère le score et notamment le symbole qui a eu le plus de réponse associé
        # Sorted trie les scores et renvoie une liste
        # reverse = True -> la liste est triée par ordre décroissant 
        scores_tries = sorted(session["score"], key = session["score"].get, reverse = True)
        # On récupère le symbole qui a le plus de points -> INITIAL DU GAGNANT
        gagnant = scores_tries[0]
        # On recup le nom du gagnant
        nom_gagnant = noms[gagnant]
        # On récupère la description correspondante
        resultat_description = resultats[gagnant]
        # On affiche le resultat
        return render_template("resultat.html", nom_gagnant = nom_gagnant ,resultat_description = resultat_description)


# route reponse pour comptabiliser les scores et passer à la question suivante
@app.route("/reponse/<numero>")
def reponse(numero):
    # On récupère le symbole associé à la réponse sélectionné
    # conversion de numero : str -> int car on l'utilise comme indice pour récupérer le bon symbole
    symbole = session["symboles"][int(numero)]
    # On incrémente le score correspondant
    session["score"][symbole] += 1
    # On incrémente le cookie numero_question pour passer à la suivante
    session["numero_question"] +=1 
    # On redirige vers  la question suivante
    return redirect("/question")

####################################
#  TOUJOURS A LA FIN DU CODE       #
####################################
# Lancement de l'application
# HOST : précise qui a accès au serveur Flask (0.0.0.0 = toutes les adresses de la machines )
# Port d'entrée au serveur via le port 81
app.run(host="0.0.0.0", port = 81)