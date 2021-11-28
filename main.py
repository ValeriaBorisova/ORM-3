import datetime
from os import abort

from flask import Flask, request
from flask import jsonify
from  flask_sqlalchemy import SQLAlchemy
from toml.decoder import unicode

app = Flask(_name_)
app.config["SQLALCHEMY_DATABASE_URL"] = "sqlite://taxi.sqlite"
db = SQLAlchemy(app)

# db. create all()

class Drivers(db.Model):
    _tablename_ = 'drivers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    car = db.Column(db.String(100),nullable=False)

    def __init__(self, name, car):
        self.name = name
        self.car = car

class Clients(db.Model):
    _tablename_ = 'clients'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    is_vip = db.Column(db.Boolean, nullable=False)

    def __init__(self, name, order, is_vip):
        self.name = name
        self.order = order
        self.is_vip = is_vip


class Reservations(db.Model):
    _tablename_ = 'reservations'

    client_id = db.Column(db.Integer, primary_key=True)
    driver_id = db.Column(db.Integer, primary_key=True)
    address_from = db.Column(db.String(100), nullable=False)
    address_to = db.Column(db.String(100), nullable=False)
    date_created = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(100), nullable=False)


    def __init__(self, client_id, driver_id, address_from, address_to, date_created, status):
        self.client_id = client_id
        self.driver_id = driver_id
        self.address_from = address_from
        self.address_to = address_to
        self.date_created = date_created
        self.status = status


@app.route('/drivers/<int:id>', methods=['GET'])
def get_driver_by_id(id):
    driver = Drivers.query.filter_by(id=id).first_or_404()
    data = {"id": driver.id, "name": driver.name, "car": driver.car}
    return jsonify(data), 200

@app.route('/drivers', methods=['POST'])
def create_driver():
    json = request.get_json()
    driver = Drivers(name=json.get('name'), car=json.get('car'))
    db.session.add(driver)
    db.session.commit()
    return f"Водитель добавлен с даннымиЖ id: {driver.id}", 201

@app.route('/drivers/<int:id>', methods=['DELETE'])
def delete_driver(id):
    delete_driver = Drivers.query.filter_by(id=id).first_or_404()
    db.session.delete(delete_driver)
    db.session.commit()
    return f"Удален  водитель с id : {id}", 204


@app.route('/clients/<int: id>', methods=['GET'])
def get_client_by_id(id):
    client = Clients.query.filter_by(id=id).first_or_404()
    data = {"id": client.id, "name": client.name,  "is_vip": client.is_vip, "order": client.order}
    return jsonify(data), 200


@app.route('/clients/<int:id>', methods=['DELETE'])
def delete_client(id):
    delete_client = Clients.query.filter_by(id=id).first_or_404()
    db.session.delete(delete_client)
    db.session.commit()
    return f"Удален клинт с id : {id}", 204

@app.route('/clients', methods=['POST'])
def create_client():
    json = request.get_json()
    client = Clients(name=json.get('name'), is_vip=json.get('is_vip'))
    db.session.add(client)
    db.session.commit()
    return f"Клиент добавлен с данными id: {client.id}", 201


@app.route('/reservations/<int: id>', methods=['GET'])
def get_reservation_by_id(id):
    reservation = Reservations.query.filter_by(id=id).first_or_404()
    data = {"id": order.id,
            "client_id": order.client_id,
            "driver_id": order.driver_id,
            "date_created": order.date_created,
            "status": order.status,
            "address_from": order.address_from,
            "address_to": order.address_to}
    return jsonify(data), 200


@app.route('/reservations', methods=['POST'])
def create_reservation():
    json = request.get_json()
    client_id = json.get('client_id')
    driver_id = json.get('driver_id')
    client = Clients.query.filter_by(id=client_id).first()
    driver = Drivers.query.filter_by(id=driver_id).first()
    reservation = Reservations(address_from=json.get('address_from'),
                               address_to=json.get('address_to'),
                               client_id=json.get('client_id'),
                               driver_id=json.get('driver_id'),
                               date_created=datetime.datetime.now(),
                               status='not_accepted')
    db.session.add(reservation)
    db.session.commit()
    return f"Заказ добавлен с данными id: {reservation.id}", 201


@app.route('/reservatons/<id>', methods=['PUT'])
def update_reservation(reservation_id):


       reservation_id = filter(lambda r: r['id'] == reservation_id,)
        if len(reservation_id) == 0:
            abort(404)
        if not request.json:
            abort(400)
        if 'Заказ удален' in request.json and type(request.json['Заказ удален']) != unicode:
            abort(400)
        if 'Заказ отменен' in request.json and type(request.json['Заказ отменен']) is not unicode:
            abort(400)
        if 'Отмена заказа' in request.json and type(request.json['Щтмена заказа']) is not bool:
            abort(400)
        reservation_id[0]['Заказ удален'] = request.json.get('Заказ удален', reservation_id[0]['Заказ удален'])
        reservation_id[0]['Заказ отменен'] = request.json.get('Заказ отменен', reservation_id[0]['Заказ отменен'])
        reservation_id[0]['Отмена заказа'] = request.json.get('Щтмена заказа', reservation_id[0]['Отмена заказа'])
        return jsonify({'Заказ отменен': reservation_id[0]})
        else:
            reservation_id: {reservation.id} =  201
