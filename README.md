# Rule Engine Application
This project is a rule engine built with Flask, enabling users to create, store, combine, and evaluate complex rules using an Abstract Syntax Tree (AST). The application provides a web interface for interaction and a REST API for programmatic access.

# Table of Contents
- [Features](#features)
- [Project Structure](#project-structure)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Data Model](#data-model)
  
# Features
- Create Rules: Define rules with logical expressions involving operators (`AND`, `OR`) and store them in a SQLite database.
- Combine Rules: Combine multiple stored rules using logical operators for complex rule evaluation.
- Evaluate Rules: Test if rules are satisfied based on dynamic input data, supporting custom conditions on user attributes.

# Project Structure
```plaintext
rule_engine_app/
│
├── app.py             # Main application with route handling
├── models.py          # Database model for Rule table
├── rule_engine.py     # Core rule creation, combination, and evaluation logic
├── templates/
│   └── index.html     # HTML file for the UI
├── requirements.txt   # Project dependencies
└── database.db        # SQLite database file
Key Files
app.py: Contains Flask routes to interact with the rule engine API.
models.py: Defines the database schema for storing rules.
rule_engine.py: Implements rule parsing, AST construction, and evaluation logic.
index.html: Provides a simple UI to interact with the application.

Setup Instructions
Prerequisites
Python 3.8+
Flask and SQLAlchemy
Installation
Clone the Repository:

bash
Copy code
git clone https://github.com/your-username/rule_engine_app.git
cd rule_engine_app
Create a Virtual Environment:

bash
Copy code
python -m venv venv
source venv/bin/activate   # On macOS/Linux
venv\Scripts\activate      # On Windows
Install Dependencies:

bash
Copy code
pip install -r requirements.txt

Set Up the Database:
Run the following commands in a Python shell to initialize the database:
python
Copy code
from app import db
db.create_all()
Run the Application:

bash
Copy code
flask run
Access the application at http://127.0.0.1:5000.

Usage
Visit the application URL to access the UI for rule management. The application also provides the following REST API endpoints.

API Endpoints
1. GET /
Description: Renders the main HTML interface.

2. POST /create_rule
Description: Creates a new rule and stores it in the database.
Request Body:
json
Copy code
{
  "rule_string": "((age > 30 AND department = 'Sales') OR (age < 25 AND department = 'Marketing')) AND (salary > 50000 OR experience > 5)"
}
Response:
201 Created: Rule successfully stored.
409 Conflict: Duplicate rule error.
500 Internal Server Error: Any other error.

3. POST /combine_rules
Description: Combines multiple rules by ID using an AND operator.
Request Body:
json
Copy code
{
  "rule_ids": [1, 2]
}
Response:
200 OK: Returns the combined AST.
404 Not Found: No matching rules for provided IDs.
500 Internal Server Error: Combination error.

4. POST /evaluate_rule/<rule_id>
Description: Evaluates a rule against provided data.
URL Parameter: rule_id - The ID of the rule to evaluate.
Request Body:
json
Copy code
{
  "age": 35,
  "department": "Sales",
  "salary": 60000,
  "experience": 6
}
Response:
200 OK: Evaluation result (true or false).
404 Not Found: Rule not found.
500 Internal Server Error: Evaluation error.

Data Model
Rule Table (models.py)
id: Unique identifier for each rule (Primary Key).
rule_string: Original rule expression.
ast: Serialized Abstract Syntax Tree (AST) representation of the rule.
