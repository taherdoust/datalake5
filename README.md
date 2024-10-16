### Project Overview:

This project aims to build a fully functional system where users can interact with a PostGIS database via a GeoServer and a Flask API server. The goal is to design an urban energy consumption simulation platform where users can add and retrieve data, such as buildings, scenarios, and projects, in both spatial and non-spatial formats.

### Key Components:
1. **PostgreSQL Database (with PostGIS extension)**:
   The main database for this project is named **`comet`**, and it is extended with PostGIS to handle spatial data (geometry). It consists of five tables: `schenario_project`, `buildings`, `BUILDING_GEOMETRY_SCENARIO`, `BUILDING_DEMOGRAPHIC_SCENARIO`, and `BUILDING_ENERGY_SCENARIO`. These tables store different aspects of building and scenario data, with a key focus on handling 3D spatial data for simulation purposes. A view named **`buildings_scenario`** is created to join these tables for easy data retrieval.

   **Tables:**
   1. **schenario_project**:
      - `scenario_name`: Name of the scenario (primary key).
      - `project_name`: Name of the project (primary key).
      - `scenario_center`: Center point of the scenario (geometry type).
      - `scenario_boundary`: Boundary of the scenario (geometry type).

   2. **buildings**:
      - `building_id`: Unique ID for each building (primary key).
      - `B_geometry`: Geometry (geometry type).
      - `ces_senz`: Building's demographic section (foreign key).

   3. **BUILDING_GEOMETRY_SCENARIO**:
      - `BUILDINGS_building_id`: References `building_id` in `buildings`.
      - `SCENARIO_LIST_scenario_name`: References `scenario_name` in `schenario_project`.
      - `SCENARIO_LIST_project_name`: References `project_name` in `schenario_project`.
      - `num_floors`: Number of floors in the building.
      - `height`: Height of the building.
      - `net_leased_area`: Total area leased.
      - `gross_floor_area`: Total floor area.

   4. **BUILDING_DEMOGRAPHIC_SCENARIO**:
      - Stores demographic information such as `sez_cens`, `year_of_construction`, etc.

   5. **BUILDING_ENERGY_SCENARIO**:
      - Stores energy-related information such as `construction_type`, `hvac_type`, `tabula_type`, etc.

   **View: `buildings_scenario`**:
   This view joins the above tables to provide a comprehensive view of all relevant data about buildings for a given scenario and project.

   ### Sample Data:
   **schenario_project**:
   ```sql
   INSERT INTO schenario_project (scenario_name, project_name, scenario_center, scenario_boundary)
   VALUES ('baseline', 'nturin', 'POINT(391065 5032194)', 'POLYGON((...))');
   ```

   **buildings**:
   ```sql
   INSERT INTO buildings (building_id, B_geometry, ces_senz)
   VALUES (1, 'MULTIPOLYGON(((...)))', 11080000001);
   ```

   ### 2. **GeoServer**:
   - **Workspace**: The GeoServer workspace is named **`comet_geo`**.
   - **Datastore**: The datastore created in GeoServer is named **`building`**, which connects to the `comet` database.
   - **Published Layers**: Each of the five tables and the view `buildings_scenario` is published as a WFS layer, enabling interaction via OGC standards (WFS for data fetching and WFS-T for transactions).

   ### 3. **Flask Server (gateway.py)**:
   This Flask server acts as a bridge between the frontend and the GeoServer. It listens for incoming requests, processes them, and sends the appropriate requests to the GeoServer.

   **Endpoints**:
   1. **POST `/insert_scenario`**:
      This endpoint accepts a GeoJSON payload that includes the project name, scenario name, and the building data. The server processes the GeoJSON and prepares a WFS-T XML request to insert the scenario and building data into the respective tables in PostGIS via GeoServer.

   **Sample GeoJSON POST Request**:
   ```json
   {
     "projectName": "name of the project",
     "scenarioName": "baseline",
     "buildings": [
       {
         "geometry": {
           "type": "Polygon",
           "coordinates": [...]
         },
         "properties": {
           "height": 8,
           "num_floors": 3,
           "net_leased_area": 300
         }
       }
     ]
   }
   ```

   **What Happens in `gateway.py`**:
   - The `gateway.py` server parses the incoming GeoJSON.
   - It converts the data into WFS-T XML format.
   - Sends a WFS-T `Insert` request to GeoServer, which stores the data in PostGIS.
   - Returns a success response or an error message if the insertion fails.

   **Example WFS-T Insert Request**:
   ```xml
   <wfs:Transaction service="WFS" version="1.0.0">
     <wfs:Insert>
       <feature:buildings>
         <feature:geometry>...</feature:geometry>
         <feature:num_floors>3</feature:num_floors>
         <feature:height>8</feature:height>
       </feature:buildings>
     </wfs:Insert>
   </wfs:Transaction>
   ```

   2. **GET `/get_buildings`**:
      This endpoint allows users to fetch all buildings for a specific scenario and project. The user provides the scenario and project names as parameters, and the server prepares a WFS `GetFeature` request to GeoServer, fetches the data, and converts it to GeoJSON.

   **Sample GET Request**:
   ```json
   {
     "projectName": "name of the project",
     "scenarioName": "baseline"
   }
   ```

   **What Happens in `gateway.py`**:
   - The Flask server builds a WFS `GetFeature` request with filters based on the scenario and project name.
   - Sends the request to GeoServer.
   - Retrieves the data, converts it to GeoJSON, and returns it to the client.

   ### GeoServer Interaction with PostGIS:
   - GeoServer acts as a middle layer between the web client (via `gateway.py`) and the PostGIS database.
   - All spatial data manipulations (insertions, queries) are performed using WFS and WFS-T protocols.
   - For any `GetFeature` or `Insert` request, GeoServer translates the request into SQL operations on the PostGIS database. For example, when a `GetFeature` request is made, GeoServer generates SQL to query PostGIS, fetches the results, and formats them into GML/GeoJSON for the client.

This design ensures smooth interaction between the database, GeoServer, and the web API, handling both spatial and non-spatial data seamlessly for an urban energy consumption simulation.
