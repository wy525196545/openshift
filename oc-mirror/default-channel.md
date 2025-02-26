#### oc-mirror error
运行oc-mirror命令报错
```
$ oc-mirror --config imageset-config-yaml file:// 
...
error generating diff: the current default channel "stable-6.0" for package "cluster-logging" could not be determined...
...
```
检查imageset-config.yaml
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
根据报错提示下载的operator版本不是当前默认的channel，需要在imageset-config.yaml里加入defaultChannel信息来下载特定的channel版本。
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