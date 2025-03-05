## Tekton
#### Create and run a basic Task
- To create a Task, open your favorite editor and create a file named hello-world.yaml with the following content:
```
apiVersion: tekton.dev/v1beta1
kind: Task
metadata:
  name: hello
spec:
  steps:
    - name: echo
      image: alpine
      script: |
        #!/bin/sh
        echo "Hello World"       
```
- Apply the changes to your cluster:：
```
oc apply -f hello-world.yaml
task.tekton.dev/hello created
```
- A TaskRun object instantiates and executes this Task. Create another file named hello-world-run.yaml with the following content:
```
apiVersion: tekton.dev/v1beta1
kind: TaskRun
metadata:
  name: hello-task-run
spec:
  taskRef:
    name: hello
```
- Apply the changes to your cluster to launch the Task:
```
 oc apply  -f hello-world-run.yaml
taskrun.tekton.dev/hello-task-run created
```
- Verify that everything worked correctly:
```
oc get taskruns.tekton.dev
NAME                                           SUCCEEDED   REASON      STARTTIME   COMPLETIONTIME
hello-task-run                                 True        Succeeded   5m44s       5m29s
```
- Take a look at the logs:
```
oc logs --selector=tekton.dev/taskRun=hello-task-run
Defaulted container "step-echo" out of: step-echo, prepare (init), place-scripts (init)
Hello World
```
#### Create and run a second Task
- Create a new file named goodbye-world.yaml and add the following content:
```
apiVersion: tekton.dev/v1beta1
kind: Task
metadata:
  name: goodbye
spec:
  params:
  - name: username
    type: string
  steps:
    - name: goodbye
      image: ubuntu
      script: |
        #!/bin/bash
        echo "Goodbye $(params.username)!"
```
This Task takes one parameter, username. Whenever this Task is used a value for that parameter must be passed to the Task.

- Apply the Task file: 
```
oc apply -f goodbye-world.yaml
task.tekton.dev/goodbye created
```
When a Task is part of a Pipeline, Tekton creates a TaskRun object for every task in the Pipeline.

#### Create and run a Pipeline
- Create a new file named hello-goodbye-pipeline.yaml and add the following content:
```
apiVersion: tekton.dev/v1beta1
kind: Pipeline
metadata:
  name: hello-goodbye
spec:
  params:
  - name: username
    type: string
  tasks:
    - name: hello
      taskRef:
        name: hello
    - name: goodbye
      runAfter:
        - hello
      taskRef:
        name: goodbye
      params:
      - name: username
        value: $(params.username)
```
The Pipeline defines the parameter username, which is then passed to the goodbye Task.
- Apply the Pipeline configuration to your cluster:
```
 oc apply -f hello-goodbye-pipeline.yaml
pipeline.tekton.dev/hello-goodbye created
```
- A PipelineRun, represented in the API as an object of kind PipelineRun, sets the value for the parameters and executes a Pipeline. To create PipelineRun, create a new file named hello-goodbye-pipeline-run.yaml with the following:
```
apiVersion: tekton.dev/v1beta1
kind: PipelineRun
metadata:
  name: hello-goodbye-run
spec:
  pipelineRef:
    name: hello-goodbye
  params:
  - name: username
    value: "Tekton"
```
- Start the Pipeline by applying the PipelineRun configuration to your cluster:
```
oc apply -f hello-goodbye-pipeline-run.yaml
pipelinerun.tekton.dev/hello-goodbye-run created
```
- To see the logs of the PipelineRun, use the following command:
```
tkn pipelinerun list
NAME                         STARTED          DURATION   STATUS
hello-goodbye-run            53 seconds ago   37s        Succeeded
[root@bastion tekton]# tkn pipelinerun logs hello-goodbye-run -f
[hello : echo] Hello World

[goodbye : goodbye] Goodbye Tekton!

```
#### Create a TriggerTemplate
A TriggerTemplate defines what happens when an event is detected.
- Create a new file named trigger-template.yaml and add the following:
```
apiVersion: triggers.tekton.dev/v1beta1
kind: TriggerTemplate
metadata:
  name: hello-template
spec:
  params:
  - name: username
    default: "Kubernetes"
  resourcetemplates:
  - apiVersion: tekton.dev/v1beta1
    kind: PipelineRun
    metadata:
      generateName: hello-goodbye-run-
    spec:
      pipelineRef:
        name: hello-goodbye
      params:
      - name: username
        value: $(tt.params.username)
```
The PipelineRun object that you created in the previous tutorial is now included in the template declaration. This trigger expects the username parameter to be available; if it’s not, it assigns a default value: “Kubernetes”.
- Apply the TriggerTemplate to your cluster:
```
 oc apply -f trigger-template.yaml
triggertemplate.triggers.tekton.dev/hello-template created
```
#### Create a TriggerBinding 
A TriggerBinding executes the TriggerTemplate, the same way you had to create a PipelineRun to execute the Pipeline.
- Create a file named trigger-binding.yaml with the following content:
```
apiVersion: triggers.tekton.dev/v1beta1
kind: TriggerBinding
metadata:
  name: hello-binding
spec: 
  params:
  - name: username
    value: $(body.username)
```
- This TriggerBinding gets some information and saves it in the username variable.
```
oc apply -f trigger-binding.yaml
triggerbinding.triggers.tekton.dev/hello-binding created
```
#### Create an EventListener
The EventListener object encompasses both the TriggerTemplate and the TriggerBinding.
- Create a file named event-listener.yaml and add the following:
```
apiVersion: triggers.tekton.dev/v1beta1
kind: EventListener
metadata:
  name: hello-listener
spec:
  serviceAccountName: tekton-robot
  triggers:
    - name: hello-trigger 
      bindings:
      - ref: hello-binding
      template:
        ref: hello-template
```
This declares that when an event is detected, it will run the TriggerBinding and the TriggerTemplate.
- The EventListener requires a service account to run. To create the service account for this example create a file named rbac.yaml and add the following:

```
apiVersion: v1
kind: ServiceAccount
metadata:
  name: tekton-robot
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: triggers-example-eventlistener-binding
subjects:
- kind: ServiceAccount
  name: tekton-robot
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: tekton-triggers-eventlistener-roles
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: triggers-example-eventlistener-clusterbinding
subjects:
- kind: ServiceAccount
  name: tekton-robot
  namespace: default
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: tekton-triggers-eventlistener-clusterroles
```

- Apply the file to your cluster
```
oc apply -f rbac.yaml
serviceaccount/tekton-robot created
rolebinding.rbac.authorization.k8s.io/triggers-example-eventlistener-binding created
clusterrolebinding.rbac.authorization.k8s.io/triggers-example-eventlistener-clusterbinding created
```
#### Running the Trigger
You have everything you need to run this Trigger and start listening for events.
- Create the EventListener:
```
oc apply -f event-listener.yaml
eventlistener.triggers.tekton.dev/hello-listener created
```
- To communicate outside the cluster, enable port-forwarding:
```
oc  port-forward service/el-hello-listener 8080
Forwarding from 127.0.0.1:8080 -> 8080
Forwarding from [::1]:8080 -> 8080
```
Keep this service running, don’t close the terminal.

#### Monitor the Trigger
Now that the EventListener is running, you can send an event and see what happens:
- Open a new terminal and submit a payload to the cluster:
```
curl -v \
   -H 'content-Type: application/json' \
   -d '{"username": "Tekton"}' \
   http://localhost:8080
```
You can change “Tekton” for any string you want. This value will be ultimately read by the goodbye-world Task.

The response is successful:
```
* Rebuilt URL to: http://localhost:8080/
*   Trying ::1...
* TCP_NODELAY set
* Connected to localhost (::1) port 8080 (#0)
> POST / HTTP/1.1
> Host: localhost:8080
> User-Agent: curl/7.61.1
> Accept: */*
> content-Type: application/json
> Content-Length: 22
>
* upload completely sent off: 22 out of 22 bytes
< HTTP/1.1 202 Accepted
< Content-Type: application/json
< Date: Wed, 05 Mar 2025 08:40:58 GMT
< Content-Length: 175
<
{"eventListener":"hello-listener","namespace":"pipelines-tutorial","eventListenerUID":"6916aefa-2846-462a-a21e-b049fd8bafa6","eventID":"4fdb5504-61e0-4144-a53d-f59e0f76eb1f"}
* Connection #0 to host localhost left intact
```
- This event triggers a PipelineRun, check the PipelineRuns on your cluster :
```
oc get pipelinerun
NAME                         SUCCEEDED   REASON      STARTTIME   COMPLETIONTIME
hello-goodbye-run            True        Succeeded   70m         69m
hello-goodbye-run-5kckt      True        Succeeded   57s         38s
```

Check the PipelineRun logs. The name is auto-generated adding a suffix for every run, in this case it’s hello-goodbye-run-5kckt. Use your own PiepelineRun name in the following command to see the logs:
```
tkn pipelinerun logs hello-goodbye-run-5kckt  -f
[hello : echo] Hello World

[goodbye : goodbye] Goodbye Tekton!
```













