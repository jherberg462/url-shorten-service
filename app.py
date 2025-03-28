from flask import Flask, request, redirect, render_template
import os
import psycopg2
import hashlib
import random
import string
from urllib.parse import urlparse

app = Flask(__name__)
DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://localhost/url_shortener')
def to_base62(num):
    chars = string.ascii_letters + string.digits
    result = []
    while num:
        num, rem = divmod(num, 62)
        result.append(chars[rem])
    return ''.join(result[::-1]) or 'a'

def generate_short_code(long_url, length=6, retries=5):
    conn = psycopg2.connect(DATABASE_URL)
    c = conn.cursor()
    for _ in range(retries):
        salt = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        hash_input = (long_url + salt).encode('utf-8')
        hash_obj = hashlib.md5(hash_input)
        hash_int = int(hash_obj.hexdigest(), 16)
        code = to_base62(hash_int)[:length]
        c.execute('SELECT 1 FROM urls WHERE short_code = %s', (code,))
        if not c.fetchone():
            conn.close()
            return code
    conn.close()
    raise Exception("Failed to generate unique code after retries")

def init_db():
    conn = psycopg2.connect(DATABASE_URL)
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS urls (short_code TEXT PRIMARY KEY, long_url TEXT)')
    conn.commit()
    conn.close()

def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        long_url = request.form['url']
        if not is_valid_url(long_url):
            return "Invalid URL", 400
        short_code = generate_short_code(long_url)
        conn = psycopg2.connect(DATABASE_URL)
        c = conn.cursor()
        try:
            c.execute('INSERT INTO urls (short_code, long_url) VALUES (%s, %s)', (short_code, long_url))
            conn.commit()
        except psycopg2.IntegrityError:
            conn.rollback()
            return "Error: Try again (code collision)", 500
        conn.close()
        return render_template('index.html', short_url=f'{request.host_url}{short_code}')
    return render_template('index.html', short_url=None)

@app.route('/<short_code>')
def redirect_url(short_code):
    # Validate short_code length (must be exactly 6 characters)
    if len(short_code) != 6:
        return 'Invalid short URL', 400
    
    conn = psycopg2.connect(DATABASE_URL)
    c = conn.cursor()
    c.execute('SELECT long_url FROM urls WHERE short_code = %s', (short_code,))
    result = c.fetchone()
    conn.close()
    if result:
        return redirect(result[0])
    return 'URL not found', 404

if __name__ == '__main__':
    init_db()
    app.run(debug=True)