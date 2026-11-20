# 模块：服务配置（第 107—113 讲）。深度：认得出。
from qhelp import Q, TF

MODULE = {
    'id': 'config', 'title': '配置中心：Config Server、ZooKeeper、Consul、Nacos、Apollo', 'short': '配置中心',
    'group': '第十四章 服务配置', 'exam': '第 107—113 讲',
    'refs': [{'label': 'Spring Cloud Config 文档（Greenwich）', 'url': 'https://cloud.spring.io/spring-cloud-config/2.1.x/single/spring-cloud-config.html'}],
    'lessons': [
        {'title': 'Spring Cloud Config：基于 Git 的配置中心', 'cards': [
'''### 一句话

服务多了，每个服务的配置文件分散在各处，改一次很麻烦。**配置中心 = 把所有服务的配置集中管理，服务启动时去配置中心拿配置。**

> 💡 和注册中心区分：**注册中心管「服务在哪」，配置中心管「用什么配置」。**

### Config Server（第 107 讲）

| 看到题目说…… | 就选 |
|---|---|
| 开启配置中心服务端 | **@EnableConfigServer** |
| 默认的配置存储后端 | **Git**（也支持 SVN、本地文件、Vault、JDBC 等） |
| 常用端口 | 8888 |

**三个词确定要读哪份配置（必背）：**

| 词 | 意思 |
|---|---|
| **application** | 应用名（spring.application.name） |
| **profile** | 环境（如 dev、prod） |
| **label** | 版本，对 Git 来说就是**分支**（默认 master） |

访问路径举例：`/{application}/{profile}/{label}`，如 `/waiter-service/dev/master`。''',
'''### 客户端和刷新（第 108 讲）

| 看到题目说…… | 就选 |
|---|---|
| 客户端的起步依赖 | **spring-cloud-starter-config** |
| 配置中心地址写在哪个文件里 | **bootstrap.yml / bootstrap.properties**（比 application 更早加载） |
| 配置中心地址 | **spring.cloud.config.uri** |
| 连不上配置中心就**立刻启动失败** | **spring.cloud.config.fail-fast=true** |
| 连不上时**重试** | 引入 spring-retry，配置重试 |
| 通过**服务发现**找配置中心 | spring.cloud.config.discovery.enabled=true |

**配置改了，怎么让程序用上新值：**
1. 在 Bean 上贴 **@RefreshScope**（标记它可以被刷新）；
2. 调用 **/actuator/refresh** 端点（POST 请求）。

> 📌 必背：**@RefreshScope + /actuator/refresh。**'''
        ]},
        {'title': '刷新方式和其他配置中心', 'cards': [
'''### 配置抽象和三种刷新方式（第 110 讲）

- 远程配置通过 **PropertySourceLocator** 接入 Spring 的 Environment（Boot 原理模块讲过 PropertySource）；
- 远程配置默认**优先于**本地配置。

| 刷新方式 | 一句话 |
|---|---|
| **单个实例刷新** | 逐个调用每个实例的 /actuator/refresh |
| **消息总线广播** | **Spring Cloud Bus** 通过 RabbitMQ / Kafka 通知**所有实例**一起刷新（/actuator/bus-refresh） |
| **监听变化自动刷新** | ZooKeeper、Consul、Nacos 能**监听**配置变化，自动推送 |

### 其他配置中心（第 109—113 讲）

| 配置中心 | 认关键词 |
|---|---|
| **ZooKeeper** | 配置存在**节点**里（如 /config/应用名），**节点监听**触发刷新 |
| **Consul** | 配置存在 **KV** 存储里，**Watch** 检测变化后发布刷新事件 |
| **Nacos** | 阿里巴巴，发布配置后客户端**自动收到**；用 **Data ID** 和 Group 定位配置 |
| **Apollo** | **携程**开源；功能最全：**灰度发布、权限管理、审计、多环境多集群** |

> 💡 Nacos 的 Data ID 默认长这样：`应用名-环境.后缀`，如 `waiter-service-dev.yaml`。'''
        ]},
    ],
    'questions': [
        Q('cfg-p1', '开启 Spring Cloud Config 服务端的注解是？', ['@EnableConfigServer', '@EnableEurekaServer', '@EnableAdminServer', '@RefreshScope'], 0,
          ['对', '注册中心', 'Boot Admin', '刷新'], '@EnableConfigServer。', lesson=0),
        Q('cfg-p2', '配置改了以后，让 Bean 使用新值需要？', ['@RefreshScope', '调用 /actuator/refresh', '重新安装 JDK', '@Primary'], [0, 1],
          ['标记可刷新', '触发刷新', '无关', '无关'], '@RefreshScope + /actuator/refresh。', lesson=0),
        Q('cfg-p3', '携程开源、支持灰度发布和权限审计的配置中心是？', ['Apollo', 'Nacos', 'Consul', 'Config Server'], 0,
          ['对', '阿里', 'HashiCorp', 'Spring 官方'], 'Apollo。', lesson=1),

        Q('cfg-1', '配置中心和注册中心的区别是？', ['配置中心管「用什么配置」，注册中心管「服务在哪」', '两者完全一样', '配置中心管服务在哪', '注册中心管配置'], 0,
          ['对', '不同', '反了', '反了'], '一个管配置，一个管地址。'),
        Q('cfg-2', 'Spring Cloud Config Server 默认的配置存储后端是？', ['Git', 'MySQL', 'Redis', 'Excel'], 0,
          ['对', '可选（JDBC），不是默认', '不是', '不是'], 'Git。'),
        Q('cfg-3', 'Config Server 中，对 Git 来说，label 表示？', ['分支', '应用名', '环境', '端口'], 0,
          ['对（默认 master）', 'application', 'profile', '无关'], 'application 应用名，profile 环境，label 分支。'),
        Q('cfg-4', 'Config Server 中，profile 表示？', ['环境（如 dev、prod）', '应用名', 'Git 分支', '用户名'], 0,
          ['对', 'application', 'label', '无关'], 'profile = 环境。'),
        Q('cfg-5', '确定要读取哪份配置的三个要素是？', ['application', 'profile', 'label', 'port'], [0, 1, 2],
          ['应用名', '环境', '版本 / 分支', '无关'], '/{application}/{profile}/{label}。'),
        Q('cfg-6', 'Config 客户端的配置中心地址通常写在哪个文件里？', ['bootstrap.yml', 'application.yml', 'pom.xml', 'schema.sql'], 0,
          ['比 application 更早加载', '加载太晚，此时还没去拿远程配置', 'Maven', 'SQL'], 'bootstrap。'),
        Q('cfg-7', 'Config 客户端连不上配置中心时**立刻启动失败**，配置？', ['spring.cloud.config.fail-fast=true', 'spring.cloud.config.uri', 'spring.retry=true', 'management.endpoints.web.exposure.include=*'], 0,
          ['fail fast = 快速失败', '地址', '不对', 'Actuator'], 'fail-fast。'),
        Q('cfg-8', 'Config 客户端配置配置中心地址的配置项是？', ['spring.cloud.config.uri', 'spring.datasource.url', 'eureka.client.service-url.defaultZone', 'server.port'], 0,
          ['对', '数据库', '注册中心', '端口'], 'spring.cloud.config.uri。'),
        Q('cfg-9', '通过消息总线让**所有实例**一起刷新配置，用？', ['Spring Cloud Bus', 'Spring Cloud Stream', 'Feign', 'Ribbon'], 0,
          ['Bus = 总线', '消息编程模型（下个模块）', '服务调用', '负载均衡'], 'Bus 广播刷新。'),
        Q('cfg-10', '把远程配置接入 Spring Environment 的抽象是？', ['PropertySourceLocator', 'DiscoveryClient', 'HealthIndicator', 'RowMapper'], 0,
          ['对', '服务发现', '健康', 'JDBC'], 'PropertySourceLocator。'),
        Q('cfg-11', '下列哪些配置中心能**监听**配置变化并自动刷新？', ['ZooKeeper', 'Consul', 'Nacos', '只用 Git 的 Config Server（不配 Bus）'], [0, 1, 2],
          ['节点监听', 'Watch', '自动推送', '需要手动调 refresh 或配合 Bus'], '第 110 讲。'),
        Q('cfg-12', 'Consul 中配置存放在？', ['KV 存储', 'Git 仓库', 'MySQL', '临时节点'], 0,
          ['对', 'Config Server 的', '不是', 'ZooKeeper 的'], 'Consul KV。'),
        Q('cfg-13', 'Nacos 配置中心用什么定位一份配置？', ['Data ID 和 Group', 'application 和 label', 'KV 路径', 'Git 分支'], 0,
          ['对', 'Config Server 的', 'Consul 的', 'Config Server 的'], 'Data ID + Group。'),
        Q('cfg-14', 'Nacos 由哪家公司开源？', ['阿里巴巴', '携程', 'Netflix', 'HashiCorp'], 0,
          ['对', 'Apollo', 'Eureka、Hystrix', 'Consul'], 'Nacos 阿里，Apollo 携程。'),
        Q('cfg-15', 'Apollo 的特色功能有？', ['灰度发布', '权限管理', '审计', '多环境多集群'], [0, 1, 2, 3],
          ['有', '有', '有', '有'], '第 113 讲。'),
        Q('cfg-16', 'ZooKeeper 配置中心通过什么触发刷新？', ['节点监听', '定时邮件', '重启服务器', '手动改数据库'], 0,
          ['对', '不是', '不是', '不是'], 'ZooKeeper 节点监听。'),
        TF('cfg-17', '默认情况下，从配置中心拿到的远程配置优先于本地配置', True, '对', '错', '第 110 讲：优先级受版本和设置影响，默认远程优先。'),
    ],
}

CHEATSHEET = '''### 配置中心（第 107—113 讲）

- 配置中心管「用什么配置」，注册中心管「服务在哪」。
- Config Server：**@EnableConfigServer**，默认 **Git**，端口 8888；**application 应用名 / profile 环境 / label 分支**。
- 客户端：spring-cloud-starter-config，写在 **bootstrap.yml**，spring.cloud.config.uri，fail-fast，spring-retry 重试，discovery.enabled。
- 刷新：**@RefreshScope + POST /actuator/refresh**；Spring Cloud **Bus** 广播（/actuator/bus-refresh）；ZooKeeper / Consul / Nacos 监听自动刷新。
- PropertySourceLocator 接入远程配置，默认远程优先。
- ZooKeeper 节点监听；Consul KV + Watch；**Nacos（阿里）Data ID + Group**；**Apollo（携程）灰度、权限、审计、多环境**。
'''
