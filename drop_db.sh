#!/bin/bash
docker-compose up -d
docker exec -it dev-db sh -c "psql -U dev_db_user dev_db -c \"DROP SCHEMA public CASCADE;\""
docker exec -it dev-db sh -c "psql -U dev_db_user dev_db -c \"CREATE SCHEMA public;\""
docker exec -it dev-db sh -c "psql -U dev_db_user dev_db -c \"GRANT ALL ON SCHEMA public TO db_dev_user;\""
docker exec -it dev-db sh -c "psql -U dev_db_user dev_db -c \"GRANT ALL ON SCHEMA public TO public;\""
docker-compose down