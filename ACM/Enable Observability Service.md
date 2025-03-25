### Enabling the Observability service 
When you enable the Observability service on your hub cluster, the multicluster-observability-operator watches for new managed clusters and automatically deploys metric and alert collection services to the managed clusters. You can use metrics and configure Grafana dashboards to make cluster resource information visible, help you save cost, and prevent service disruptions.

#### Enabling Observability from the command line interface 

Notes: 
- When Observability is enabled or disabled on OpenShift Container Platform managed clusters that are managed by Red Hat Advanced Cluster Management, the observability endpoint operator updates the cluster-monitoring-config config map by adding additional alertmanager configuration that automatically restarts the local Prometheus.
- The Observability endpoint operator updates the cluster-monitoring-config config map by adding additional alertmanager configurations that automatically restart the local Prometheus. When you insert the alertmanager configuration in the OpenShift Container Platform managed cluster, the configuration removes the settings that relate to the retention field of the Prometheus metrics.

#### Complete the following steps to enable the Observability service:
- Log in to your Red Hat Advanced Cluster Management hub cluster.
- Create a namespace for the Observability service with the following command:
    ```
    oc create namespace open-cluster-management-observability
    ```
- Generate your pull-secret. If Red Hat Advanced Cluster Management is installed in the open-cluster-management namespace, run the following command:
  ```
  DOCKER_CONFIG_JSON=`oc extract secret/multiclusterhub-operator-pull-secret -n  open-cluster-management --to=-`
  ```
    - If the multiclusterhub-operator-pull-secret is not defined in the namespace, copy the pull-secret from the openshift-config namespace into the open-cluster-management-observability namespace by running the following command:
        ```
        DOCKER_CONFIG_JSON=`oc extract secret/pull-secret -n openshift-config --to=-`
        ```
    - Create the pull-secret in the open-cluster-management-observability namespace by running the following command:
        ```
        oc create secret generic multiclusterhub-operator-pull-secret \
        -n open-cluster-management-observability \
        --from-literal=.dockerconfigjson="$DOCKER_CONFIG_JSON" \
        --type=kubernetes.io/dockerconfigjson
        ```
        Important: If you modify the global pull secret for your cluster by using the OpenShift Container Platform documentation, be sure to also update the global pull secret in the Observability namespace. See [Updating the global pull secret](https://docs.redhat.com/en/documentation/openshift_container_platform/4.16/html/images/managing-images#images-update-global-pull-secret_using-image-pull-secrets) for more details.

- Create a secret for your object storage for your cloud provider. Your secret must contain the credentials to your storage solution. For example, run the following command:
    ```
    oc create -f thanos-object-storage.yaml -n open-cluster-management-observability
    ```
View the following examples of secrets for the supported object stores 
```
apiVersion: v1
kind: Secret
metadata:
  name: thanos-object-storage
  namespace: open-cluster-management-observability
type: Opaque
stringData:
  thanos.yaml: |
    type: s3
    config:
      bucket: acm-bucket
      endpoint: minio-minio.apps.ocp4.example.com
      insecure: true
      access_key: minioadmin
      secret_key: minioadmin
```
#### Creating the MultiClusterObservability custom resource 
- Create the MultiClusterObservability custom resource YAML file named multiclusterobservability_cr.yaml.
View the following default YAML file for observability:
    ```
    apiVersion: observability.open-cluster-management.io/v1beta2
    kind: MultiClusterObservability
    metadata:
    name: observability
    spec:
      observabilityAddonSpec: {}
      storageConfig:
        metricObjectStorage:
          name: thanos-object-storage
          key: thanos.yaml
    ```

- To deploy on infrastructure machine sets, you must set a label for your set by updating the nodeSelector in the MultiClusterObservability YAML. Your YAML might resemble the following content:
    ```
    nodeSelector:
      node-role.kubernetes.io/infra: ""
    ```
- Apply the Observability YAML to your cluster by running the following command:
    ```
    oc apply -f multiclusterobservability_cr.yaml
    ```
All the pods in open-cluster-management-observability namespace for Thanos, Grafana and Alertmanager are created. All the managed clusters connected to the Red Hat Advanced Cluster Management hub cluster are enabled to send metrics back to the Red Hat Advanced Cluster Management Observability service.
- Validate that the Observability service is enabled and the data is populated by launching the Grafana dashboards.
- Access the multicluster-observability-operator deployment to verify that the multicluster-observability-operator pod is being deployed by the multiclusterhub-operator deployment. Run the following command:
    ```
    oc get deploy multicluster-observability-operator -n open-cluster-management --show-labels
    NAME                                  READY   UP-TO-DATE   AVAILABLE   AGE     LABELS
    multicluster-observability-operator   1/1     1            1           5h13m   installer.name=multiclusterhub,installer.namespace=open-cluster-management
    ```
- Optional: If you want to exclude specific managed clusters from collecting the Observability data, add the following cluster label to your clusters: observability: disabled.

#### The Observability service is enabled. After you enable the Observability service, the following functions are initiated:

- All the alert managers from the managed clusters are forwarded to the Red Hat Advanced Cluster Management hub cluster.
- All the managed clusters that are connected to the Red Hat Advanced Cluster Management hub cluster are enabled to send alerts back to the Red Hat Advanced Cluster Management Observability service. You can configure the Red Hat Advanced Cluster Management Alertmanager to take care of deduplicating, grouping, and routing the alerts to the correct receiver integration such as email, PagerDuty, or OpsGenie. You can also handle silencing and inhibition of the alerts.

Note: Alert forwarding to the Red Hat Advanced Cluster Management hub cluster feature is only supported by managed clusters on a supported OpenShift Container Platform version. After you install Red Hat Advanced Cluster Management with Observability enabled, alerts are automatically forwarded to the hub cluster. See [Forwarding alerts](https://docs.redhat.com/en/documentation/red_hat_advanced_cluster_management_for_kubernetes/2.12/html/observability/observing-environments-intro#forward-alerts) to learn more.