## Tekton Pipelines
Tekton Pipelines is a Kubernetes extension that installs and runs on your Kubernetes cluster. It defines a set of Kubernetes Custom Resources that act as building blocks from which you can assemble CI/CD pipelines. Once installed, Tekton Pipelines becomes available via the Kubernetes CLI (kubectl) and via API calls, just like pods and other resources. Tekton is open-source and part of the CD Foundation, a Linux Foundation project.


### Tekton Pipelines entities
<table>
  <tr style="background-color: #f2f2f2;">
    <th align="left">Entity</th>
    <th align="left">Description</th>
  </tr>
  <tr style="background-color: #ffffff;">
    <td><strong>Task</strong></td>
    <td>Defines a series of steps which launch specific build or delivery tools that ingest specific inputs and produce specific outputs.</td>
  </tr>
  <tr style="background-color: #f2f2f2;">
    <td><strong>TaskRun</strong></td>
    <td>Instantiates a Task for execution with specific inputs, outputs, and execution parameters. Can be invoked on its own or as part of a Pipeline.</td>
  </tr>
  <tr style="background-color: #ffffff;">
    <td><strong>Pipeline</strong></td>
    <td>Defines a series of Tasks that accomplish a specific build or delivery goal. Can be triggered by an event or invoked from a PipelineRun.</td>
  </tr>
  <tr style="background-color: #f2f2f2;">
    <td><strong>PipelineRun</strong></td>
    <td>Instantiates a Pipeline for execution with specific inputs, outputs, and execution parameters.</td>
  </tr>
  <tr style="background-color: #ffffff;">
    <td><strong>PipelineResource (Deprecated)</strong></td>
    <td>Defines locations for inputs ingested and outputs produced by the steps in Tasks.</td>
  </tr>
  <tr style="background-color: #f2f2f2;">
    <td><strong>Run (alpha)</strong></td>
    <td>Instantiates a Custom Task for execution when specific inputs.</td>
  </tr>
</table>



