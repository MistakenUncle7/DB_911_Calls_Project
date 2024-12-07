SELECT 
    incidents.recordld, 
    incidents.district, 
    incidents.description, 
    policeStations.policePost 
FROM 
    incidents
JOIN 
    locations ON incidents.locationRecordId = locations.locationRecordId
JOIN 
    policeStations ON locations.policeStationId = policeStations.policeStationId;