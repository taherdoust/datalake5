CREATE VIEW buildings_scenario AS
SELECT
    b.building_id,
    b.B_geometry,
    b.ces_senz,
    bg.num_floors,
    bg.height,
    bg.net_leased_area,
    bg.gross_floor_area,
    bd.sez_cens,
    bd.year_of_construction,
    be.construction_type,
    be.hvac_type,
    be.tabula_type
FROM
    buildings b
JOIN
    BUILDING_GEOMETRY_SCENARIO bg ON b.building_id = bg.BUILDINGS_building_id
JOIN
    BUILDING_DEMOGRAPHIC_SCENARIO bd ON b.building_id = bd.building_id
JOIN
    BUILDING_ENERGY_SCENARIO be ON b.building_id = be.building_id;
