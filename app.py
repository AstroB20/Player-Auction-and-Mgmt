from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# MySQL Configuration
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Tiger",
    database="player_mgmt"
)
cursor = conn.cursor()

# Routes
@app.route('/')
def index():
    cursor.execute("SELECT * FROM players")
    players = cursor.fetchall()
    return render_template('index.html', players=players)

@app.route('/player/<int:player_id>', methods=['GET', 'POST'])
def player_detail(player_id):
    if request.method == 'POST':
        bidder_name = request.form['bidder_name']
        bid_amount = float(request.form['bid_amount'])
        cursor.execute("INSERT INTO bids (player_id, bidder_name, bid_amount) VALUES (%s, %s, %s)",
                       (player_id, bidder_name, bid_amount))
        conn.commit()
        return redirect(f'/player/{player_id}')

    cursor.execute("SELECT * FROM players WHERE id = %s", (player_id,))
    player = cursor.fetchone()
    cursor.execute("SELECT * FROM bids WHERE player_id = %s ORDER BY bid_amount DESC", (player_id,))
    bids = cursor.fetchall()
    return render_template('player_detail.html', player=player, bids=bids)

@app.route('/add_player', methods=['GET', 'POST'])
def add_player():
    if request.method == 'POST':
        name = request.form['name']
        position = request.form['position']
        base_price = float(request.form['base_price'])
        cursor.execute("INSERT INTO players (name, position, base_price) VALUES (%s, %s, %s)",
                       (name, position, base_price))
        conn.commit()
        return redirect('/')

    return render_template('add_player.html')

if __name__ == '__main__':
    app.run(debug=True)
