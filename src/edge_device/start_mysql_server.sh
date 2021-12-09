docker run --name mysql57 -d --restart unless-stopped -p 3306:3306 ibex/debian-mysql-server-5.7
echo "Run Command to enter mysql database: docker exec -it mysql57 "mysql" -u root"
echo "CREATE USER 'root'@'%' IDENTIFIED by 'cloud123';"
echo "GRANT ALL PRIVILEGES on *.* TO 'root'@'%' WITH GRANT OPTION;"
echo "CREATE DATABASE lambda;"
echo "USE lambda;"
echo "CREATE TABLE IF NOT EXISTS temps_found ( temp_id INT AUTO_INCREMENT, temp FLOAT NOT NULL, sensor_type INT NOT NULL, time_stamp TIMESTAMP, PRIMARY KEY (temp_id) ) ENGINE=INNODB;"
