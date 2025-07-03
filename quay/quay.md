# Quay 容器镜像仓库分享

**作者：魏阳**  
**日期：2025-06-26**

---

## 一、Quay 概述

- 什么是 Quay  
- 核心功能：
    - 镜像托管与分发  
    - 安全扫描（Clair/Quay Scanner）  
    - 地理复制（Geo-Replication）  
    - 访问控制与策略管理  

---

## 二、架构与组件
Quay 的主要架构组件包括：

- **quay-server**：主服务进程，负责 API、Web UI、身份认证、镜像管理等核心功能。
- **worker**：后台任务处理，包括镜像安全扫描、垃圾回收、统计等。
    - **nginx**：反向代理，处理 HTTP/HTTPS 流量。
    - **gunicorn-web**：Web API 服务进程。
    - **gunicorn-registry**：镜像仓库 API 服务进程。
    - **gcworker**：垃圾回收任务处理。
    - **repositorygcworker**：仓库级别垃圾回收。
    - **namespacegcworker**：命名空间级别垃圾回收。
    - **security worker**：安全扫描任务处理。
    - **Globalpromstats**：Prometheus 指标收集。
    - **Servicekeyworker**：服务密钥管理。
- **redis**：缓存与队列服务，加速数据访问与任务调度。
- **registry**：兼容 OCI/Docker 的镜像存储与分发服务。
- **PostgreSQL**：关系型数据库，存储元数据、用户信息等。
- **存储后端**：支持本地磁盘、S3、Ceph 等多种对象存储方案。



---

## 三、部署方式

- [Red Hat Quay on OpenShift Container Platform](https://docs.redhat.com/en/documentation/red_hat_quay/3.14/html/deploying_the_red_hat_quay_operator_on_openshift_container_platform/index)  ------》 OCPPlus订阅
- [Red Hat Quay Proof of Concept](https://docs.redhat.com/en/documentation/red_hat_quay/3.14/html/proof_of_concept_-_deploying_red_hat_quay/index)  ------》Red Hat Quay stand 订阅
- [Red Hat Quay - High Availability](https://docs.redhat.com/en/documentation/red_hat_quay/3.14/html/deploy_red_hat_quay_-_high_availability/index) ------》Red Hat Quay stand 订阅
- [Creating a mirror registry with mirror registry for Red Hat OpenShift](https://docs.redhat.com/en/documentation/openshift_container_platform/4.16/html/disconnected_installation_mirroring/installing-mirroring-creating-registry) ------》OCP 订阅

---

## 四、日常使用

- 镜像的推送与拉取（docker/podman login、push、pull）
- 镜像标签管理与版本控制
- 访问权限设置（团队、用户、机器人账号）
- 镜像安全扫描与漏洞报告查看
- 镜像仓库的浏览与搜索
- 镜像清理与空间管理（自动垃圾回收）
- 审计日志与操作记录查询
- Web UI 与 API 的常用操作
- 镜像同步与地理复制的日常维护


---

## 五、案例分享Quay 常见排错方法

- **服务不可用/登录失败**  
    - 检查 Quay Pod/服务状态，确认所有组件正常运行。
    - 查看 Quay 日志（如 `quay-server`、`worker`、`registry`）获取详细错误信息。
    - 检查数据库（PostgreSQL）、Redis、存储后端的连接状态。

- **镜像推送/拉取失败**  
    - 确认客户端（docker/podman）登录凭证正确，仓库地址无误。
    - 检查网络连通性、防火墙设置及 TLS 证书有效性。
    - 查看 registry 组件日志，定位 401/403/500 等错误。

- **安全扫描异常**  
    - 检查 Clair/Quay Scanner 服务状态及日志。
    - 确认镜像格式和层数符合扫描要求。

- **空间不足/垃圾回收无效**  
    - 检查存储后端容量，确认垃圾回收任务是否正常执行。
    - 查看 gcworker、repositorygcworker 日志。

- **权限与访问控制问题**  
    - 检查团队、用户、机器人账号的权限配置。
    - 确认仓库的可见性和访问策略设置。




