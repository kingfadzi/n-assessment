SELECT
    a.app_name,
    s.agent_version AS agent_id,
    COUNT(DISTINCT s.id) AS total_servers,
    COUNT(DISTINCT CASE WHEN s.reachable = true THEN s.id END) AS reachable_servers,
    COUNT(DISTINCT CASE WHEN s.reachable = false THEN s.id END) AS unreachable_servers,
    ROUND((COUNT(DISTINCT CASE WHEN s.reachable = true THEN s.id END) * 100.0 / COUNT(DISTINCT s.id)), 2) AS utilization_percentage
FROM
    servers s
JOIN server_type_instance sti ON s.id = sti.mapped_server_id
JOIN server_type st ON sti.server_type = st.id
JOIN applications a ON st.app_id = a.app_id
GROUP BY
    a.app_name, s.agent_version
ORDER BY
    a.app_name, s.agent_version;

---

SELECT
    a.app_name,
    COUNT(DISTINCT s.id) AS total_servers,
    COUNT(DISTINCT CASE WHEN s.reachable = true THEN s.id END) AS reachable_servers,
    COUNT(DISTINCT CASE WHEN s.reachable = false THEN s.id END) AS unreachable_servers,
    ROUND((COUNT(DISTINCT CASE WHEN s.reachable = true THEN s.id END) * 100.0 / total.total_count), 2) AS reachability_proportion_of_total,
    ROUND((COUNT(DISTINCT CASE WHEN s.reachable = false THEN s.id END) * 100.0 / total.total_count), 2) AS unreachability_proportion_of_total
FROM
    servers s
JOIN server_type_instance sti ON s.id = sti.mapped_server_id
JOIN server_type st ON sti.server_type = st.id
JOIN applications a ON st.app_id = a.app_id
CROSS JOIN (SELECT COUNT(DISTINCT id) AS total_count FROM servers) total
WHERE
    a.app_name != 'aws.app'
GROUP BY
    a.app_name, total.total_count
ORDER BY
    a.app_name;
