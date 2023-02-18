from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///calls.db'
db = SQLAlchemy(app)

class Call(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    from_number = db.Column(db.String(15), nullable=False)
    to_number = db.Column(db.String(15), nullable=False)
    start_time = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "from_number": self.from_number,
            "to_number": self.to_number,
            "start_time": self.start_time.isoformat()
        }

@app.route('/initiate-call', methods=['POST'])
def initiate_call():
    from_number = request.json.get('from_number')
    to_number = request.json.get('to_number')

    if not from_number or not to_number:
        return jsonify(error='Invalid request data'), 400

    call = Call(from_number=from_number, to_number=to_number)
    db.session.add(call)
    db.session.commit()

    return jsonify(success=True), 201

@app.route('/call-report', methods=['GET'])
def call_report():
    phone_number = request.args.get('phone')
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=10, type=int)

    if not phone_number:
        return jsonify(error='Invalid request data'), 400

    calls = Call.query.filter((Call.from_number == phone_number) | (Call.to_number == phone_number)) \
        .order_by(Call.start_time.desc()) \
        .paginate(page=page, per_page=per_page)

    return jsonify(success=True, data=[call.to_dict() for call in calls.items], has_next=calls.has_next)

if __name__ == '__main__':
    app.run(debug=True)
