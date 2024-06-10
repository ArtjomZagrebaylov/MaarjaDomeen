from flask import Flask, request, jsonify, send_from_directory
import sqlite3
import os

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
              CREATE TABLE IF NOT EXISTS domain_purchase
              (id INTEGER PRIMARY KEY AUTOINCREMENT,
              domain TEXT, firstName TEXT, lastName TEXT, dob TEXT,
              telephone TEXT, email TEXT, streetAddress TEXT,
              city TEXT, state TEXT, postalCode TEXT, country TEXT,
              paymentMethod TEXT)
              ''')
    conn.commit()
    conn.close()

@app.route('/save', methods=['POST'])
def save():
    try:
        data = request.get_json()
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('''
                  INSERT INTO domain_purchase (domain, firstName, lastName, dob,
                  telephone, email, streetAddress, city, state, postalCode, country,
                  paymentMethod)
                  VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                  (data.get('domain'), data.get('firstName'), data.get('lastName'),
                   data.get('dob'), data.get('telephone'), data.get('email'),
                   data.get('streetAddress'), data.get('city'), data.get('state'),
                   data.get('postalCode'), data.get('country'), data.get('paymentMethod')))
        conn.commit()
        conn.close()
        return jsonify({'success': True})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/')
def index():
    return send_from_directory(os.getcwd(), 'index.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
