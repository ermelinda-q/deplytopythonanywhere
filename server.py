# Flask Server file
# Author: E. Qejvani
# Based on lectures by A. Beatty
# Use of render_template from: https://www.geeksforgeeks.org/flask-rendering-templates/ 
# and
# https://flask.palletsprojects.com/en/stable/quickstart/

from flask import Flask, jsonify, request, abort, render_template
from flask_cors import CORS, cross_origin
from fluteDAO import fluteDAO

# initializing Flask to default - imported render_template for easier mapping.
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# Mapping - I used render_template to get index.html file.
@app.route('/')
@cross_origin()
def index():
    return render_template('index.html')

# Render view_all.html page to list all flutes.
@app.route('/view_all')
@cross_origin()
def view_all():
    return render_template('view_all.html')

# Render find_flute.html page to search for flute by ID.
@app.route('/find_flute')
@cross_origin()
def find_flute():
    return render_template('find_flute.html')


# Render create_flute.html page to add a new flute.
@app.route('/create_flute')
@cross_origin()
def create_flute_page():
    return render_template('create_flute.html')

# Render update_flute.html page to update flute info.
@app.route('/update_flute')
@cross_origin()
def update_flute_page():
    return render_template('update_flute.html')


# Render delete_flute.html page to delete flute by ID.
@app.route('/delete_flute')
@cross_origin()
def delete_flute_page():
    return render_template('delete_flute.html')

# getAll() - curl "http://127.0.0.1:5000/flutes"
@app.route('/flutes', methods=["GET"])
@cross_origin()
def getAll():
    results = fluteDAO.getAll()
    return jsonify(results)


# findById() - curl "http://127.0.0.1:5000/flutes/id"
@app.route('/flutes/<int:id>', methods=["GET"])
@cross_origin()
def findById(id):
    found = fluteDAO.findByID(id)
    return jsonify(found)


# create() - curl -i -H "Content-Type:application/json" -X POST 
# -d "{\"fluteMaker\":\"Yamaha\",\"fluteModel\":\"YFL-222\",
# \"fluteLevel\":\"Beginner\",\"fluteHead\":\"Nickel\",\"fluteBody\":\"Silver\",
# \"fluteMechanism\":\"Closed\",\"priceRange\":1000}" http://127.0.0.1:5000/flutes
@app.route('/flutes', methods=['POST'])
@cross_origin()
def create():
    if not request.json:
        abort(400)
    flute = {
        "fluteMaker": request.json['fluteMaker'],
        "fluteModel": request.json['fluteModel'],
        "fluteLevel": request.json['fluteLevel'],
        "fluteHead": request.json['fluteHead'],
        "fluteBody": request.json['fluteBody'],
        "fluteMechanism": request.json['fluteMechanism'],
        "priceRange": request.json['priceRange'],
    }
    added = fluteDAO.create(flute)
    return jsonify(added)


# update() - curl -i -H "Content-Type:application/json" -X PUT -d "{\"fluteMaker\":\"Yamaha\",
# \"fluteModel\":\"YFL-221\",\"fluteLevel\":\"Intermediate\",\"fluteHead\":\"Silver\",
# \"fluteBody\":\"Silver\",\"fluteMechanism\":\"Open\",\"priceRange\":1500}" http://127.0.0.1:5000/flutes/1
@app.route('/flutes/<int:id>', methods=['PUT'])
@cross_origin()
def update(id):
    found = fluteDAO.findByID(id)
    if not found:
        abort(404)

    if not request.json:
        abort(400)
    reqJson = request.json

    for field in ['fluteMaker', 'fluteModel', 'fluteLevel', 'fluteHead', 'fluteBody', 'fluteMechanism', 'priceRange']:
        if field in reqJson:
            found[field] = reqJson[field]

    fluteDAO.update(id, found)
    return jsonify(found)


# delete() - curl -X DELETE http://127.0.0.1:5000/flutes/1
@app.route('/flutes/<int:id>', methods=['DELETE'])
@cross_origin()
def delete(id):
    fluteDAO.delete(id)
    return jsonify({"done": True})


if __name__ == '__main__':
    app.run(debug=True)
