from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# Define the Rule model
class Rule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rule_string = db.Column(db.Text, nullable=False)
    ast = db.Column(db.Text, nullable=False)  # Store AST as JSON
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Rename the backref to avoid conflict
    metadata_entries = db.relationship('Metadata', backref='rule', cascade='all, delete-orphan', single_parent=True)

# Metadata for rules (additional info)
class Metadata(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rule_id = db.Column(db.Integer, db.ForeignKey('rule.id'), nullable=False)
    attribute_name = db.Column(db.String(100), nullable=False)
    attribute_value = db.Column(db.String(100), nullable=False)
