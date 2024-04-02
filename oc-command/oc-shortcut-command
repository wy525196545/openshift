- View openshift certificates updated within one year
```
$ oc get secret -A -o json | jq -r '.items[] | select(.metadata.annotations."auth.openshift.io/certificate-not-after"!=null) | select(.metadata.name|test("-[0-9]+$")|not) | "\(.metadata.namespace) \(.metadata.name) \(.metadata.annotations."auth.openshift.io/certificate-not-before") \(.metadata.annotations."auth.openshift.io/certificate-not-after")"' | column -t
```
