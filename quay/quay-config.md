##### Export the current configuration file of quay
```
oc extract secret/config-bundle-secret
config.yaml
```
##### Update quay's configuration file
```
oc set data secret/config-bundle-secret --from-file=config.yaml=config.yaml
```
