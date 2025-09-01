from app import create_app, db
from flask import Flask,jsonify
app = create_app()

@app.route('/')
def home():
    return jsonify({"message": "Welcome to waste2worth page"})
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    print(app.url_map)

    app.run(debug=True)
