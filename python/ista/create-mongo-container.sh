docker run -e MONGO_INITDB_ROOT_USERNAME=vitalii -e MONGO_INITDB_ROOT_PASSWORD=vitalii -d --name mongo -p 27017:27017 -p 28017:28017 -v /home/technik/projects/ista/data/db-mongo:/data/db mongo


