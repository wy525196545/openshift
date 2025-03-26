#### oc-mirror error
Running the `oc-mirror` command results in the following error:
```
$ oc-mirror --config imageset-config-yaml file:// 
...
error generating diff: the current default channel "stable-6.0" for package "cluster-logging" could not be determined...
...
```
Check the `imageset-config.yaml` file:
```
apiVersion: mirror.openshift.io/v1alpha2
kind: ImageSetConfiguration
storageConfig:
  registry:
   imageURL: bastion.ocp4.example.com:5000/mirror/metadata
   skipTLS: false
mirror:
  operators:
    - catalog: registry.redhat.io/redhat/redhat-operator-index:v4.14
      packages:
        - name: cluster-logging
          channels:
            - name: stable-5.9
              minVersion: '5.9.5'
              maxVersion: '5.9.5'
```
According to the error message, the downloaded operator version is not the current default channel. You need to add the `defaultChannel` information in the `imageset-config.yaml` file to download a specific channel version.
```
apiVersion: mirror.openshift.io/v1alpha2
kind: ImageSetConfiguration
storageConfig:
  registry:
   imageURL: bastion.ocp4.example.com:5000/mirror/metadata
   skipTLS: false
mirror:
  operators:
    - catalog: registry.redhat.io/redhat/redhat-operator-index:v4.14
      packages:
        - name: cluster-logging
          defaultChannel: stable-5.9        ---------> 新增
          channels:
            - name: stable-5.9
              minVersion: '5.9.5'
              maxVersion: '5.9.5'
```