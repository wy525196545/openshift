Because the quay user password is hash-encrypted and cannot be modified directly in the database, the general idea is to create a new test user with a known password, and then use the known hash-encrypted password to replace it with that of the quayadmin user. Password, so that the password of quayadmin is the same as the password of the test user, so that you can log in to the quayadmin super user, and then delete the test user.

- Create a new test user testpassword on the quay web page
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
  example-registry-quay-database=> select id,username,password_hash from public.user;
  id |   username   |                        password_hash
  ----+--------------+--------------------------------------------------------------
  3 | testtag      |
  4 | wytest       |
  5 | testuser     | $2b$12$1PVtLe4Fe51pDefCNnW2BO9Vdf4oDEGXKOKnccUFxNNPbQDWeHP8S
  6 | testpassword | $2b$12$Y9cmYnKbxLqbBH5oAGe6g.UOQ0901re48bNVrUgO1uucI7oNdVe7q
  1 | quayadmin    | $2b$12$Y9cmYnKbxLqbBH5oAGe6g.UOQ0901re48bNVrUgO1uucI7oNdVe7q
  (5 rows) 
  ```
  You can see that the new testpassword is the test user, copy his password_hash, and then update the quayadmin password. Then you can log in to quayadmin with the test user's password.
  ```
  example-registry-quay-database=> UPDATE public.user SET password_hash = '$2b$12$Y9cmYnKbxLqbBH5oAGe6g.UOQ0901re48bNVrUgO1uucI7oNdVe7q' where username = 'quayadmin';
  UPDATE 1
  ```
  In this way, you can log in to quayadmin with the password of the test user testpassword, and then delete the test user
  ```
  DELETE FROM public.user  WHERE username = 'testpassword';
  ```
- (tip)Please keep your user password carefully. Please do not directly operate the database unless it is an emergency cleanup.

- Query all tables in the database
```
SELECT table_schema, table_name
FROM information_schema.tables
WHERE table_type = 'BASE TABLE'
ORDER BY table_schema, table_name;
```
- Query table structure
```
\d <tablename>
```

Update quay's configuration file
```
oc set data secret/config-bundle-secret --from-file=config.yaml=config.yaml
```
