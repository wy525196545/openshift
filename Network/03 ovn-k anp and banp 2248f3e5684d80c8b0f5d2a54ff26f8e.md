# 03 ovn-k anp and banp

![image.png](03%20ovn-k%20anp%20and%20banp%202248f3e5684d80c8b0f5d2a54ff26f8e/image.png)

Similar to what we did in [netpol](https://www.notion.so/2004a0a52326807e9b85e9efe5db19e8?pvs=21), we use ovsdb-client monitor to track the changes to nbdb. The ANP looks like:

```bash
apiVersion: policy.networking.k8s.io/v1alpha1
kind: AdminNetworkPolicy
metadata:
  name: allow-monitoring
spec:
  priority: 9
  subject:
    namespaces: {}
  ingress:
  - name: "allow-ingress-from-monitoring"
    action: "Allow"
    from:
    - namespaces:
        matchLabels:
          kubernetes.io/metadata.name: openshift-monitoring
```

## Analyze the events of ACL of ANP

```bash
$ ovsdb-client monitor --format=json unix:/var/run/ovn/ovnnb_db.sock ACL
```

We only captured one event, which is good.

```bash
{"data":[["502e24a7-d188-4a80-b040-6db177c4129c","insert","allow-related","to-lport",["map",[["direction","Ingress"],["gress-index","0"],["k8s.ovn.org/id","default-network-controller:AdminNetworkPolicy:allow-monitoring:Ingress:0:None"],["k8s.ovn.org/name","allow-monitoring"],["k8s.ovn.org/owner-controller","default-network-controller"],["k8s.ovn.org/owner-type","AdminNetworkPolicy"],["port-policy-protocol","None"]]],0,false,"outport == @a14012923409128626925 && ((ip4.src == $a5642994970181515866))","acl-logging","ANP:allow-monitoring:Ingress:0",["map",[]],29100,["set",[]],["set",[]],["set",[]],1,["uuid","5c0d0417-5d4d-4eb1-b2f1-5e6f4a59f32c"]]],"headings":["row","action","action","direction","external_ids","label","log","match","meter","name","options","priority","sample_est","sample_new","severity","tier","_version"]}
```

Taking closer to the acl object itself, we pay attention to the match, priority and tier.

```bash
sh-5.1# ovn-nbctl list acl 502e24a7-d188-4a80-b040-6db177c4129c
_uuid               : 502e24a7-d188-4a80-b040-6db177c4129c
action              : allow-related
direction           : to-lport
external_ids        : {direction=Ingress, gress-index="0", "k8s.ovn.org/id"="default-network-controller:AdminNetworkPolicy:allow-monitoring:Ingress:0:None", "k8s.ovn.org/name"=allow-monitoring, "k8s.ovn.org/owner-controller"=default-network-controller, "k8s.ovn.org/owner-type"=AdminNetworkPolicy, port-policy-protocol=None}
label               : 0
log                 : false
match               : "outport == @a14012923409128626925 && ((ip4.src == $a5642994970181515866))"
meter               : acl-logging
name                : "ANP:allow-monitoring:Ingress:0"
options             : {}
priority            : 29100
sample_est          : []
sample_new          : []
severity            : []
tier                : 1
```

### Match

The port_group includes the Pods that are running in this node, aka worker-0:

```bash
sh-5.1# ovn-nbctl list port_group a14012923409128626925
_uuid               : 56f0aa94-c54e-4ace-8993-7bb89b24df09
acls                : [0bd60357-80dc-4e03-a33d-f5935fefb43f]
external_ids        : {"k8s.ovn.org/id"="default-network-controller:AdminNetworkPolicy:allow-monitoring", "k8s.ovn.org/name"=allow-monitoring, "k8s.ovn.org/owner-controller"=default-network-controller, "k8s.ovn.org/owner-type"=AdminNetworkPolicy}
name                : a14012923409128626925
ports               : [098294fe-ece5-4dd3-8d89-8266d989b129, 4487b8cd-fe70-4d76-9255-41b261bd99b7, 45d36d33-9bc2-40e7-a264-456d3ecc845c, 4908cf45-aa2e-4559-a45b-a3b6e58f309e, 7fecfef0-f5d2-47d9-b16f-dab7369032fb, c265e0b8-eb92-44aa-8d93-9b62d85e0385, ebe9e9f9-f27f-42e8-a3c1-448f5e179932]
```

```bash
sh-5.1# ovn-nbctl list logical_switch_port 098294fe-ece5-4dd3-8d89-8266d989b129
_uuid               : 098294fe-ece5-4dd3-8d89-8266d989b129
addresses           : ["0a:58:0a:81:00:05 10.129.0.5"]
dhcpv4_options      : []
dhcpv6_options      : []
dynamic_addresses   : []
enabled             : []
external_ids        : {namespace=openshift-ingress-canary, pod="true"}
ha_chassis_group    : []
mirror_rules        : []
name                : openshift-ingress-canary_ingress-canary-l8vrv
options             : {iface-id-ver="2783218f-b0dc-4c08-9a63-cbd84cb17225", requested-chassis=worker-0}
parent_name         : []
port_security       : ["0a:58:0a:81:00:05 10.129.0.5"]

sh-5.1# ovn-nbctl list logical_switch_port 45d36d33-9bc2-40e7-a264-456d3ecc845c
_uuid               : 45d36d33-9bc2-40e7-a264-456d3ecc845c
addresses           : ["0a:58:0a:81:00:07 10.129.0.7"]
dhcpv4_options      : []
dhcpv6_options      : []
dynamic_addresses   : []
enabled             : []
external_ids        : {namespace=openshift-console, pod="true"}
ha_chassis_group    : []
mirror_rules        : []
name                : openshift-console_downloads-6cdd99fcbb-wvtpr
options             : {iface-id-ver="14b11e36-72aa-4f92-8192-6703f81a9e8e", requested-chassis=worker-0}
parent_name         : []
port_security       : ["0a:58:0a:81:00:07 10.129.0.7"]
```

The address_set is

```bash
sh-5.1# ovn-nbctl list address_set a5642994970181515866
_uuid               : c0206b39-3949-4829-8798-c64b3918eb2d
addresses           : ["10.128.0.108", "10.128.0.17", "10.128.0.67", "10.128.0.78", "10.128.0.80", "10.128.0.81", "10.128.0.82", "10.128.0.83", "10.129.0.10", "10.129.0.8", "10.130.0.9"]
external_ids        : {direction=Ingress, gress-index="0", ip-family=v4, "k8s.ovn.org/id"="default-network-controller:AdminNetworkPolicy:allow-monitoring:Ingress:0:v4", "k8s.ovn.org/name"=allow-monitoring, "k8s.ovn.org/owner-controller"=default-network-controller, "k8s.ovn.org/owner-type"=AdminNetworkPolicy}
name                : a5642994970181515866
```

Then we double confirm the address_set with the Pod IPs under openshift-monitoring

```bash
$ oc get pods -o wide -n openshift-monitoring
NAME                                                     READY   STATUS    RESTARTS   AGE   IP             NODE       NOMINATED NODE   READINESS GATES
alertmanager-main-0                                      6/6     Running   0          9h    10.130.0.9     worker-1   <none>           <none>
cluster-monitoring-operator-64f8745b4d-t9npd             1/1     Running   0          9h    10.128.0.17    master-0   <none>           <none>
kube-state-metrics-55f88d76b6-hx8hw                      3/3     Running   0          9h    10.128.0.81    master-0   <none>           <none>
metrics-server-59895676d4-sz58m                          1/1     Running   0          9h    10.128.0.83    master-0   <none>           <none>
monitoring-plugin-7b499bd6c-pst25                        1/1     Running   0          9h    10.128.0.108   master-0   <none>           <none>
node-exporter-blncn                                      2/2     Running   0          9h    172.16.0.104   worker-0   <none>           <none>
node-exporter-j5f94                                      2/2     Running   0          9h    172.16.0.101   master-0   <none>           <none>
node-exporter-jmw5b                                      2/2     Running   0          9h    172.16.0.105   worker-1   <none>           <none>
openshift-state-metrics-6fbcf6dfdf-zjq8c                 3/3     Running   0          9h    10.128.0.80    master-0   <none>           <none>
prometheus-k8s-0                                         6/6     Running   0          9h    10.129.0.10    worker-0   <none>           <none>
prometheus-operator-74d6869c45-mg86r                     2/2     Running   0          9h    10.128.0.78    master-0   <none>           <none>
prometheus-operator-admission-webhook-5c94965845-snfc7   1/1     Running   0          9h    10.128.0.67    master-0   <none>           <none>
telemeter-client-6d7f99bb4b-snxb8                        3/3     Running   0          9h    10.128.0.82    master-0   <none>           <none>
thanos-querier-5d7bb59b8c-627k9                          6/6     Running   0          9h    10.129.0.8     worker-0   <none>           <none>
```

### Tier and Priority

OVN uses tier to define the precedency of ACLs, aka the order of different layer of ACLs. This is used by the ovn-kubernetes to implement different hierarchy of network polices. 

https://man7.org/linux/man-pages/man5/ovn-nb.5.html#ACL_TABLE

```bash
tier: integer, in range 0 to 3
              The hierarchical tier that this ACL belongs to.

              ACLs can be assigned to numerical tiers. When evaluating
              ACLs, an internal counter is used to determine which tier
              of ACLs should be evaluated. Tier 0 ACLs are evaluated
              first. If no verdict can be determined, then tier 1 ACLs
              are evaluated next. This continues until the maximum tier
              value is reached. If all tiers of ACLs are evaluated and no
              verdict is reached, then the options:default_acl_drop
              option from table NB_Global is used to determine how to
              proceed.

              In this version of OVN, the maximum tier value for ACLs is
              3, meaning there are 4 tiers of ACLs allowed (0-3).
              
              
priority: integer, in range 0 to 32,767
              The QoS rule’s priority. Rules with numerically higher
              priority take precedence over those with lower. If two QoS
              rules with the same priority both match, then the one
              actually applied to a packet is undefined.
```

If we go back to [netpol](https://www.notion.so/2004a0a52326807e9b85e9efe5db19e8?pvs=21) and check normal netpol’s tier, we will find the tier of them are tier 2. Since ANP has tier 1, that’s why and the result that ANP takes precedency than NP. If ANPs are in the same tier, then the higher priority takes precedency, but in ANP yaml, the smaller priority takes precedency, which needs to be cared.

## Analyze the event of BANP - ACL

banp looks like this:

```bash
apiVersion: policy.networking.k8s.io/v1alpha1
kind: BaselineAdminNetworkPolicy
metadata:
  name: default
spec:
  priority: 9
  subject:
    namespaces: {}
  ingress:
  - name: "allow-ingress-from-dns"
    action: "Allow"
    from:
    - namespaces:
        matchLabels:
          kubernetes.io/metadata.name: openshift-dns
```

```bash
{"data":[["bc1e4050-cdc4-49ad-99b6-15ccb5fb33b2","insert","allow-related","to-lport",["map",[["direction","Ingress"],["gress-index","0"],["k8s.ovn.org/id","default-network-controller:BaselineAdminNetworkPolicy:default:Ingress:0:None"],["k8s.ovn.org/name","default"],["k8s.ovn.org/owner-controller","default-network-controller"],["k8s.ovn.org/owner-type","BaselineAdminNetworkPolicy"],["port-policy-protocol","None"]]],0,false,"outport == @a9550609891683691927 && ((ip4.src == $a168374317940583916))","acl-logging","BANP:default:Ingress:0",["map",[]],1750,["set",[]],["set",[]],["set",[]],3,["uuid","54315ef3-7eb2-4508-adbd-62e49404d06e"]]],"headings":["row","action","action","direction","external_ids","label","log","match","meter","name","options","priority","sample_est","sample_new","severity","tier","_version"]}
```

Then we take a look at the acl. Since we understand the tier in ovn acl, it is expected to see BANP has the lowest tier value. Let’s double confirm:

```bash
sh-5.1# ovn-nbctl list acl bc1e4050-cdc4-49ad-99b6-15ccb5fb33b2
_uuid               : bc1e4050-cdc4-49ad-99b6-15ccb5fb33b2
action              : allow-related
direction           : to-lport
external_ids        : {direction=Ingress, gress-index="0", "k8s.ovn.org/id"="default-network-controller:BaselineAdminNetworkPolicy:default:Ingress:0:None", "k8s.ovn.org/name"=default, "k8s.ovn.org/owner-controller"=default-network-controller, "k8s.ovn.org/owner-type"=BaselineAdminNetworkPolicy, port-policy-protocol=None}
label               : 0
log                 : false
match               : "outport == @a9550609891683691927 && ((ip4.src == $a168374317940583916))"
meter               : acl-logging
name                : "BANP:default:Ingress:0"
options             : {}
priority            : 1750
sample_est          : []
sample_new          : []
severity            : []
tier                : 3
```

It is perfect that we see BANP has highest tier 3, which means it will be evaluated lastly. Then we check the port_group and address_set as we did many times before:

```bash
sh-5.1# ovn-nbctl list port_group a9550609891683691927
_uuid               : 6eace039-870c-4aa3-a962-f7bd5875566a
acls                : [bc1e4050-cdc4-49ad-99b6-15ccb5fb33b2]
external_ids        : {"k8s.ovn.org/id"="default-network-controller:BaselineAdminNetworkPolicy:default", "k8s.ovn.org/name"=default, "k8s.ovn.org/owner-controller"=default-network-controller, "k8s.ovn.org/owner-type"=BaselineAdminNetworkPolicy}
name                : a9550609891683691927
ports               : [098294fe-ece5-4dd3-8d89-8266d989b129, 4487b8cd-fe70-4d76-9255-41b261bd99b7, 45d36d33-9bc2-40e7-a264-456d3ecc845c, 4908cf45-aa2e-4559-a45b-a3b6e58f309e, 7fecfef0-f5d2-47d9-b16f-dab7369032fb, c265e0b8-eb92-44aa-8d93-9b62d85e0385, ebe9e9f9-f27f-42e8-a3c1-448f5e179932]

sh-5.1# ovn-nbctl list address_set a168374317940583916
_uuid               : 35993657-6bed-4279-9315-a5cf5a51f810
addresses           : ["10.128.0.68", "10.129.0.6", "10.130.0.6"]
external_ids        : {direction=Ingress, gress-index="0", ip-family=v4, "k8s.ovn.org/id"="default-network-controller:BaselineAdminNetworkPolicy:default:Ingress:0:v4", "k8s.ovn.org/name"=default, "k8s.ovn.org/owner-controller"=default-network-controller, "k8s.ovn.org/owner-type"=BaselineAdminNetworkPolicy}
name                : a168374317940583916
```

We check some ports and confirm the addresses

```bash
sh-5.1# ovn-nbctl list logical_switch_port 098294fe-ece5-4dd3-8d89-8266d989b129
_uuid               : 098294fe-ece5-4dd3-8d89-8266d989b129
addresses           : ["0a:58:0a:81:00:05 10.129.0.5"]
dhcpv4_options      : []
dhcpv6_options      : []
dynamic_addresses   : []
enabled             : []
external_ids        : {namespace=openshift-ingress-canary, pod="true"}
ha_chassis_group    : []
mirror_rules        : []
name                : openshift-ingress-canary_ingress-canary-l8vrv
options             : {iface-id-ver="2783218f-b0dc-4c08-9a63-cbd84cb17225", requested-chassis=worker-0}
parent_name         : []
port_security       : ["0a:58:0a:81:00:05 10.129.0.5"]

$ oc get pods -n openshift-dns -o wide
NAME                  READY   STATUS    RESTARTS   AGE   IP             NODE       NOMINATED NODE   READINESS GATES
dns-default-4gffg     2/2     Running   0          9h    10.129.0.6     worker-0   <none>           <none>
dns-default-4t7qr     2/2     Running   0          9h    10.130.0.6     worker-1   <none>           <none>
dns-default-6m7j6     2/2     Running   0          9h    10.128.0.68    master-0   <none>           <none>
node-resolver-55rc6   1/1     Running   0          9h    172.16.0.101   master-0   <none>           <none>
node-resolver-9sc6p   1/1     Running   0          9h    172.16.0.104   worker-0   <none>           <none>
node-resolver-czvtj   1/1     Running   0          9h    172.16.0.105   worker-1   <none>           <none>
```

## Summary

1. ANP (Admin Network Policy) operates at tier 1 in OVN's ACL system, taking precedence over regular NetworkPolicies which operate at tier 2.
2. Within ANPs, priority values work inversely - lower priority numbers in the ANP YAML take precedence over higher ones.
3. BANP (Baseline Admin Network Policy) operates at tier 3, meaning it's evaluated last in the ACL chain after regular NetworkPolicies and ANPs.
4. The implementation follows OVN's tiered ACL system (tiers 0-3), where lower tier numbers are evaluated first. If no verdict is reached after evaluating all tiers, the system falls back to the default_acl_drop option.
5. The ACL implementation for these policies uses port groups and address sets to manage the allowed traffic patterns, similar to regular NetworkPolicies.