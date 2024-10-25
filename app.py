from flask import Flask, jsonify, request, render_template
from models import db, Rule
from rule_engine import create_rule, combine_rules, evaluate_rule
import json
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)

# SQLite Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Ensure tables are created
with app.app_context():
    db.create_all()

# Route to serve the HTML page
@app.route('/')
def index():
    return render_template('index.html')

# Route to create rules
@app.route('/create_rule', methods=['POST'])
def create_rule_api():
    try:
        rule_string = request.json.get('rule_string')
        ast = create_rule(rule_string)
        new_rule = Rule(rule_string=rule_string, ast=json.dumps(ast.to_dict()))  # Convert AST to dict for JSON
        db.session.add(new_rule)
        db.session.commit()
        return jsonify({'message': 'Rule created', 'rule_id': new_rule.id}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Rule already exists'}), 409
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route to combine rules
@app.route('/combine_rules', methods=['POST'])
def combine_rules_api():
    rule_ids = request.json.get('rule_ids')
    if not rule_ids:
        return jsonify({'error': 'No rule IDs provided'}), 400

    rules = Rule.query.filter(Rule.id.in_(rule_ids)).all()
    if not rules:
        return jsonify({'error': 'No rules found for the provided IDs'}), 404

    rule_nodes = [json.loads(rule.ast) for rule in rules]
    combined_ast = combine_rules(rule_nodes)
    return jsonify({'combined_ast': combined_ast}), 200

# Route to evaluate rule
@app.route('/evaluate_rule/<int:rule_id>', methods=['POST'])
def evaluate_rule_api(rule_id):
    try:
        data = request.json
        rule = Rule.query.get(rule_id)
        if not rule:
            return jsonify({'error': 'Rule not found'}), 404

        ast = json.loads(rule.ast)
        result = evaluate_rule(ast, data)
        return jsonify({'result': result}), 200
    except Exception as e:
        print(f"Error evaluating rule: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
