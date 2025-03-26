# How to Query Metrics on an OCP Cluster Using PromQL

To query metrics on an OpenShift Container Platform (OCP) cluster using PromQL, follow these steps:

1. **Access the OpenShift Web Console**:
    Open your browser and log in to the OpenShift Web Console.

2. **Navigate to the Monitoring Page**:
    In the left-hand navigation menu, select `Monitoring` -> `Query`.

3. **Write a PromQL Query**:
    Enter your PromQL query in the query input box. For example, to query CPU usage:
    ```promql
    sum(rate(container_cpu_usage_seconds_total{namespace="default"}[5m]))
    ```

4. **Execute the Query**:
    Click the `Execute` button to run the query and view the results.

5. **View the Chart**:
    The query results will be displayed as a chart. You can adjust the time range and refresh rate as needed.

6. **Save the Query**:
    If you frequently use a specific query, save it as a custom query for quick access later.

By following these steps, you can query and monitor metrics on an OCP cluster using PromQL.

## Querying Metrics Using the API

In addition to using PromQL in the OpenShift Web Console, you can query metrics via the API. Here are the steps to do so:

### Obtain a Valid API Token

To obtain a valid API token, follow these steps:

1. **Retrieve the Token Using the `oc` Command-Line Tool**:
    - Open a terminal and log in to the OpenShift cluster:
    ```sh
    export TOKEN=$(oc create token prometheus-k8s -n openshift-monitoring)
    export URL=$(oc get route prometheus-k8s -o jsonpath='https://{.spec.host}' -n openshift-monitoring)
    ```

2. **Construct the Query**:
    - Define the PromQL query:
    ```sh
    export QUERY="sum(rate(container_cpu_usage_seconds_total{namespace=\"default\"}[5m]))"
    ```

3. **Send the API Request**:
    - Use `curl` or another HTTP client to send the request, including the API token for authentication. For example:
    ```sh
    curl -s -k -XPOST "${URL}/api/v1/query" \
     -H "Authorization: Bearer ${TOKEN}" \
     --data-urlencode "query=${QUERY}" | jq
    ```

The API response will contain the query results in JSON format.

By following these steps, you can query and monitor metrics on an OCP cluster using the API.