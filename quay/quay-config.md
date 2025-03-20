##### Export the current configuration file of quay

This command extracts the `config-bundle-secret` secret from OpenShift and saves its contents, including the `config.yaml` file, to the current directory.

```
oc extract secret/config-bundle-secret
config.yaml
```

##### Update quay's configuration file

This command updates the `config-bundle-secret` secret in OpenShift with the new `config.yaml` file.
```
oc set data secret/config-bundle-secret --from-file=config.yaml=config.yaml
```
