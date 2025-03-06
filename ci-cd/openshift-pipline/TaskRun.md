# Configuring a TaskRun
A TaskRun definition supports the following fields:
- Required:
  - apiVersion - Specifies the API version, for example tekton.dev/v1beta1.
  - kind - Identifies this resource object as a TaskRun object.
  - metadata - Specifies the metadata that uniquely identifies the TaskRun, such as a name.
  - spec - Specifies the configuration for the TaskRun.
  - taskRef or taskSpec - Specifies the Tasks that the TaskRun will execute.
- Optional:
  - serviceAccountName - Specifies a ServiceAccount object that provides custom credentials for executing the TaskRun.
  - params - Specifies the desired execution parameters for the Task.
  - timeout - Specifies the timeout before the TaskRun fails.
  - podTemplate - Specifies a Pod template to use as the starting point for configuring the Pods for the Task.
  - workspaces - Specifies the physical volumes to use for the Workspaces declared by a Task.
  - debug- Specifies any breakpoints and debugging configuration for the Task execution.
  - stepOverrides - Specifies configuration to use to override the Task’s Steps.
  - sidecarOverrides - Specifies configuration to use to override the Task’s Sidecars.
