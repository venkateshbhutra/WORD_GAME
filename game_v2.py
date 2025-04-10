

from flask import Flask, render_template_string, request, redirect, url_for
import pandas as pd
import random

app = Flask(__name__)

# Load word pairs from Excel file
def load_word_pairs(file_path):
    df = pd.read_excel(file_path)  # Assumes headers: "German", "English"
    return df[['German', 'English']].dropna().to_dict(orient='records')

# Load word pairs once at app startup
word_pairs = load_word_pairs("vocab.xlsx")

@app.route('/', methods=['GET', 'POST'])
def index():
    # Get a random word pair
    if request.method == 'POST':
        index = int(request.form['index'])
        word = word_pairs[index]['English']
        translation = word_pairs[index]['German']
        show_translation = request.form.get('show_translation') == 'yes'
    else:
        index = random.randint(0, len(word_pairs) - 1)
        word = word_pairs[index]['English']
        translation = word_pairs[index]['German']
        show_translation = False

    return render_template_string("""
        <html>
            <head>
                <title>German Practice</title>
            </head>
            <body>
                <h1>German Word Practice</h1>
                <p style="font-size:24px;">English Word</p>
                <p style="font-size:24px;"><strong>{{ word }}</strong></p>

                {% if show_translation %}
                    <p style="font-size:20px; color:green;">Translation: <strong>{{ translation }}</strong></p>
                {% endif %}

                <form method="POST">
                    <input type="hidden" name="index" value="{{ index }}">
                    <input type="hidden" name="show_translation" value="yes">
                    <button type="submit">Show Translation</button>
                </form>

                <form method="GET">
                    <button type="submit">New Word</button>
                </form>
            </body>
        </html>
    """, word=word, translation=translation, show_translation=show_translation, index=index)

if __name__ == '__main__':
    app.run(debug=False)
