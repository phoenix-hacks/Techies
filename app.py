from flask import Flask, render_template

# Initialize Flask app
app = Flask(__name__, static_folder='../frontend/static', template_folder='../frontend/templates')

# Home route to render index.html
@app.route('/')
def index():
    return render_template('index.html')

# Start the Flask app
if __name__ == '__main__':
    app.run(debug=True)
