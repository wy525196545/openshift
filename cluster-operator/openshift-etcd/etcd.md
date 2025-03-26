# How to Query etcd Keys

To query the top 10 most frequent keys in the etcd database of OpenShift, you can use the `etcdctl` command-line tool. Below are some commonly used query commands:

## Query All Keys

```sh
etcdctl get "" --prefix --keys-only
```

## Query Keys with a Specific Prefix

```sh
etcdctl get /your/prefix --prefix
```

## Query the Top 10 Most Frequent Keys

To find the top 10 most frequent keys in the etcd database, use the following command:

```sh
etcdctl get / --prefix --keys-only | sed '/^$/d' | cut -d/ -f3 | sort | uniq -c | sort -rn | head
```
