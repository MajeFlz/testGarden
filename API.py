import aiomysql
from flask import Flask, jsonify, request
from app.settings import settings
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


async def get_pool() -> aiomysql.Pool:
    return await aiomysql.create_pool(**settings.database.__dict__, autocommit=True)


async def execute_query(query: str, *args) -> any:
    pool = await get_pool()
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute(query, args)
            return await cur.fetchall()


async def get_users() -> list:
    result = await execute_query("SELECT user_id, score FROM users ORDER BY score DESC")
    return [{'user_id': row[0], 'score': row[1]} for row in result]


@app.route('/api/users', methods=['GET'])
async def get_users_list():
    users = await get_users()
    return jsonify(users)


async def get_score(user_id: int) -> int:
    result = await execute_query("SELECT score FROM users WHERE user_id = %s", user_id)
    return result[0][0] if result else None


@app.route('/api/users/score', methods=['GET'])
async def get_user_score():
    user_id = request.args.get('user_id')

    if not user_id:
        return jsonify({'error': 'User ID is required'}), 400

    try:
        user_id = int(user_id)
    except ValueError:
        return jsonify({'error': 'Invalid user ID'}), 400

    score = await get_score(user_id)
    if score is None:
        return jsonify({'error': 'User not found'}), 404

    return jsonify({'user_id': user_id, 'score': score})


async def inc_score(user_id: int) -> int:
    result = await execute_query("UPDATE users SET score = score + 1 WHERE user_id = %s", user_id)
    return result


@app.route('/api/users/increase-score', methods=['POST'])
async def increase_user_score():
    data = request.json
    user_id = data.get('user_id')

    if user_id is None:
        return jsonify({'error': 'User ID is required'}), 400

    try:
        user_id = int(user_id)
    except ValueError:
        return jsonify({'error': 'Invalid user ID'}), 400

    result = await inc_score(user_id)

    if result is None:
        return jsonify({'error': 'User not found'}), 404

    return jsonify({'message': 'User score increased successfully'})


async def update_wallet(user_id: int, wallet: int) -> int:
    result = await execute_query("UPDATE users SET wallet = %s WHERE user_id = %s", wallet, user_id)
    return result


@app.route('/api/users/update_wallet', methods=['POST'])
async def update_user_wallet():
    data = await request.get_json()
    user_id = data.get('user_id')
    wallet = data.get('wallet')

    if user_id is None:
        return jsonify({"error": "User ID is required"}), 400

    try:
        result = await update_wallet(user_id, wallet)
        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
