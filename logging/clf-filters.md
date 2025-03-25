#### In OpenShift Logging 6.1, the `labels` field has been removed and replaced with `filter` to add labels.

##### Reference Example
```
apiVersion: observability.openshift.io/v1
kind: ClusterLogForwarder
metadata:
  name: collector
  namespace: openshift-logging
spec:
  serviceAccount:
    name: collector
  filters:
  - name: my-label1
    openshiftLabels:
      environment: quality
      log: app
    type: openshiftLabels
  outputs:
  - name: default-lokistack
    type: lokiStack
    lokiStack:
      authentication:
        token:
          from: serviceAccount
      target:
        name: logging-loki
        namespace: openshift-logging
    tls:
      ca:
        key: service-ca.crt
        configMapName: openshift-service-ca.crt
  pipelines:
  - name: default-app
    inputRefs:
    - application
    filterRefs:
      - my-label1
    outputRefs:
    - default-lokistack
```