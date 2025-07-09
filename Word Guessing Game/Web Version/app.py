# Import necessary modules
from flask import Flask, render_template, request, session  # Flask core, templates, form data, session tracking
import random  # For selecting a random letter
import string  # For accessing ASCII uppercase letters

# Create a Flask application instance
app = Flask(__name__)

# Secret key is required to use sessions securely (replace with a stronger key in production)
app.secret_key = 'your_secret_key_here'

# Maximum number of attempts allowed per game
MAX_ATTEMPTS = 10

# Route for both GET (page load) and POST (form submission) methods
@app.route('/', methods=['GET', 'POST'])
def index():
    # If the game hasn't started yet (no secret letter in session), initialize it
    if 'secret_letter' not in session:
        session['secret_letter'] = random.choice(string.ascii_uppercase)  # Choose a random letter A-Z
        session['attempts'] = 0  # Initialize attempt counter
        session['game_over'] = False  # Game is active

    message = ''     # Message to show to the user
    success = False  # Flag for whether the guess was correct

    # If form was submitted and game is still active
    if request.method == 'POST' and not session.get('game_over', False):
        guess = request.form['guess'].strip().upper()  # Get and sanitize user input

        # If user exceeded the allowed number of attempts
        if session['attempts'] >= MAX_ATTEMPTS:
            message = f"🚫 Maximum of {MAX_ATTEMPTS} attempts reached. The secret letter was '{session['secret_letter']}'."
            session['game_over'] = True  # Mark game as over
        else:
            session['attempts'] += 1  # Increment attempt counter

            # Validate input
            if len(guess) != 1 or guess not in string.ascii_uppercase:
                message = "❌ Invalid input. Please enter a single letter (A–Z)."
            elif guess < session['secret_letter']:
                message = "🔽 Too low in the alphabet! Try a higher letter."
            elif guess > session['secret_letter']:
                message = "🔼 Too high in the alphabet! Try a lower letter."
            else:
                # Correct guess
                message = f"🎉 Correct! The secret letter was '{session['secret_letter']}'!<br>"
                message += f"✅ You guessed it in {session['attempts']} attempt(s)."
                success = True
                session['game_over'] = True  # Mark game as complete

            # If the last guess used up all attempts
            if not success and session['attempts'] >= MAX_ATTEMPTS:
                message += f"<br>🚫 You've reached the maximum of {MAX_ATTEMPTS} attempts. The secret letter was '{session['secret_letter']}'."
                session['game_over'] = True

    # Handle "Play Again" button click
    if request.form.get('action') == 'play_again':
        # Clear the session to reset the game
        session.pop('secret_letter', None)
        session.pop('attempts', None)
        session.pop('game_over', None)
        return render_template('index.html', message='', success=False)  # Reload the game

    # Render the main game page with message and status
    return render_template('index.html', message=message, success=success)

# Run the Flask app on localhost with debug mode enabled
if __name__ == "__main__":
    app.run(debug=True, host='localhost')
