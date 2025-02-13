#### How to view the maximum number of connections to the current database
##### Quay deployed as a standalone virtual machine
- Get the username and password from the deployment command
  ```
podman run -d --rm --name postgresql-quay \
  -e POSTGRESQL_USER=quayuser \
  -e POSTGRESQL_PASSWORD=quaypass \
  -e POSTGRESQL_DATABASE=quay \
  -e POSTGRESQL_ADMIN_PASSWORD=adminpass \
  -p 5432:5432 \
  -v $QUAY/postgres-quay:/var/lib/pgsql/data:Z \
  registry.redhat.io/rhel8/postgresql-13

podman ps
243e28889c1f  registry.redhat.io/rhel8/postgresql-13:1-109  run-postgresql        7 days ago    Up 7 days   0.0.0.0:5432->5432/tcp  postgresql_database
  ```
- Enter the container
  ```
podman exec -it 243e28889c1f /bin/sh
sh-4.4$ psql -d quaydb -U quayuser
psql (13.7)
Type "help" for help.
quaydb=> SHOW max_connections;
 max_connections
-----------------
 100
(1 row)

  ```
- The default number of database connections is only 100, which may not meet the user's usage requirements. You need to modify the number of database connections.
  
- add the POSTGRESQL_MAX_CONNECTIONS parameter when starting podman.
  ```
podman run -d --name postgresql_database     -v /var/lib/pgsql/data:/var/lib/pgsql/data:Z      -e POSTGRESQL_USER=quayuser -e POSTGRESQL_PASSWORD=quaypass   -e POSTGRESQL_MAX_CONNECTIONS='2000'  -e POSTGRESQL_DATABASE=quaydb -p 5432:5432     registry.redhat.io/rhel8/postgresql-13:1-109

  ```
##### Quay Operator Deployment
- Switch to the project that deploys quay-registry
  ```
  oc project quay-enterprise
  ```
- View database authentication information
  ```
  $ oc get secret | grep postgres-config-secret
  example-registry-postgres-config-secret-762h2khm8c           Opaque                                4      24d
  ```
- Export the current authentication information and view the database name and username
  ```
  $ oc extract secret/example-registry-postgres-config-secret-762h2khm8c
   database-name
   database-password
   database-root-password
   database-username
  ```
- Enter the database pod and use the authentication information to switch the database.
  ```
  oc rsh example-registry-quay-database-6646f57dff-9xgsd 
  sh-4.4$ psql -d example-registry-quay-database -U example-registry-quay-database
  psql (13.13)
  Type "help" for help.
  example-registry-quay-database=> SHOW max_connections;
   max_connections
  -----------------
   2000
  (1 row)
  ```

