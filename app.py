from flask import Flask, render_template

app = Flask(__name__)


# Voeg hier vragen toe of pas bestaande vragen aan.
QUESTIONS = [
    "Waar kun je midden in de nacht voor wakker worden gemaakt?",
    "Wat is de beste reis die je ooit hebt gemaakt?",
    "Welke vaardigheid zou je meteen willen leren?",
    "Wat was jouw favoriete vak op school?",
    "Waar ben je op dit moment dankbaar voor?",
    "Wat is jouw ideale vrije dag?",
    "Welke film of serie kun je blijven kijken?",
    "Wat wilde je vroeger worden?",
    "Met welke bekende persoon zou je een dag willen ruilen?",
    "Wat is het beste advies dat je ooit hebt gekregen?",
    "Welke kleine gewoonte maakt jouw dag beter?",
    "Wat staat er bovenaan jouw bucketlist?",
    "Wat is jouw favoriete seizoen en waarom?",
    "Welke muziek zet je op om vrolijk te worden?",
    "Wat zou je doen als je een maand helemaal vrij was?",
    "Wat is een talent van jou dat weinig mensen kennen?",
    "Welke uitvinding kun je echt niet missen?",
    "Wat is jouw favoriete traditie?",
    "Waar moest je voor het laatst heel hard om lachen?",
    "Wat zou je graag nog eens opnieuw beleven?",
    "Welk gerecht zou je iedere week kunnen eten?",
    "Waar kom jij helemaal tot rust?",
    "Welke eigenschap waardeer je het meest in een vriend?",
    "Wat is iets waar je stiekem best trots op bent?",
    "Als je één superkracht mocht kiezen, welke zou dat zijn?",
    "Wat maakt voor jou een avond echt geslaagd?",
    "Welke plek in Antwerpen laat je graag aan iemand zien?",
    "Wanneer ben je voor het laatst buiten je comfortzone gestapt?",
    "Wat is een klein gebaar dat veel voor jou betekent?",
    "Welke droom hoop je ooit nog waar te maken?",
]


@app.get("/")
def index():
    return render_template("index.html", questions=QUESTIONS)


@app.get("/health")
def health():
    return "ok"


if __name__ == "__main__":
    app.run()
