SELECT 
    incidents.district, 
    COUNT(incidents.recordld) AS totalIncidents, 
    MAX(incidents.description) AS mostCommonIncident 
FROM 
    incidents 
GROUP BY 
    incidents.district 
ORDER BY 
    totalIncidents DESC;