Enable Master Node Scheduling in an OCP Cluster

To enable scheduling on Master nodes in an OpenShift Container Platform (OCP) cluster, follow these steps:

1. **Mark Master Nodes as Schedulable**:  
    Use the `oc patch` command to mark Master nodes as schedulable.

    ```sh
    oc patch schedulers.config.openshift.io cluster --type merge --patch '{"spec": {"mastersSchedulable": true}}'
    ```

2. **Verify Node Status**:  
    Use the following command to verify if the Master nodes have been marked as schedulable.

    ```
    oc get node
    NAME                         STATUS   ROLES                         AGE    VERSION
    master01.yawei.example.com   Ready    control-plane,master,worker   183d   v1.29.10+67d3387
    master02.yawei.example.com   Ready    control-plane,master,worker   183d   v1.29.10+67d3387
    master03.yawei.example.com   Ready    control-plane,master,worker   183d   v1.29.10+67d3387
    worker01.yawei.example.com   Ready    worker                        183d   v1.29.10+67d3387
    worker02.yawei.example.com   Ready    worker                        183d   v1.29.10+67d3387
    worker03.yawei.example.com   Ready    worker                        183d   v1.29.10+67d3387
    ```

    The output should show that the Master nodes have the `worker` role label.

3. **Check Scheduler Configuration**:  
        Ensure that the scheduler configuration allows workloads to be scheduled on Master nodes.

    ```sh
    oc get pods --all-namespaces -o wide | grep master
    ```

