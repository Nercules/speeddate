from flask import Flask, render_template

app = Flask(__name__)


# Add questions here or adjust existing questions.
QUESTIONS = [
    "What could someone wake you up for in the middle of the night?",
    "What is the best trip you have ever taken?",
    "Which skill would you love to learn right away?",
    "What was your favourite subject at school?",
    "What are you grateful for at the moment?",
    "What does your ideal day off look like?",
    "Which movie or series could you keep watching forever?",
    "What did you want to be when you grew up?",
    "Which famous person would you like to swap lives with for a day?",
    "If you could wake up anywhere in the world tomorrow, where would it be?",
    "Which small habit makes your day better?",
    "What is at the top of your bucket list?",
    "What is your favourite season and why?",
    "What music do you put on to cheer yourself up?",
    "What would you do if you had a whole month off?",
    "What is a talent of yours that few people know about?",
    "Which invention could you really not do without?",
    "What is your favourite tradition?",
    "What topic could you talk about for hours?",
    "What would you love to experience all over again?",
    "Which dish could you eat every single week?",
    "Where do you truly unwind?",
    "Which quality do you value most in a friend?",
    "What is something you are secretly quite proud of?",
    "If you could choose one superpower, which one would it be?",
    "What makes an evening truly great for you?",
    "Which hobby or activity would you love to try?",
    "When did you last step outside your comfort zone?",
    "What is a small gesture that means a lot to you?",
    "Which dream do you hope to make come true one day?",
]


@app.get("/")
def index():
    return render_template("index.html", questions=QUESTIONS)


@app.get("/health")
def health():
    return "ok"


if __name__ == "__main__":
    app.run()
