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

































