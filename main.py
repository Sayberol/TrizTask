# TRIZ
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///services.db'
db = SQLAlchemy(app)


class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    condition = db.Column(db.String(20))
    description = db.Column(db.Text)

db.create_all()


@app.route('/services', methods=['GET'])
def get_services():
    services = Service.query.all()
    services_list = [{'name': service.name, 'condition': service.condition} for service in services]
    return jsonify({'services': services_list})


@app.route('/services/name', methods=['GET'])
def get_service(name):
    service = Service.query.filter_by(name=name).all()
    service_list = [{'condition': s.condition, 'description': s.description, 'timestamp': s.id} for s in service] # timestamp - временная метка, используется для отслеживания истории изменения состояния сервиса
    return jsonify({'history': service_list})


@app.route('/services', methods=['POST'])
def add_service():
    data = request.get_json()
    name = data['name']
    condition = data['condition']
    description = data.get['description', '']

    service = Service(name=name, condition=condition, description=description)
    db.session.add(service)
    db.session.commit()
    return jsonify({'message': "Добавлен успешно!"})



if __name__ == '__main__':
    app.run(debug=True)