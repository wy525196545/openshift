# 02 ovn-k netpol

The netpol is implemented by acls and group port. Let’s take a look what should they exist inside the nbdb.

## ovsdb-client monitor tool

There is a tool that we can use to monitor the NBDB what exactly was inserted or deleted when certain k8s object has been created and ovnkube-controller translates the k8s objects into ovn-kubernetes nbdb object. If we want to track the ACL table of NBDB:

```bash
$ ovsdb-client monitor --format=json unix:/var/run/ovn/ovnnb_db.sock ACL
```

To list all the tables under the OVN nbdb:

```bash
sh-5.1# ovsdb-client list-tables unix:/var/run/ovn/ovnnb_db.sock
```

At the same time, create a netpol in other terminal and check the result. 

```bash
$ cat netpol.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-from-openshift-console
spec:
  podSelector:
    matchLabels:
      app: toolbox
  policyTypes:
  - Ingress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          kubernetes.io/metadata.name: openshift-console
```

The first rule is the default deny-all rule if any netpol is applied. You see drop for Egress and Ingress.

```bash
{
  "data": [
    [
      "**118ed3bd-7f12-4c72-8033-f0b7a28e5984**",
      "insert",
      "drop",
      "from-lport",
      [
        "map",
        [
          [
            "direction",
            "Egress"
          ],
          [
            "k8s.ovn.org/id",
            "default-network-controller:NetpolNamespace:test-svc:Egress:defaultDeny"
          ],
          [
            "k8s.ovn.org/name",
            "test-svc"
          ],
          [
            "k8s.ovn.org/owner-controller",
            "default-network-controller"
          ],
          [
            "k8s.ovn.org/owner-type",
            "NetpolNamespace"
          ],
          [
            "type",
            "defaultDeny"
          ]
        ]
      ],
      0,
      false,
      "inport == @a4931194819496400786_egressDefaultDeny",
      "acl-logging",
      "NP:test-svc:Egress",
      [
        "map",
        [
          [
            "apply-after-lb",
            "true"
          ]
        ]
      ],
      1000,
      [
        "set",
        []
      ],
      2,
      [
        "uuid",
        "b9eaf6a5-12d9-4d16-8e63-e7aa2ff18301"
      ]
    ],
    [
      "**050e37de-601f-493e-8924-91f579233c1c**",
      "insert",
      "allow",
      "from-lport",
      [
        "map",
        [
          [
            "direction",
            "Egress"
          ],
          [
            "k8s.ovn.org/id",
            "default-network-controller:NetpolNamespace:test-svc:Egress:arpAllow"
          ],
          [
            "k8s.ovn.org/name",
            "test-svc"
          ],
          [
            "k8s.ovn.org/owner-controller",
            "default-network-controller"
          ],
          [
            "k8s.ovn.org/owner-type",
            "NetpolNamespace"
          ],
          [
            "type",
            "arpAllow"
          ]
        ]
      ],
      0,
      false,
      "inport == @a4931194819496400786_egressDefaultDeny && (arp || nd)",
      "acl-logging",
      "NP:test-svc:Egress",
      [
        "map",
        [
          [
            "apply-after-lb",
            "true"
          ]
        ]
      ],
      1001,
      [
        "set",
        []
      ],
      2,
      [
        "uuid",
        "cfad38db-6ea8-4e87-af3c-66da163531d7"
      ]
    ],
    [
      "**a8ae0d37-f319-4e44-9269-59d34dd99e6f**",
      "insert",
      "allow",
      "to-lport",
      [
        "map",
        [
          [
            "direction",
            "Ingress"
          ],
          [
            "k8s.ovn.org/id",
            "default-network-controller:NetpolNamespace:test-svc:Ingress:arpAllow"
          ],
          [
            "k8s.ovn.org/name",
            "test-svc"
          ],
          [
            "k8s.ovn.org/owner-controller",
            "default-network-controller"
          ],
          [
            "k8s.ovn.org/owner-type",
            "NetpolNamespace"
          ],
          [
            "type",
            "arpAllow"
          ]
        ]
      ],
      0,
      false,
      "outport == @a4931194819496400786_ingressDefaultDeny && (arp || nd)",
      "acl-logging",
      "NP:test-svc:Ingress",
      [
        "map",
        []
      ],
      1001,
      [
        "set",
        []
      ],
      2,
      [
        "uuid",
        "3404e025-3aa5-4c12-91de-be85b28214be"
      ]
    ],
    [
      "**9afcfbff-a0bb-4ed2-9249-ccaf9dacc9f4**",
      "insert",
      "drop",
      "to-lport",
      [
        "map",
        [
          [
            "direction",
            "Ingress"
          ],
          [
            "k8s.ovn.org/id",
            "default-network-controller:NetpolNamespace:test-svc:Ingress:defaultDeny"
          ],
          [
            "k8s.ovn.org/name",
            "test-svc"
          ],
          [
            "k8s.ovn.org/owner-controller",
            "default-network-controller"
          ],
          [
            "k8s.ovn.org/owner-type",
            "NetpolNamespace"
          ],
          [
            "type",
            "defaultDeny"
          ]
        ]
      ],
      0,
      false,
      "outport == @a4931194819496400786_ingressDefaultDeny",
      "acl-logging",
      "NP:test-svc:Ingress",
      [
        "map",
        []
      ],
      1000,
      [
        "set",
        []
      ],
      2,
      [
        "uuid",
        "5ea634dd-230f-4662-9722-a2105dc4f05f"
      ]
    ]
  ],
  "headings": [
    "row",
    "action",
    "action",
    "direction",
    "external_ids",
    "label",
    "log",
    "match",
    "meter",
    "name",
    "options",
    "priority",
    "severity",
    "tier",
    "_version"
  ]
}

{
  "data": [
    [
      "**8366192e-6afb-4c7a-89cd-d34e5b52a8c3**",
      "insert",
      "allow-related",
      "to-lport",
      [
        "map",
        [
          [
            "direction",
            "Ingress"
          ],
          [
            "gress-index",
            "0"
          ],
          [
            "ip-block-index",
            "-1"
          ],
          [
            "k8s.ovn.org/id",
            "default-network-controller:NetworkPolicy:test-svc:allow-from-openshift-console:Ingress:0:None:-1"
          ],
          [
            "k8s.ovn.org/name",
            "test-svc:allow-from-openshift-console"
          ],
          [
            "k8s.ovn.org/owner-controller",
            "default-network-controller"
          ],
          [
            "k8s.ovn.org/owner-type",
            "NetworkPolicy"
          ],
          [
            "port-policy-protocol",
            "None"
          ]
        ]
      ],
      0,
      false,
      "ip4.src == {$a11622011068173273797} && outport == @a16753228860045385154",
      "acl-logging",
      "NP:test-svc:allow-from-openshift-console:Ingress:0",
      [
        "map",
        []
      ],
      1001,
      [
        "set",
        []
      ],
      2,
      [
        "uuid",
        "91b17058-7ac4-4ef7-b6f8-512ebaef46f7"
      ]
    ]
  ],
  "headings": [
    "row",
    "action",
    "action",
    "direction",
    "external_ids",
    "label",
    "log",
    "match",
    "meter",
    "name",
    "options",
    "priority",
    "severity",
    "tier",
    "_version"
  ]
}
```

## Analyze the events of ACL

In order to better see the progress of analysis, let’s use a table to track our process.

| id | Direction | Policy | Finished |
| --- | --- | --- | --- |
| 118ed3bd-7f12-4c72-8033-f0b7a28e5984 | Egress | Drop | ❌ |
| 050e37de-601f-493e-8924-91f579233c1c | Egress | Allow | ❌ |
| a8ae0d37-f319-4e44-9269-59d34dd99e6f | Ingress | Allow | ❌ |
| 9afcfbff-a0bb-4ed2-9249-ccaf9dacc9f4 | Ingress | Drop | ❌ |
| 8366192e-6afb-4c7a-89cd-d34e5b52a8c3 | Ingress | Allow-Related | ❌ |

Let’s take a closer look at the first ACL. There are two drops and if we filter its _uuid for each drop rule, it will be much easier to track:

```bash
sh-5.1# ovn-nbctl list acl 118ed3bd-7f12-4c72-8033-f0b7a28e5984
_uuid               : 118ed3bd-7f12-4c72-8033-f0b7a28e5984
action              : drop
direction           : from-lport
external_ids        : {direction=Egress, "k8s.ovn.org/id"="default-network-controller:NetpolNamespace:test-svc:Egress:defaultDeny", "k8s.ovn.org/name"=test-svc, "k8s.ovn.org/owner-controller"=default-network-controller, "k8s.ovn.org/owner-type"=NetpolNamespace, type=defaultDeny}
label               : 0
log                 : false
match               : "inport == @a4931194819496400786_egressDefaultDeny"
meter               : acl-logging
name                : "NP:test-svc:Egress"
options             : {apply-after-lb="true"}
priority            : 1000
severity            : []
tier                : 2
```

If we taking the latter as an example to further look, it is easy to tell @a49311 is a port_group

```bash
sh-5.1# ovn-nbctl list port_group a4931194819496400786_egressDefaultDeny
_uuid               : 53d20031-4392-440a-89ca-16a42eeaaead
acls                : [050e37de-601f-493e-8924-91f579233c1c, 118ed3bd-7f12-4c72-8033-f0b7a28e5984]
external_ids        : {name=a4931194819496400786_egressDefaultDeny}
name                : a4931194819496400786_egressDefaultDeny
ports               : []
```

Since we don’t have egress Netpol defined, the ports are empty.

| id | Direction | Policy | Finished | Function |
| --- | --- | --- | --- | --- |
| 118ed3bd-7f12-4c72-8033-f0b7a28e5984 | Egress | Drop | ✅ | Deny All |
| 050e37de-601f-493e-8924-91f579233c1c | Egress | Allow | ❌ |  |
| a8ae0d37-f319-4e44-9269-59d34dd99e6f | Ingress | Allow | ❌ |  |
| 9afcfbff-a0bb-4ed2-9249-ccaf9dacc9f4 | Ingress | Drop | ❌ |  |
| 8366192e-6afb-4c7a-89cd-d34e5b52a8c3 | Ingress | Allow-Related | ❌ |  |

Then we take a look at the second Egress Allow acl:

```bash
sh-5.1# ovn-nbctl list acl  050e37de-601f-493e-8924-91f579233c1c
_uuid               : 050e37de-601f-493e-8924-91f579233c1c
action              : allow
direction           : from-lport
external_ids        : {direction=Egress, "k8s.ovn.org/id"="default-network-controller:NetpolNamespace:test-svc:Egress:arpAllow", "k8s.ovn.org/name"=test-svc, "k8s.ovn.org/owner-controller"=default-network-controller, "k8s.ovn.org/owner-type"=NetpolNamespace, type=arpAllow}
label               : 0
log                 : false
match               : "inport == @a4931194819496400786_egressDefaultDeny && (arp || nd)"
meter               : acl-logging
name                : "NP:test-svc:Egress"
options             : {apply-after-lb="true"}
priority            : 1001
severity            : []
tier                : 2
```

The above acl means the arp or nd is allowed for the Egress. BTW nd means neighbor discovery and you could regard it as IPv6’s ARP. So K8s always allows L2 to work regardless network policy.

| id | Direction | Policy | Finished | Function |
| --- | --- | --- | --- | --- |
| 118ed3bd-7f12-4c72-8033-f0b7a28e5984 | Egress | Drop | ✅ | Deny All |
| 050e37de-601f-493e-8924-91f579233c1c | Egress | Allow | ✅ | Allow ARP or ND |
| a8ae0d37-f319-4e44-9269-59d34dd99e6f | Ingress | Allow | ❌ |  |
| 9afcfbff-a0bb-4ed2-9249-ccaf9dacc9f4 | Ingress | Drop | ❌ |  |
| 8366192e-6afb-4c7a-89cd-d34e5b52a8c3 | Ingress | Allow-Related | ❌ |  |

Similarly the third Ingress Allow rule is to open ARP or ND traffic for Ingress direction:

```bash
sh-5.1# ovn-nbctl list acl a8ae0d37-f319-4e44-9269-59d34dd99e6f
_uuid               : a8ae0d37-f319-4e44-9269-59d34dd99e6f
action              : allow
direction           : to-lport
external_ids        : {direction=Ingress, "k8s.ovn.org/id"="default-network-controller:NetpolNamespace:test-svc:Ingress:arpAllow", "k8s.ovn.org/name"=test-svc, "k8s.ovn.org/owner-controller"=default-network-controller, "k8s.ovn.org/owner-type"=NetpolNamespace, type=arpAllow}
label               : 0
log                 : false
match               : "outport == @a4931194819496400786_ingressDefaultDeny && (arp || nd)"
meter               : acl-logging
name                : "NP:test-svc:Ingress"
options             : {}
priority            : 1001
severity            : []
tier                : 2
```

| id | Direction | Policy | Finished | Function |
| --- | --- | --- | --- | --- |
| 118ed3bd-7f12-4c72-8033-f0b7a28e5984 | Egress | Drop | ✅ | Deny All |
| 050e37de-601f-493e-8924-91f579233c1c | Egress | Allow | ✅ | Allow APR or ND |
| a8ae0d37-f319-4e44-9269-59d34dd99e6f | Ingress | Allow | ✅ | Allow ARP or ND |
| 9afcfbff-a0bb-4ed2-9249-ccaf9dacc9f4 | Ingress | Drop | ❌ |  |
| 8f90f85e-55ee-461e-9e64-95d36505ed73 | Ingress | Allow-Related | ❌ |  |

```bash
sh-5.1# ovn-nbctl list acl 9afcfbff-a0bb-4ed2-9249-ccaf9dacc9f4
_uuid               : 9afcfbff-a0bb-4ed2-9249-ccaf9dacc9f4
action              : drop
direction           : to-lport
external_ids        : {direction=Ingress, "k8s.ovn.org/id"="default-network-controller:NetpolNamespace:test-svc:Ingress:defaultDeny", "k8s.ovn.org/name"=test-svc, "k8s.ovn.org/owner-controller"=default-network-controller, "k8s.ovn.org/owner-type"=NetpolNamespace, type=defaultDeny}
label               : 0
log                 : false
match               : "outport == @a4931194819496400786_ingressDefaultDeny"
meter               : acl-logging
name                : "NP:test-svc:Ingress"
options             : {}
priority            : 1000
severity            : []
tier                : 2
```

It apparently has a port_group a493119 and let’s see whether it has any matched ports:

```bash
sh-5.1# ovn-nbctl list port_group a4931194819496400786_ingressDefaultDeny
_uuid               : d48c062c-f28b-4ab5-93ea-cb9641858f1b
acls                : [9afcfbff-a0bb-4ed2-9249-ccaf9dacc9f4, a8ae0d37-f319-4e44-9269-59d34dd99e6f]
external_ids        : {name=a4931194819496400786_ingressDefaultDeny}
name                : a4931194819496400786_ingressDefaultDeny
ports               : [8e9696cb-2424-4df5-a691-89e99047e0b1]
```

This time we got the matched ports under this port_group because we defined Ingress NetworkPolicy. It will take effect on the ports 8e9696cb-2424-4df5-a691-89e99047e0b1, which is our Pod port:

```bash
sh-5.1# ovn-nbctl list logical_switch_port 8e9696cb-2424-4df5-a691-89e99047e0b1
_uuid               : 8e9696cb-2424-4df5-a691-89e99047e0b1
addresses           : ["0a:58:0a:81:00:10 10.129.0.16"]
dhcpv4_options      : []
dhcpv6_options      : []
dynamic_addresses   : []
enabled             : []
external_ids        : {namespace=test-svc, pod="true"}
ha_chassis_group    : []
mirror_rules        : []
name                : test-svc_toolbox-deployment-9b79df6d5-pmhtx
options             : {iface-id-ver="a7ce1561-0d8f-4d9f-ae5e-e098cfca04bc", requested-chassis=worker-0}
parent_name         : []
port_security       : ["0a:58:0a:81:00:10 10.129.0.16"]
tag                 : []
tag_request         : []
type                : ""
up                  : true
```

```bash
[root@dell-per430-35 ovn]# oc get pods -o wide -n test-svc
NAME                                 READY   STATUS    RESTARTS   AGE    IP            NODE       NOMINATED NODE   READINESS GATES
toolbox-deployment-9b79df6d5-pmhtx   1/1     Running   0          4h8m   10.129.0.16   worker-0   <none>           <none>
```

In OVN port_group is usually used to firstly group a set of groups under the same namespace then apply acl on this group of ports. It is technically possible to apply acl on individual port but it is less convenient and practical.

| id | Direction | Policy | Finished | Function |
| --- | --- | --- | --- | --- |
| 118ed3bd-7f12-4c72-8033-f0b7a28e5984 | Egress | Drop | ✅ | Deny All |
| 050e37de-601f-493e-8924-91f579233c1c | Egress | Allow | ✅ | Allow ARP or ND |
| a8ae0d37-f319-4e44-9269-59d34dd99e6f | Ingress | Allow | ✅ | Allow ARP or ND |
| 9afcfbff-a0bb-4ed2-9249-ccaf9dacc9f4 | Ingress | Drop | ✅ | Deny All |
| 8366192e-6afb-4c7a-89cd-d34e5b52a8c3 | Ingress | Allow-Related | ❌ |  |

Then we take a look at the last acl rule

```bash
sh-5.1# ovn-nbctl list acl 8366192e-6afb-4c7a-89cd-d34e5b52a8c3
_uuid               : 8366192e-6afb-4c7a-89cd-d34e5b52a8c3
action              : allow-related
direction           : to-lport
external_ids        : {direction=Ingress, gress-index="0", ip-block-index="-1", "k8s.ovn.org/id"="default-network-controller:NetworkPolicy:test-svc:allow-from-openshift-console:Ingress:0:None:-1", "k8s.ovn.org/name"="test-svc:allow-from-openshift-console", "k8s.ovn.org/owner-controller"=default-network-controller, "k8s.ovn.org/owner-type"=NetworkPolicy, port-policy-protocol=None}
label               : 0
log                 : false
match               : "ip4.src == {$a11622011068173273797} && outport == @a16753228860045385154"
meter               : acl-logging
name                : "NP:test-svc:allow-from-openshift-console:Ingress:0"
options             : {}
priority            : 1001
severity            : []
tier                : 2
```

Normally the string which starts with $ means it is an address_set, while the string which starts with @ is port_group, as we mentioned before.

```bash
sh-5.1# ovn-nbctl list address_set a11622011068173273797
_uuid               : 20562610-009c-4f5d-9907-ea3aa54e86ee
addresses           : ["10.128.0.20", "10.128.0.9"]
external_ids        : {ip-family=v4, "k8s.ovn.org/id"="default-network-controller:Namespace:openshift-console:v4", "k8s.ovn.org/name"=openshift-console, "k8s.ovn.org/owner-controller"=default-network-controller, "k8s.ovn.org/owner-type"=Namespace}
name                : a11622011068173273797
```

Remember the network policy rule? We allow the Pods from openshift-console to access our Pods and let’s see whether the IPs match:

```bash
[root@dell-per430-35 ~]# oc get pods -n openshift-console -o wide
NAME                        READY   STATUS    RESTARTS       AGE   IP            NODE       NOMINATED NODE   READINESS GATES
console-6d65b99df4-4cks2    1/1     Running   20             11d   10.128.0.20   master-0   <none>           <none>
downloads-6548f4b5d-9kj6f   1/1     Running   37 (10d ago)   11d   10.128.0.9    master-0   <none>           <none>
```

And finally check the port_group:

```bash
sh-5.1# ovn-nbctl list port_group a16753228860045385154
_uuid               : 5bbbd234-15f3-4f9a-bdc3-a3b62836c909
acls                : [8366192e-6afb-4c7a-89cd-d34e5b52a8c3]
external_ids        : {name=test-svc_allow-from-openshift-console}
name                : a16753228860045385154
ports               : [8e9696cb-2424-4df5-a691-89e99047e0b1]
```

| id | Direction | Policy | Finished | Function |
| --- | --- | --- | --- | --- |
| 118ed3bd-7f12-4c72-8033-f0b7a28e5984 | Egress | Drop | ✅ | Deny All |
| 050e37de-601f-493e-8924-91f579233c1c | Egress | Allow | ✅ | Allow ARP or ND |
| a8ae0d37-f319-4e44-9269-59d34dd99e6f | Ingress | Allow | ✅ | Allow ARP or ND |
| 9afcfbff-a0bb-4ed2-9249-ccaf9dacc9f4 | Ingress | Drop | ✅ | Deny All |
| 8366192e-6afb-4c7a-89cd-d34e5b52a8c3 | Ingress | Allow-Related | ✅ | Allow specific address_set to specific port_group |

## Analyze the events of Port_Group

Since ACL has relationship with port_group, it is natural to think during the netpol creation, new port_groups will be created as well. Let’s use the ovsdb-client monitor again to track the Port_Group:

```bash
sh-5.1# ovsdb-client monitor --format=json unix:/var/run/ovn/ovnnb_db.sock Port_Group
```

We will see 4 events created in our sample.

```bash
{"data":[["ee237e6d-2035-4a41-8acd-d469632ea1c2","insert",["set",[["uuid","c6cebcce-681c-4926-a389-29b331479b62"],["uuid","d182f985-c79f-49b7-abd2-305e1dccde82"]]],["map",[["name","a4931194819496400786_egressDefaultDeny"]]],"a4931194819496400786_egressDefaultDeny",["set",[]],["uuid","d9bac07c-b018-431f-994e-200437df7ff1"]],["c80c509e-6d50-4f00-886a-4d732680b451","insert",["set",[["uuid","1dd73076-d72c-44d2-8c46-85a6a0c6c10d"],["uuid","2e9a8d39-97eb-410c-9019-a7f51cd4165e"]]],["map",[["name","a4931194819496400786_ingressDefaultDeny"]]],"a4931194819496400786_ingressDefaultDeny",["set",[]],["uuid","a265ec6f-fb7a-4136-a4b3-96a50035d1f1"]]],"headings":["row","action","acls","external_ids","name","ports","_version"]}
{"data":[["4609e395-8af4-4654-bc88-022725ccf2d9","insert",["set",[]],["map",[["name","test-svc_allow-from-openshift-console"]]],"a16753228860045385154",["set",[]],["uuid","db6c2e2c-074b-4d36-b079-93427124bb41"]]],"headings":["row","action","acls","external_ids","name","ports","_version"]}
{"data":[["4609e395-8af4-4654-bc88-022725ccf2d9","old",["set",[]],null,null,null,["uuid","db6c2e2c-074b-4d36-b079-93427124bb41"]],["","new",["uuid","8056450c-c2c4-436b-bd6a-6b0a3cdbd2a8"],["map",[["name","test-svc_allow-from-openshift-console"]]],"a16753228860045385154",["set",[]],["uuid","c575653a-6ecc-4cf0-a141-fdab65c5b496"]]],"headings":["row","action","acls","external_ids","name","ports","_version"]}
{"data":[["c80c509e-6d50-4f00-886a-4d732680b451","old",null,null,null,["set",[]],["uuid","a265ec6f-fb7a-4136-a4b3-96a50035d1f1"]],["","new",["set",[["uuid","1dd73076-d72c-44d2-8c46-85a6a0c6c10d"],["uuid","2e9a8d39-97eb-410c-9019-a7f51cd4165e"]]],["map",[["name","a4931194819496400786_ingressDefaultDeny"]]],"a4931194819496400786_ingressDefaultDeny",["uuid","61d1202e-71c5-487b-b339-b20446baa8ae"],["uuid","990d6b69-46f4-4ef4-8f58-96e24f95b41c"]],["4609e395-8af4-4654-bc88-022725ccf2d9","old",null,null,null,["set",[]],["uuid","c575653a-6ecc-4cf0-a141-fdab65c5b496"]],["","new",["uuid","8056450c-c2c4-436b-bd6a-6b0a3cdbd2a8"],["map",[["name","test-svc_allow-from-openshift-console"]]],"a16753228860045385154",["uuid","61d1202e-71c5-487b-b339-b20446baa8ae"],["uuid","2ce567e3-5117-4528-90d2-17e22084f923"]]],"headings":["row","action","acls","external_ids","name","ports","_version"]}
```

### **Event 1: Batch Insert of 2 Port_Groups**

```
{
  "data": [
    ["ee237e6d-2035-4a41-8acd-d469632ea1c2", "insert", ...],// egressDefaultDeny["c80c509e-6d50-4f00-886a-4d732680b451", "insert", ...]// ingressDefaultDeny]
}
```

| **UUID** | **Name** | **Type** | **Key Details** |
| --- | --- | --- | --- |
| **`d9bac07c-b018-431f-994e-200437df7ff1`** | **`a4931194819496400786_egressDefaultDeny`** | Insert | - ACLs: [**`c6cebcce...`**, **`d182f985...`**]- Ports: Empty |
| **`a265ec6f-fb7a-4136-a4b3-96a50035d1f1`** | **`a4931194819496400786_ingressDefaultDeny`** | Insert | - ACLs: [**`1dd73076...`**, **`2e9a8d39...`**]- Ports: Empty |

### **Event 2: Insert Allow-Rule Port_Group**

```
{
  "data": [
    ["4609e395-8af4-4654-bc88-022725ccf2d9", "insert", ...]
  ]
}
```

| **UUID** | **Name** | **Type** | **Key Details** |
| --- | --- | --- | --- |
| **`db6c2e2c-074b-4d36-b079-93427124bb41`** | **`test-svc_allow-from-openshift-console`** | Insert | - ACLs: Empty- Ports: Empty |

### **Event 3: Modify Allow-Rule Port_Group (Add ACL)**

```
{
  "data": [
    ["4609e395-8af4-4654-bc88-022725ccf2d9", "old", ...],
    ["", "new", ...]
  ]
}
```

| **UUID** | **Change** | **Before (Old)** | **After (New)** |
| --- | --- | --- | --- |
| **`db6c2e2c...`** → **`c575653a...`** | Update ACL | - ACLs: **`[]`** | - ACLs: [**`8056450c...`**] (allow-rule) |

### **Event 4: Batch Modify (Add Ports)**

```
{
  "data": [
    ["c80c509e-6d50-4f00-886a-4d732680b451", "old", ...],// ingressDefaultDeny["", "new", ...],
    ["4609e395-8af4-4654-bc88-022725ccf2d9", "old", ...],// allow-from-openshift-console["", "new", ...]
  ]
}
```

| **UUID** | **Name** | **Change** | **Port Added** |
| --- | --- | --- | --- |
| **`a265ec6f...`** → **`990d6b69...`** | **`a4931194819496400786_ingressDefaultDeny`** | Add Port | **`61d1202e-71c5...`** (pod) |
| **`c575653a...`** → **`2ce567e3...`** | **`test-svc_allow-from-openshift-console`** | Add Same Port | **`61d1202e-71c5...`** (pod) |

So it has two inserts and 2 modification operations which includes old and new to show what has been changed in the modifications. 2 Inserts are used to create default port_group for Egress deny and Ingress deny while 2 modify operations are used to attach the ACL and change the corresponding port_group otherwise the port under the port_group is empty.

## Summary

The port_group selects the affected Pods, then it has the acls to restrict the actual rules, by using address_set to restrict the source of the Pods in case of Ingress network policy, where the source Pods belong to other namespace. The port group selects the ports that exist in ${Node} logical switch.