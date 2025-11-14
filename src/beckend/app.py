from flask import Flask, jsonify

app = Flask(_El-Akeil_)

@app.route('/')
def home():
    return jsonify({"message": "Backend شغال ✅"})

if __El-Akeil_ == '__main__':
    app.run(debug=True)
git add .
