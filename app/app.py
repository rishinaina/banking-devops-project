from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint
from decimal import Decimal
import os

app = Flask(__name__)

DB_USER = os.getenv('DB_USER', 'bankuser')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'bankpass')
DB_HOST = os.getenv('DB_HOST', 'db')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME', 'bankdb')
DATABASE_URL = os.getenv(
    'DATABASE_URL',
    f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
)

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Account(db.Model):
    __tablename__ = 'accounts'
    id = db.Column(db.Integer, primary_key=True)
    owner_name = db.Column(db.String(100), nullable=False, default='Demo User')
    balance = db.Column(db.Numeric(12, 2), nullable=False, default=0.00)
    __table_args__ = (
        CheckConstraint('balance >= 0', name='check_balance_non_negative'),
    )


def seed_default_account() -> None:
    if Account.query.first() is None:
        account = Account(owner_name='Demo User', balance=Decimal('1000.00'))
        db.session.add(account)
        db.session.commit()


@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'}), 200


@app.route('/balance/<int:account_id>', methods=['GET'])
def get_balance(account_id: int):
    account = Account.query.get(account_id)
    if not account:
        return jsonify({'error': 'Account not found'}), 404
    return jsonify({
        'account_id': account.id,
        'owner_name': account.owner_name,
        'balance': float(account.balance)
    }), 200


@app.route('/deposit/<int:account_id>', methods=['POST'])
def deposit(account_id: int):
    account = Account.query.get(account_id)
    if not account:
        return jsonify({'error': 'Account not found'}), 404

    data = request.get_json(silent=True) or {}
    amount = data.get('amount')
    if amount is None:
        return jsonify({'error': 'Amount is required'}), 400

    amount = Decimal(str(amount))
    if amount <= 0:
        return jsonify({'error': 'Amount must be greater than zero'}), 400

    account.balance = Decimal(str(account.balance)) + amount
    db.session.commit()

    return jsonify({
        'message': 'Deposit successful',
        'account_id': account.id,
        'new_balance': float(account.balance)
    }), 200


@app.route('/withdraw/<int:account_id>', methods=['POST'])
def withdraw(account_id: int):
    account = Account.query.get(account_id)
    if not account:
        return jsonify({'error': 'Account not found'}), 404

    data = request.get_json(silent=True) or {}
    amount = data.get('amount')
    if amount is None:
        return jsonify({'error': 'Amount is required'}), 400

    amount = Decimal(str(amount))
    if amount <= 0:
        return jsonify({'error': 'Amount must be greater than zero'}), 400

    if Decimal(str(account.balance)) < amount:
        return jsonify({'error': 'Insufficient balance'}), 400

    account.balance = Decimal(str(account.balance)) - amount
    db.session.commit()

    return jsonify({
        'message': 'Withdrawal successful',
        'account_id': account.id,
        'new_balance': float(account.balance)
    }), 200


@app.route('/init', methods=['POST'])
def initialize():
    db.create_all()
    seed_default_account()
    return jsonify({'message': 'Database initialized'}), 200


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        seed_default_account()
    app.run(host='0.0.0.0', port=5000)
