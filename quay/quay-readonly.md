##  Enabling read-only mode for Red Hat Quay on OpenShift Container Platform 
##### Enabling read-only mode for your Red Hat Quay on OpenShift Container Platform deployment allows you to manage the registry’s operations. Administrators can enable read-only mode to restrict write access to the registry, which helps ensure data integrity, mitigate risks during maintenance windows, and provide a safeguard against unintended modifications to registry data. It also helps to ensure that your Red Hat Quay registry remains online and available to serve images to users.

##### When backing up and restoring, you are required to scale down your Red Hat Quay on OpenShift Container Platform deployment. This results in service unavailability during the backup period which, in some cases, might be unacceptable. Enabling read-only mode ensures service availability during the backup and restore procedure for Red Hat Quay on OpenShift Container Platform deployments.

### Creating service keys for Red Hat Quay on OpenShift Container Platform 
- Red Hat Quay uses service keys to communicate with various components. These keys are used to sign completed requests, such as requesting to scan images, login, storage access, and so on.
- 1.Enter the following command to obtain a list of Red Hat Quay pods:
    ```
    $ oc get pods -n <namespace>
    ```
    Example output
    ```
    example-registry-clair-app-6ff967b6fb-nhtg7        1/1     Running     2 (28m ago)   28m
    example-registry-clair-postgres-5988c9988d-th7lx   1/1     Running     0             28m
    example-registry-quay-app-76d74d4c65-bjhtp         1/1     Running     2 (28m ago)   28m
    example-registry-quay-app-upgrade-kj8nr            0/1     Completed   2             29m
    example-registry-quay-database-f87796775-bdmkf     1/1     Running     0             28m
    example-registry-quay-mirror-76c766598f-25w66      1/1     Running     0             28m
    example-registry-quay-mirror-76c766598f-87sdl      1/1     Running     0             28m
    example-registry-quay-redis-86648bb7f8-zphlg       1/1     Running     0             28m
    ```
- 2.Open a remote shell session to the Quay container by entering the following command:
    ```
    oc rsh example-registry-quay-app-76c8f55467-52wjz
    ```
- 3.Enter the following command to create the necessary service keys:
    ```
    sh-4.4$ python3 tools/generatekeypair.py quay-readonly
    ```
    Example output
    ```
    Writing public key to quay-readonly.jwk
    Writing key ID to quay-readonly.kid
    Writing private key to quay-readonly.pem
    ```
- 4.Copy the generated files from the pod to your local machine using the following command:
    ```
    oc cp <namespace>/<pod-name>:/quay-registry/quay-readonly.* /local/destination/path/
    ```
    Replace `<namespace>` with your namespace, `<pod-name>` with the name of your Quay pod (e.g., `example-registry-quay-app-76c8f55467-52wjz`), and `/local/destination/path/` with the desired local directory path.
### Adding keys to the PostgreSQL database 
* Use the following procedure to add your service keys to the PostgreSQL database.
- 1.Enter the following command to enter your Red Hat Quay database environment:
    ```
    oc rsh example-registry-quay-database-76c8f55467-52wjz psql -U <database_username> -d <database_name>
    ```
    **How to obtain the database password**

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
- 2.Display the approval types and associated notes of the servicekeyapproval by entering the following command:
    ```
    sh-4.4$  psql -d example-registry-quay-database -U example-registry-quay-database
    psql (13.20)
    Type "help" for help.

    example-registry-quay-database=>select * from servicekeyapproval;
    ```
    Example output
    ```
    id | approver_id |          approval_type           |       approved_date        | notes
    ----+-------------+----------------------------------+----------------------------+-------
    1 |             | ServiceKeyApprovalType.AUTOMATIC | 2025-04-23 08:51:47.395059 |
    2 |             | ServiceKeyApprovalType.AUTOMATIC | 2025-04-23 08:53:04.896346 |
    3 |             | ServiceKeyApprovalType.AUTOMATIC | 2025-04-23 08:53:09.226008 |
    (3 rows)
    ```
- 3.Add the service key to your Red Hat Quay database by entering the following query:（Fill in the contents of the .kid and jwk files just created）
    ```
    example-registry-quay-database=>
    INSERT INTO servicekey (name, service, metadata, kid, jwk, created_date, expiration_date) VALUES ('quay-readonly','quay','{}','vqWhNdXCbs1nWMIkpty7LuUBtDWarS9s9piCNJNCTzA','{"n":"3OW1t1zOD-C83zzjqB6oQ-dk7MvGNUqU9GC_axnXiXggShf-fxCH-bZQe6XtdygUdppWozBsvshPiWvXLOvKwkRBpB4qK2ubKYpSa-znzyOfGZjrs96miUcF7qs6tGrYtNUyvlIKodroRHDyaRi4kPMpuj8Pscyec5Y-YR-NfqsiNYoWAmZrpSoT-jtI2vrNWDTfZybxBKGN8igpFJBuQJSoF2uJVvVXbqZjZWo7ozCvWxBUMu8Vd1Q6EgJHFROCYruW_4zCmqtgojCO0aIKWauvUZLKgqiJOGfG3W4zzSCTvEvQs7dtVXdTwA1EkZhd5D13wUGMD2SZOq7NB1aBiw","e":"AQAB","kty":"RSA","kid":"vqWhNdXCbs1nWMIkpty7LuUBtDWarS9s9piCNJNCTzA"}',' 2025-04-21 05:19:11', ' 2025-05-21 05:19:11');
    ```
    Example output
    ```
    INSERT 0 1
    ```
- 4,Next, add the key approval with the following query:
    ```
    example-registry-quay-database=> INSERT INTO servicekeyapproval ("approval_type", "approved_date", "notes")  VALUES ('ServiceKeyApprovalType.SUPERUSER', '2025-04-21 05:20:11', 'backup');
    ```
    Example output
    ```
    INSERT 0 1
    ```
- 5.Set the approval_id field on the created service key row to the id field from the created service key approval. You can use the following SELECT statements to get the necessary IDs:
    ```
    example-registry-quay-database=> UPDATE servicekey SET approval_id = (SELECT id FROM servicekeyapproval WHERE approval_type = 'ServiceKeyApprovalType.SUPERUSER') WHERE name = 'quay-readonly';
    ```
    Example output
    ```
    UPDATE 1
    ```
### Configuring read-only mode Red Hat Quay on OpenShift Container Platform 
- After the service keys have been created and added to your PostgreSQL database, you must restart the Quay container on your OpenShift Container Platform deployment.
- 1.Enter the following command to read the secret name of your Red Hat Quay on OpenShift Container Platform deployment:
    ```
    oc get deployment example-registry-quay-app -oyaml | grep 'quay-config'
          value: example-registry-quay-config-secret-g2cb58h7dh
              name: example-registry-quay-config-secret-g2cb58h7dh
              name: example-registry-quay-config-tls-gf6tg8hhf2
    ```
- 2 Use the base64 command to encode the quay-readonly.kid and quay-readonly.pem files:
    ```
    # base64 -w0 quay-readonly.kid
    dnFXaE5kWENiczFuV01Ja3B0eTdMdVVCdERXYXJTOXM5cGlDTkpOQ1R6QQ==
    ```
- 3 Obtain the current configuration bundle and secret by entering the following command:
    ```
    oc get secret example-registry-quay-config-secret-g2cb58h7dh -o json | jq '.data."config.yaml"' | cut -d '"' -f2 | base64 -d -w0 > config.yaml
    ```
- 4 Edit the config.yaml file and add the following information:
    ```
    # ...
    REGISTRY_STATE: readonly
    INSTANCE_SERVICE_KEY_KID_LOCATION: 'conf/stack/quay-readonly.kid'
    INSTANCE_SERVICE_KEY_LOCATION: 'conf/stack/quay-readonly.pem'
    # ...
    ```
- 5 Save the file and base64 encode it by running the following command:
    ```
    # base64 -w0 config.yaml
    QUxMT1dfUFVMTFNfV0lUSE9VVF9TVFJJQ1RfTE9HR0lORzogZmFsc2UKQVVUSEVOVElDQVRJT05fVFlQRTogRGF0YWJhc2UKQlVJTERMT0dTX1JFRElTOgogIGhvc3Q6IGV4YW1wbGUtcmVnaXN0cnktcXVheS1yZWRpcwogIHBvcnQ6IDYzNzkKREFUQUJBU0VfU0VDUkVUX0tFWTogRWVwSFpVdWVNYm9EVUU3R3NRRkR2bElnYjJST1Z1aVJreXAxUTA0Rko1cUtlVHptOEpIOUJYSGc5MWdmVVV6OEdGNE5YeUc4RUh3d2M5bTkKREJfQ09OTkVDVElPTl9BUkdTOgogIGF1dG9yb2xsYmFjazogdHJ1ZQogIHRocmVhZGxvY2FsczogdHJ1ZQpEQl9VUkk6IHBvc3RncmVzcWw6Ly9leGFtcGxlLXJlZ2lzdHJ5LXF1YXktZGF0YWJhc2U6UWpYQjM5VjNEVGJOOE55dUlXeThVWjRqREpabGhsNS1sdTFtV0M1SkwzTUJkZ3I2Z25WNUJmZ2IxdHVrS2hTeXloTTdDQTdEcW01T1prMGJAZXhhbXBsZS1yZWdpc3RyeS1xdWF5LWRhdGFiYXNlOjU0MzIvZXhhbXBsZS1yZWdpc3RyeS1xdWF5LWRhdGFiYXNlCkRFRkFVTFRfVEFHX0VYUElSQVRJT046IDJ3CkRJU1RSSUJVVEVEX1NUT1JBR0VfQ09ORklHOgogIGRlZmF1bHQ6CiAgLSBSYWRvc0dXU3RvcmFnZQogIC0gYWNjZXNzX2tleTogbWluaW9hZG1pbgogICAgYnVja2V0X25hbWU6IHF1YXktYnVja2V0CiAgICBob3N0bmFtZTogbWluaW8tbWluaW8uYXBwcy5vY3A0LnlhbmcuY29tCiAgICBpc19zZWN1cmU6IGZhbHNlCiAgICBwb3J0OiA4MAogICAgc2VjcmV0X2tleTogbWluaW9hZG1pbgogICAgc3RvcmFnZV9wYXRoOiAvCkRJU1RSSUJVVEVEX1NUT1JBR0VfREVGQVVMVF9MT0NBVElPTlM6IFtdCkRJU1RSSUJVVEVEX1NUT1JBR0VfUFJFRkVSRU5DRToKLSBkZWZhdWx0CkVOVEVSUFJJU0VfTE9HT19VUkw6IC9zdGF0aWMvaW1nL1JIX0xvZ29fUXVheV9CbGFja19VWC1ob3Jpem9udGFsLnN2ZwpFWFRFUk5BTF9UTFNfVEVSTUlOQVRJT046IHRydWUKRkVBVFVSRV9CVUlMRF9TVVBQT1JUOiBmYWxzZQpGRUFUVVJFX0RJUkVDVF9MT0dJTjogdHJ1ZQpGRUFUVVJFX01BSUxJTkc6IGZhbHNlCkZFQVRVUkVfUkVQT19NSVJST1I6IHRydWUKRkVBVFVSRV9TRUNVUklUWV9OT1RJRklDQVRJT05TOiB0cnVlCkZFQVRVUkVfU0VDVVJJVFlfU0NBTk5FUjogdHJ1ZQpQUkVGRVJSRURfVVJMX1NDSEVNRTogaHR0cHMKUkVHSVNUUllfVElUTEU6IFJlZCBIYXQgUXVheQpSRUdJU1RSWV9USVRMRV9TSE9SVDogUmVkIEhhdCBRdWF5ClJFUE9fTUlSUk9SX0lOVEVSVkFMOiAzMApSRVBPX01JUlJPUl9UTFNfVkVSSUZZOiB0cnVlClNFQ1JFVF9LRVk6IHoyM0g1NXRrZ0pqakM3ckFiRUZwWEhjVUhWWEZKZllpaEtCZkFmOVR5djltTHdGZjJzUVVUbzdCZmp0ZjlXcDlkV3AyNlJpdVYwY2tKQ3pnClNFQ1VSSVRZX1NDQU5ORVJfSU5ERVhJTkdfSU5URVJWQUw6IDMwClNFQ1VSSVRZX1NDQU5ORVJfVjRfRU5EUE9JTlQ6IGh0dHA6Ly9leGFtcGxlLXJlZ2lzdHJ5LWNsYWlyLWFwcC5xdWF5LWVudGVycHJpc2Uuc3ZjLmNsdXN0ZXIubG9jYWwKU0VDVVJJVFlfU0NBTk5FUl9WNF9OQU1FU1BBQ0VfV0hJVEVMSVNUOgotIGFkbWluClNFQ1VSSVRZX1NDQU5ORVJfVjRfUFNLOiBNamxtZDNFeWNFeHpSRk40VG5Od09UTjVZekp5ZUVKRkxYZEhabXR0WW5RPQpTRVJWRVJfSE9TVE5BTUU6IGV4YW1wbGUtcmVnaXN0cnktcXVheS1xdWF5LWVudGVycHJpc2UuYXBwcy5vY3A0LnlhbmcuY29tClNFVFVQX0NPTVBMRVRFOiB0cnVlClNVUEVSX1VTRVJTOgotIHF1YXlhZG1pbgpUQUdfRVhQSVJBVElPTl9PUFRJT05TOgotIDJ3ClRFQU1fUkVTWU5DX1NUQUxFX1RJTUU6IDYwbQpURVNUSU5HOiBmYWxzZQpVU0VSX0VWRU5UU19SRURJUzoKICBob3N0OiBleGFtcGxlLXJlZ2lzdHJ5LXF1YXktcmVkaXMKICBwb3J0OiA2Mzc5ClJFR0lTVFJZX1NUQVRFOiByZWFkb25seQpJTlNUQU5DRV9TRVJWSUNFX0tFWV9LSURfTE9DQVRJT046ICdjb25mL3N0YWNrL3F1YXktcmVhZG9ubHkua2lkJwpJTlNUQU5DRV9TRVJWSUNFX0tFWV9MT0NBVElPTjogJ2NvbmYvc3RhY2svcXVheS1yZWFkb25seS5wZW0nCg==
    ```
- 6 Scale down the Red Hat Quay Operator pods to 0. This ensures that the Operator does not reconcile the secret after editing it.
    ```
    $ oc scale --replicas=0 deployment quay-operator.v3.14.0 -n openshift-operators
    ```
- 7 Edit the secret to include the new content:
    ```
    $ oc edit secret example-registry-quay-config-secret-g2cb58h7dh -n quay-namespace
    "quay-readonly.kid": "ZjUyNDFm..."
    "quay-readonly.pem": "LS0tLS1CRUdJTiBSU0E..."
     "config.yaml": "QUNUSU9OX0xPR19..."
    ```
### Verifying that Red Hat Quay is in read-only mode

After configuring and restarting your Red Hat Quay deployment, verify that the registry is operating in read-only mode:

1. **Check the Quay UI:**  
    - Log in to the Red Hat Quay web console.
    - Attempt to perform a write operation, such as pushing a new image or creating a new repository.  
    - The UI should display a message indicating that the registry is in read-only mode and write operations are not permitted.



2. **Test with CLI:**  
    - Attempt to push an image using the  or Podman CLI:
      ```
      podman login example-registry-quay-quay-enterprise.apps.ocp4.yang.com --tls-verify=false
      podman tag  7af3297a3fb4 example-registry-quay-quay-enterprise.apps.ocp4.yang.com/quayadmin/test:v1
      podman push example-registry-quay-quay-enterprise.apps.ocp4.yang.com/quayadmin/test:v1 --tls-verify=false
      Getting image source signatures
      Copying blob bd9ddc54bea9 skipped: already exists
      Copying blob fe707316409f skipped: already exists
      Copying config 7af3297a3f done   |
      Writing manifest to image destination
      Error: writing manifest: uploading manifest v1 to example-registry-quay-quay-enterprise.apps.ocp4.yang.com/quayadmin/test: denied: System is currently read-only. Pulls will succeed but all write operations are currently suspended.
        ```
    - The push should fail with an error indicating that the registry is read-only.

    If  checks confirm that write operations are blocked and the registry is serving images, Red Hat Quay is successfully running in read-only mode.


###  Scaling up the Red Hat Quay on OpenShift Container Platform from a read-only deployment 
- 1.Edit the config.yaml file and remove the following information:
    ```
    # ...
    REGISTRY_STATE: readonly
    INSTANCE_SERVICE_KEY_KID_LOCATION: 'conf/stack/quay-readonly.kid'
    INSTANCE_SERVICE_KEY_LOCATION: 'conf/stack/quay-readonly.pem'
    # ...
    ```
- 2.Scale the Red Hat Quay Operator back up by entering the following command:
    ```
    oc scale --replicas=1 deployment quay-operator -n openshift-operators
    ```
