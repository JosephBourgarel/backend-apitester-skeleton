import pathlib as pl

import numpy as np
import pandas as pd

from flask import Flask, jsonify, request, make_response
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

data = pl.Path(__file__).parent.absolute() / 'data'

# Charger les données CSV
associations_df = pd.read_csv(data / 'associations_etudiantes.csv')
evenements_df = pd.read_csv(data / 'evenements_associations.csv')

## Vous devez ajouter les routes ici : 
@app.route("/api/alive", methods = ['GET'])
def en_fonctionnement():
    return make_response(jsonify({ "message": "Alive" }), 200)


@app.route("/api/associations", methods = ['GET'])
def id_associations():
    id_assos = associations_df['id'].unique().to_list()
    return make_response(jsonify({'message' : id_assos}), 200)

@app.route("/api/associations/<int:id>", methods = ["GET"])
def details_assos(id):
    if id in associations_df['id'].unique():
        details = associations_df.loc[id].to_dict()
        return make_response(jsonify(details), 200)
    else:
        return make_response(jsonify({ "error": "Association not found" }), 404)
    

@app.route("/api/evenements", methods = ['GET'])
def events():
    return make_response(jsonify({'message': f'{evenements_df['id'].unique().to_list()}'}), 200)


@app.route("/api/evenement/<int:id>", methods = ['GET'])
def details_events(id):
    if id in evenements_df['id'].unique():
        details = evenements_df.loc[id].to_dict()
        return make_response(jsonify(details), 200)
    else:
        return make_response(jsonify({ "error": "Event not found" }), 404)


@app.route('/api/association/<int:id>/evenements', methods = ['GET'])
def events_par_assos():
    events_assos = dict()
    for id_asso in associations_df['id'].unique():
        events_assos[id_asso] = evenements_df[evenements_df['association_id'] == id_asso].to_list()
    return make_response(jsonify(events_assos), 200)


@app.route('/api/associations/type/<type>', methods = ['GET'])
def par_type():
    assos_type = dict()
    for type in associations_df['type'].unique():
        assos_type[type] = associations_df[associations_df['type'] == 'BDE']['nom'][0]
    return make_response(jsonify(assos_type), 200)


if __name__ == '__main__':
    app.run(debug=False)
