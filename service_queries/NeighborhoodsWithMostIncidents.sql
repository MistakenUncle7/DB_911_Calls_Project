SELECT 
    locations.neighborhood, 
    COUNT(incidents.recordld) AS total_incidents 
FROM 
    locations 
JOIN 
    incidents ON locations.locationRecordId = incidents.locationRecordId 
GROUP BY 
    locations.neighborhood 
ORDER BY 
    total_incidents DESC;