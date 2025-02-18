from flask import Blueprint, request, jsonify
from app.models import Player
from app.database import db
import random

auction_bp = Blueprint('auction', __name__)

teams = {}
max_players_per_team = 0
auction_queue = []

@auction_bp.route('/setup_teams', methods=['POST'])
def setup_teams():
    global teams, max_players_per_team
    data = request.get_json()
    num_teams = data['num_teams']
    max_players_per_team = data['max_players']
    budgets = data['budgets']

    teams.clear()
    for i in range(num_teams):
        team_name = f"Team {i + 1}"
        teams[team_name] = {"budget": budgets[i], "players": [], "player_count": 0}

    return jsonify({"message": "Teams setup successfully", "teams": teams})

@auction_bp.route('/add_players', methods=['POST'])
def add_players():
    data = request.get_json()
    players = data['players']

    for p in players:
        player = Player(name=p['name'], base_price=p['base_price'])
        db.session.add(player)

    db.session.commit()

    return jsonify({"message": "Players added successfully!"})

@auction_bp.route('/randomize_players', methods=['GET'])
def randomize_players():
    global auction_queue
    available_players = Player.query.filter_by(status='Available').all()
    auction_queue = random.sample(available_players, len(available_players))

    return jsonify({"message": "Players randomized", "queue_size": len(auction_queue)})

@auction_bp.route('/get_next_player', methods=['GET'])
def get_next_player():
    global auction_queue
    if not auction_queue:
        return jsonify({"message": "Auction finished!", "player": None})

    current_player = auction_queue.pop(0)
    return jsonify({
        "id": current_player.id,
        "name": current_player.name,
        "base_price": current_player.base_price,
        "status": current_player.status,
    })

@auction_bp.route('/submit_bid', methods=['POST'])
def submit_bid():
    global teams, max_players_per_team
    data = request.get_json()

    player_id = data['player_id']
    team_name = data['team_name']
    bid_amount = data['bid_amount']

    if team_name not in teams:
        return jsonify({"error": "Team not found"}), 400

    if teams[team_name]['budget'] < bid_amount:
        return jsonify({"error": "Insufficient budget"}), 400

    if teams[team_name]['player_count'] >= max_players_per_team:
        return jsonify({"error": "Max players reached"}), 400

    player = Player.query.get(player_id)

    if not player or player.status != 'Available':
        return jsonify({"error": "Player not available"}), 400

    # Update Player in DB
    player.status = 'Sold'
    player.sold_to = team_name
    player.sold_price = bid_amount

    db.session.commit()

    # Update Team
    teams[team_name]['budget'] -= bid_amount
    teams[team_name]['players'].append(player_id)
    teams[team_name]['player_count'] += 1

    return jsonify({"message": f"Player {player.name} sold to {team_name} for {bid_amount}"})

@auction_bp.route('/get_auction_summary', methods=['GET'])
def get_auction_summary():
    sold_players = Player.query.filter_by(status='Sold').all()
    unsold_players = Player.query.filter_by(status='Available').all()

    sold_players_data = [{
        'id': p.id,
        'name': p.name,
        'base_price': p.base_price,
        'sold_to': p.sold_to,
        'sold_price': p.sold_price
    } for p in sold_players]

    unsold_players_data = [{
        'id': p.id,
        'name': p.name,
        'base_price': p.base_price
    } for p in unsold_players]

    return jsonify({
        "teams": teams,
        "sold_players": sold_players_data,
        "unsold_players": unsold_players_data
    })
