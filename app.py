from flask import Flask, render_template

app = Flask(__name__)


# Voeg hier vragen toe of pas bestaande vragen aan.
# Elke vraag heeft een Nederlandse ("nl") en Engelse ("en") versie.
QUESTIONS = [
    {"nl": "Waar kun je midden in de nacht voor wakker worden gemaakt?", "en": "What could someone wake you up for in the middle of the night?"},
    {"nl": "Wat is de beste reis die je ooit hebt gemaakt?", "en": "What is the best trip you have ever taken?"},
    {"nl": "Welke vaardigheid zou je meteen willen leren?", "en": "Which skill would you love to learn right away?"},
    {"nl": "Wat was jouw favoriete vak op school?", "en": "What was your favourite subject at school?"},
    {"nl": "Waar ben je op dit moment dankbaar voor?", "en": "What are you grateful for at the moment?"},
    {"nl": "Wat is jouw ideale vrije dag?", "en": "What does your ideal day off look like?"},
    {"nl": "Welke film of serie kun je blijven kijken?", "en": "Which movie or series could you keep watching forever?"},
    {"nl": "Wat wilde je vroeger worden?", "en": "What did you want to be when you grew up?"},
    {"nl": "Met welke bekende persoon zou je een dag willen ruilen?", "en": "Which famous person would you like to swap lives with for a day?"},
    {"nl": "Als je morgen overal ter wereld wakker kon worden, waar zou dat zijn?", "en": "If you could wake up anywhere in the world tomorrow, where would it be?"},
    {"nl": "Welke kleine gewoonte maakt jouw dag beter?", "en": "Which small habit makes your day better?"},
    {"nl": "Wat staat er bovenaan jouw bucketlist?", "en": "What is at the top of your bucket list?"},
    {"nl": "Wat is jouw favoriete seizoen en waarom?", "en": "What is your favourite season and why?"},
    {"nl": "Welke muziek zet je op om vrolijk te worden?", "en": "What music do you put on to cheer yourself up?"},
    {"nl": "Wat zou je doen als je een maand helemaal vrij was?", "en": "What would you do if you had a whole month off?"},
    {"nl": "Wat is een talent van jou dat weinig mensen kennen?", "en": "What is a talent of yours that few people know about?"},
    {"nl": "Welke uitvinding kun je echt niet missen?", "en": "Which invention could you really not do without?"},
    {"nl": "Wat is jouw favoriete traditie?", "en": "What is your favourite tradition?"},
    {"nl": "Over welk onderwerp kun je urenlang praten?", "en": "What topic could you talk about for hours?"},
    {"nl": "Wat zou je graag nog eens opnieuw beleven?", "en": "What would you love to experience all over again?"},
    {"nl": "Welk gerecht zou je iedere week kunnen eten?", "en": "Which dish could you eat every single week?"},
    {"nl": "Waar kom jij helemaal tot rust?", "en": "Where do you truly unwind?"},
    {"nl": "Welke eigenschap waardeer je het meest in een vriend?", "en": "Which quality do you value most in a friend?"},
    {"nl": "Wat is iets waar je stiekem best trots op bent?", "en": "What is something you are secretly quite proud of?"},
    {"nl": "Als je één superkracht mocht kiezen, welke zou dat zijn?", "en": "If you could choose one superpower, which one would it be?"},
    {"nl": "Wat maakt voor jou een avond echt geslaagd?", "en": "What makes an evening truly great for you?"},
    {"nl": "Welke hobby of activiteit zou je graag eens willen proberen?", "en": "Which hobby or activity would you love to try?"},
    {"nl": "Wanneer ben je voor het laatst buiten je comfortzone gestapt?", "en": "When did you last step outside your comfort zone?"},
    {"nl": "Wat is een klein gebaar dat veel voor jou betekent?", "en": "What is a small gesture that means a lot to you?"},
    {"nl": "Welke droom hoop je ooit nog waar te maken?", "en": "Which dream do you hope to make come true one day?"},
]


@app.get("/")
def index():
    return render_template("index.html", questions=QUESTIONS)


@app.get("/health")
def health():
    return "ok"


if __name__ == "__main__":
    app.run()
