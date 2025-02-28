# 在 OCP 集群上打开 Master 节点的可调度功能

要在 OpenShift Container Platform (OCP) 集群上打开 Master 节点的可调度功能，可以按照以下步骤进行：

1. **标记 Master 节点为可调度**：
    使用 `oc patch` 命令将 Master 节点标记为可调度。

    ```sh
    oc patch schedulers.config.openshift.io cluster --type merge --patch '{"spec": {"mastersSchedulable": true}}'
    ```

2. **验证节点状态**：
    使用以下命令验证 Master 节点是否已被标记为可调度。

    ```sh
    oc get node
    NAME                         STATUS   ROLES                         AGE    VERSION
    master01.yawei.example.com   Ready    control-plane,master,worker   183d   v1.29.10+67d3387
    master02.yawei.example.com   Ready    control-plane,master,worker   183d   v1.29.10+67d3387
    master03.yawei.example.com   Ready    control-plane,master,worker   183d   v1.29.10+67d3387
    worker01.yawei.example.com   Ready    worker                        183d   v1.29.10+67d3387
    worker02.yawei.example.com   Ready    worker                        183d   v1.29.10+67d3387
    worker03.yawei.example.com   Ready    worker                        183d   v1.29.10+67d3387
    ```

    输出中应显示 Master有worker的标签

3. **检查调度器配置**：
    确保调度器配置允许在 Master 节点上调度工作负载。

    ```sh
    oc get pods --all-namespaces -o wide | grep master
    ```

