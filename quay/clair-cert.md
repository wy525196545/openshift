
#### When the user manages the clair scanner, the clair-app pod log may show "tls: failed to verify certificate: x509: certificate signed by unknown authority"

- Users are required to add the CA certificate to the /var/run/certs/ directory
```
$ openssl s_client -connect QUAY_HOSTNAME:443 -showcerts 2>/dev/null </dev/null | sed -ne '/-BEGIN CERTIFICATE-/,/-END CERTIFICATE-/p' > quay-wildcard-certificate.crt
$ oc create secret generic quay-wildcard-cert-secret --from-file=ca.crt=quay-wildcard-certificate.crt -n quay-namespace
$ oc edit deployment clair-deployment-name -n quay-namespace
...
spec:
  template:
    spec:
      containers:
      - ...
        volumeMounts:
        - name: quay-cert
          path: /var/run/certs/ca.crt
          subPath: ca.crt
       ...
       volumes:
       - name: quay-cert
         secret:
           secretName: quay-wildcard-cert-secret
```
