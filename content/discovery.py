# 模块：服务注册与发现（第 91—99 讲）。深度：认得出。
from qhelp import Q, TF

MODULE = {
    'id': 'discovery', 'title': '服务注册与发现：Eureka、ZooKeeper、Consul、Nacos、负载均衡、Feign', 'short': '注册与发现',
    'group': '第十二章 服务注册与发现', 'exam': '第 91—99 讲',
    'refs': [{'label': 'Spring Cloud Netflix 文档（Greenwich）', 'url': 'https://cloud.spring.io/spring-cloud-netflix/2.1.x/single/spring-cloud-netflix.html'}],
    'lessons': [
        {'title': '注册与发现，以及 Eureka', 'cards': [
'''### 一句话

服务多了以后，调用方需要知道「某个服务现在有哪些机器、地址是什么」。

- **服务注册**：服务启动时把自己的地址**登记**到注册中心；
- **服务发现**：调用方去注册中心**查**某个服务有哪些实例。

**DiscoveryClient** 是 Spring Cloud 定义的「服务发现」接口：按服务名拿到实例列表（getServices()、getInstances(服务名)）。

### Eureka（第 91、94 讲）

**Netflix 开源的注册中心。**

| 看到题目说…… | 就选 |
|---|---|
| 开启 Eureka 服务端 | **@EnableEurekaServer** |
| 开启服务发现客户端（通用） | **@EnableDiscoveryClient** |
| 客户端配置注册中心地址 | **eureka.client.service-url.defaultZone** |
| 单机的注册中心自己不要注册自己 | register-with-eureka=false、fetch-registry=false |

- 客户端定时发**心跳**续约（默认 30 秒），太久没心跳（默认 90 秒）会被剔除；
- Eureka 2.x 的开发已经**停止**。'''
        ]},
        {'title': '负载均衡和 Feign', 'cards': [
'''### 客户端负载均衡（第 92 讲）

一个服务有好几台机器，调用方**自己**决定这次调用哪一台，叫**客户端负载均衡**。

| 看到题目说…… | 就选 |
|---|---|
| 课程中用的客户端负载均衡组件（Netflix） | **Ribbon** |
| Ribbon 进入维护后，Spring 官方的替代品 | **Spring Cloud LoadBalancer** |
| 让 RestTemplate 能用**服务名**代替真实地址 | 在 RestTemplate 上贴 **@LoadBalanced** |

例子：网址写 `http://waiter-service/coffee`，加了 @LoadBalanced 后，会自动把 waiter-service 换成某台机器的真实地址。

### Feign：声明式的服务调用（第 93 讲）

**Feign = 只写一个接口，贴上注解，就能调用远程服务**，不用自己拼网址、发请求。

| 看到题目说…… | 就选 |
|---|---|
| 起步依赖 | **spring-cloud-starter-openfeign** |
| 开启 Feign | **@EnableFeignClients** |
| 声明一个远程服务的客户端接口 | **@FeignClient(name = "服务名")** |
| 超时设置 | feign.client.config.default.connect-timeout / read-timeout |

底层的 HTTP 库可以换成 Apache HttpClient 或 OkHttp。

> 📌 认准：**@LoadBalanced 让 RestTemplate 认服务名；@FeignClient 只写接口就能调。**'''
        ]},
        {'title': '其他注册中心：ZooKeeper、Consul、Nacos', 'cards': [
'''### 四个注册中心对比（第 95—99 讲，常考）

| 注册中心 | 出身 | 特点（认关键词） |
|---|---|---|
| **Eureka** | Netflix | **AP**（优先保证可用）；2.x 已停止开发 |
| **ZooKeeper** | Apache | **CP**（优先保证一致）；用**临时节点**登记服务；网络有问题时可能不可用，课程认为**不太适合做注册中心** |
| **Consul** | HashiCorp | 自带**健康检查**、**DNS 接口**、KV 存储、多数据中心 |
| **Nacos** | **阿里巴巴** | **服务发现 + 配置管理**二合一；有控制台（默认端口 8848） |

- CAP 里：C = 一致性，A = 可用性，P = 分区容错。（补充）
- 起步依赖都长一个样：spring-cloud-starter-**zookeeper**-discovery、spring-cloud-starter-**consul**-discovery、spring-cloud-starter-**alibaba-nacos**-discovery。
- Nacos 地址配置：**spring.cloud.nacos.discovery.server-addr**。

### 自己实现 DiscoveryClient（第 98 讲）

实现 DiscoveryClient 接口的方法（getServices、getInstances 等），比如从固定配置里读出服务列表；再适配给 Ribbon（实现 ServerList）。'''
        ]},
    ],
    'questions': [
        Q('disc-p1', '服务启动时把自己的地址登记到注册中心，叫？', ['服务注册', '服务发现', '负载均衡', '熔断'], 0,
          ['登记 → 注册', '查 → 发现', '选机器', '保护'], '注册是登记，发现是查。', lesson=0),
        Q('disc-p2', '让 RestTemplate 可以用服务名代替真实地址，贴？', ['@LoadBalanced', '@FeignClient', '@EnableDiscoveryClient', '@Primary'], 0,
          ['对', 'Feign 的', '开启发现', '主 Bean'], '@LoadBalanced。', lesson=1),
        Q('disc-p3', '阿里巴巴开源、同时支持服务发现和配置管理的是？', ['Nacos', 'Eureka', 'ZooKeeper', 'Consul'], 0,
          ['对', 'Netflix', 'Apache', 'HashiCorp'], 'Nacos 二合一。', lesson=2),

        Q('disc-1', 'Spring Cloud 中定义的、按服务名获取实例列表的接口是？', ['DiscoveryClient', 'RestTemplate', 'FeignClient', 'LoadBalancer'], 0,
          ['对', 'HTTP 客户端', '声明式客户端', '负载均衡'], 'DiscoveryClient.getInstances。'),
        Q('disc-2', '开启 Eureka 服务端的注解是？', ['@EnableEurekaServer', '@EnableDiscoveryClient', '@EnableFeignClients', '@EnableConfigServer'], 0,
          ['对', '客户端', 'Feign', '配置中心'], '@EnableEurekaServer。'),
        Q('disc-3', 'Eureka 客户端配置注册中心地址的配置项是？', ['eureka.client.service-url.defaultZone', 'spring.datasource.url', 'server.port', 'spring.cloud.nacos.discovery.server-addr'], 0,
          ['对', '数据库', '端口', 'Nacos 的'], 'defaultZone。'),
        Q('disc-4', 'Eureka 客户端通过什么告诉注册中心「我还活着」？', ['定时发送心跳', '发送邮件', '写数据库', '什么都不做'], 0,
          ['续约，默认 30 秒一次', '不是', '不是', '不是'], '心跳续约。'),
        Q('disc-5', '调用方自己决定调用哪台机器，这叫？', ['客户端负载均衡', '服务端负载均衡', '服务注册', '熔断'], 0,
          ['对', '那是 Nginx 等做的', '不是', '不是'], '客户端负载均衡。'),
        Q('disc-6', '课程中使用的 Netflix 客户端负载均衡组件是？', ['Ribbon', 'Hystrix', 'Eureka', 'Zuul'], 0,
          ['对', '熔断', '注册中心', '网关'], 'Ribbon。'),
        Q('disc-7', 'Ribbon 进入维护后，Spring 官方推出的替代品是？', ['Spring Cloud LoadBalancer', 'Hystrix', 'Feign', 'Zipkin'], 0,
          ['对', '熔断', '声明式调用', '追踪'], 'Spring Cloud LoadBalancer。'),
        Q('disc-8', '只写接口、贴上注解就能调用远程服务的是？', ['Feign', 'RestTemplate', 'WebClient', 'JdbcTemplate'], 0,
          ['声明式', '要自己拼网址', '要自己拼网址', '数据库'], 'Feign。'),
        Q('disc-9', '开启 Feign 的注解是？', ['@EnableFeignClients', '@FeignClient', '@EnableDiscoveryClient', '@LoadBalanced'], 0,
          ['开启', '声明单个客户端', '服务发现', '负载均衡'], '@EnableFeignClients + @FeignClient。'),
        Q('disc-10', '声明一个调用 waiter-service 的 Feign 客户端接口，贴？', ['@FeignClient(name = "waiter-service")', '@LoadBalanced', '@RestController', '@Service'], 0,
          ['对', 'RestTemplate 的', '服务端', '业务层'], '@FeignClient。'),
        Q('disc-11', 'Feign 的起步依赖是？', ['spring-cloud-starter-openfeign', 'spring-boot-starter-web', 'spring-cloud-starter-netflix-ribbon', 'feign-spring-boot-starter'], 0,
          ['对', 'Web', 'Ribbon', '命名不对'], 'openfeign。'),
        Q('disc-12', '优先保证**一致性**（CP）的注册中心是？', ['ZooKeeper', 'Eureka', 'Nacos 默认模式', 'Ribbon'], 0,
          ['对', 'AP', 'Nacos 默认 AP，也支持 CP', '不是注册中心'], 'Eureka AP，ZooKeeper CP。'),
        Q('disc-13', '优先保证**可用性**（AP）的注册中心是？', ['Eureka', 'ZooKeeper', 'MySQL', 'Redis'], 0,
          ['对', 'CP', '不是', '不是'], 'Eureka AP。'),
        Q('disc-14', '自带健康检查和 DNS 接口的注册中心是？', ['Consul', 'Eureka', 'ZooKeeper', 'Ribbon'], 0,
          ['HashiCorp 的', '不是', '不是', '不是'], 'Consul。'),
        Q('disc-15', 'ZooKeeper 用什么方式登记服务实例（服务下线时自动消失）？', ['临时节点', '永久文件', '数据库表', '环境变量'], 0,
          ['对', '不是', '不是', '不是'], '临时节点。'),
        Q('disc-16', 'Nacos 服务发现配置服务端地址的配置项是？', ['spring.cloud.nacos.discovery.server-addr', 'eureka.client.service-url.defaultZone', 'spring.cloud.consul.host', 'server.port'], 0,
          ['对', 'Eureka', 'Consul', '端口'], 'server-addr。'),
        Q('disc-17', 'Nacos 控制台默认端口是？', ['8848', '8080', '8761', '9411'], 0,
          ['对（珠峰高度）', 'Tomcat 默认', 'Eureka 常用', 'Zipkin'], '8848。', adv=True),
        TF('disc-18', '课程认为 ZooKeeper 非常适合做服务注册中心', False, '错', '对：它是 CP，网络分区时可能不可用，不太适合', '第 95 讲。'),
        TF('disc-19', 'Eureka 2.x 的开发已经停止', True, '对', '错', '组件维护状态。'),
        Q('disc-20', '自己实现一个 DiscoveryClient，需要实现哪些方法？', ['getServices()', 'getInstances()', 'description()', 'proceed()'], [0, 1, 2],
          ['要', '要', '要', 'AOP 的'], '第 98 讲。', adv=True),
    ],
}

CHEATSHEET = '''### 注册与发现（第 91—99 讲）

- 注册 = 登记，发现 = 查；**DiscoveryClient**（getServices、getInstances）。
- Eureka（Netflix，**AP**，2.x 停止）：@EnableEurekaServer；@EnableDiscoveryClient；defaultZone；心跳 30 秒、90 秒剔除。
- 客户端负载均衡：**Ribbon**（维护）→ **Spring Cloud LoadBalancer**；**@LoadBalanced** 让 RestTemplate 认服务名。
- **Feign**：spring-cloud-starter-openfeign，@EnableFeignClients，**@FeignClient(name=)**，可配超时、换 HttpClient / OkHttp。
- ZooKeeper（Apache，**CP**，临时节点，不太适合做注册中心）；Consul（HashiCorp，健康检查、DNS、KV）；**Nacos（阿里，发现 + 配置，8848）**，server-addr。
'''
