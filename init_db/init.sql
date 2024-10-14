CREATE EXTENSION IF NOT EXISTS postgis;

-- Table: scenario_project
CREATE TABLE scenario_project (
    scenario_name VARCHAR(100),
    project_name VARCHAR(100),
    scenario_center GEOMETRY(Point, 4326),
    scenario_boundary GEOMETRY(Polygon, 4326),
    PRIMARY KEY (scenario_name, project_name)
);

-- Table: buildings
CREATE TABLE buildings (
    building_id SERIAL PRIMARY KEY,
    B_geometry GEOMETRY(MultiPolygon, 4326),
    ces_senz BIGINT
);

-- Table: BUILDING_GEOMETRY_SCENARIO
CREATE TABLE BUILDING_GEOMETRY_SCENARIO (
    BUILDINGS_building_id INTEGER REFERENCES buildings(building_id),
    SCENARIO_LIST_scenario_name VARCHAR(100),
    SCENARIO_LIST_project_name VARCHAR(100),
    num_floors INTEGER,
    height FLOAT,
    net_leased_area FLOAT,
    gross_floor_area FLOAT,
    PRIMARY KEY (BUILDINGS_building_id, SCENARIO_LIST_scenario_name, SCENARIO_LIST_project_name),
    FOREIGN KEY (SCENARIO_LIST_scenario_name, SCENARIO_LIST_project_name) REFERENCES scenario_project(scenario_name, project_name)
);

-- Table: BUILDING_DEMOGRAPHIC_SCENARIO
CREATE TABLE BUILDING_DEMOGRAPHIC_SCENARIO (
    building_id INTEGER REFERENCES buildings(building_id),
    scenario_name VARCHAR(100),
    project_name VARCHAR(100),
    sez_cens VARCHAR(100),
    year_of_construction INTEGER,
    PRIMARY KEY (building_id, scenario_name, project_name),
    FOREIGN KEY (scenario_name, project_name) REFERENCES scenario_project(scenario_name, project_name)
);

-- Table: BUILDING_ENERGY_SCENARIO
CREATE TABLE BUILDING_ENERGY_SCENARIO (
    building_id INTEGER REFERENCES buildings(building_id),
    scenario_name VARCHAR(100),
    project_name VARCHAR(100),
    construction_type VARCHAR(100),
    hvac_type VARCHAR(100),
    tabula_type VARCHAR(100),
    PRIMARY KEY (building_id, scenario_name, project_name),
    FOREIGN KEY (scenario_name, project_name) REFERENCES scenario_project(scenario_name, project_name)
);
