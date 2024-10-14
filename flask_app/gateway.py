from flask import Flask, request, jsonify
import requests
import os
from lxml import etree

app = Flask(__name__)

# GeoServer and PostGIS settings from environment variables
GEOSERVER_URL = 'http://geoserver:8080/geoserver'  # GeoServer within Docker
POSTGIS_HOST = os.getenv('POSTGIS_HOST', 'postgis')
POSTGIS_DB = os.getenv('POSTGIS_DB', 'comet')
POSTGIS_USER = os.getenv('POSTGIS_USER', 'postgres')
POSTGIS_PASSWORD = os.getenv('POSTGIS_PASSWORD', 'postgres')

# Utility to create WFS-T (Web Feature Service - Transaction) XML
def build_wfs_transaction_insert(building):
    nsmap = {
        'wfs': 'http://www.opengis.net/wfs',
        'feature': 'http://www.comet.org'
    }
    
    transaction = etree.Element("{http://www.opengis.net/wfs}Transaction", nsmap=nsmap)
    insert = etree.SubElement(transaction, "{http://www.opengis.net/wfs}Insert")
    
    feature = etree.SubElement(insert, "{http://www.comet.org}buildings")
    geom = etree.SubElement(feature, "{http://www.comet.org}B_geometry")
    geom.text = building['geometry']['coordinates']  # Needs proper formatting
    
    for key, value in building['properties'].items():
        prop = etree.SubElement(feature, "{http://www.comet.org}" + key)
        prop.text = str(value)
    
    return etree.tostring(transaction, pretty_print=True)

@app.route('/insert_scenario', methods=['POST'])
def insert_scenario():
    data = request.get_json()
    project_name = data.get('projectName')
    scenario_name = data.get('scenarioName')
    buildings = data.get('buildings', [])

    # Insert scenario_project entry
    for building in buildings:
        wfs_insert_xml = build_wfs_transaction_insert(building)

        headers = {'Content-Type': 'text/xml'}
        response = requests.post(
            f"{GEOSERVER_URL}/wfs",
            data=wfs_insert_xml,
            headers=headers,
            auth=('admin', 'geoserver')
        )
        
        if response.status_code != 200:
            return jsonify({'error': 'Failed to insert building data', 'details': response.text}), 400
    
    return jsonify({'message': 'Scenario and buildings inserted successfully'}), 200

@app.route('/get_buildings', methods=['GET'])
def get_buildings():
    project_name = request.args.get('projectName')
    scenario_name = request.args.get('scenarioName')

    if not project_name or not scenario_name:
        return jsonify({'error': 'projectName and scenarioName are required'}), 400

    # Construct WFS GetFeature request
    wfs_url = f"{GEOSERVER_URL}/wfs"
    params = {
        'service': 'WFS',
        'version': '1.0.0',
        'request': 'GetFeature',
        'typeName': 'comet_geo:buildings_scenario',
        'outputFormat': 'application/json',
        'CQL_FILTER': f"scenario_name='{scenario_name}' AND project_name='{project_name}'"
    }

    response = requests.get(wfs_url, params=params, auth=('admin', 'geoserver'))

    if response.status_code != 200:
        return jsonify({'error': 'Failed to retrieve buildings data', 'details': response.text}), 400

    return response.json(), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
