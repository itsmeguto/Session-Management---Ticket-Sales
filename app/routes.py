from flask import Blueprint, jsonify, current_app, render_template, request, redirect, url_for, flash, session
import uuid

bp = Blueprint('main', __name__)  # 'main' is the blueprint name

def generate_session_id():
    return uuid.uuid4().hex  # This generates a random UUID and converts it to a hexadecimal string

@bp.route('/test', methods=['GET'])
def test():
    return jsonify({'message': 'This is a test route'})

@bp.route('/use_redis', methods=['GET'])
def use_redis():
    redis_instance = current_app.redis
    # Use the redis_instance here
    return jsonify({'message': 'Redis used'})

@bp.route('/some_route', methods=['GET', 'POST'])
def some_route():
    current_app.logger.info('Processing some_route')
    try:
        # Your route logic here
        pass
    except Exception as e:
        current_app.logger.error('Error processing some_route', exc_info=True)


# Assuming you already have a Blueprint named 'bp'
@bp.route('/test_sales', methods=['GET'])
def test_sales():
    return render_template('test_tickets.html')


@bp.route('/create_session', methods=['POST'])
def create_session():
    # Check if the session already exists
    if 'user_id' in session:
        flash('Session already exists.')
    else:
        # Clearing the session and starting fresh:
        session.clear()  # Clears all keys
        session['user_id'] = uuid.uuid4().hex
        flash('New session created successfully.')


    return redirect(url_for('main.test_sales'))  # Adjust to your redirect preference