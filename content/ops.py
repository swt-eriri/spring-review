# 模块：运行中的 Spring Boot（第 75—85 讲）。深度：认得出。端点默认值按 Boot 2.1 补充。
from qhelp import Q, TF

MODULE = {
    'id': 'ops', 'title': '运行中的 Spring Boot：监控、容器、打包', 'short': 'Boot 运维',
    'group': '第十章 运行中的 Spring Boot', 'exam': '第 75—85 讲',
    'refs': [{'label': 'Spring Boot 2.1 文档 · Actuator 端点', 'url': 'https://docs.spring.io/spring-boot/docs/2.1.x/reference/html/production-ready-endpoints.html'}],
    'lessons': [
        {'title': 'Actuator 和健康检查', 'cards': [
'''### 一句话

**Actuator = 给程序装上「仪表盘」，通过一些网址查看程序的运行状态。**这些网址叫**端点**（Endpoint），默认都在 **/actuator** 下面。

### 常用端点：对号入座

| 端点 | 看什么 |
|---|---|
| **health** | 健康状态 |
| info | 程序信息 |
| **beans** | 容器里所有的 Bean |
| **conditions** | 自动配置的条件评估结果 |
| configprops | 所有 @ConfigurationProperties 配置 |
| **env** | 环境变量和配置 |
| **mappings** | 所有请求映射（网址 → 方法） |
| **metrics** | 各种指标 |
| loggers | 日志级别（还能在线修改） |
| threaddump / heapdump | 线程信息 / 内存快照 |
| **shutdown** | 关闭程序（**默认关闭**） |

> ⚠️ Spring Boot 2 通过 HTTP **默认只开放 health 和 info**。想全开：`management.endpoints.web.exposure.include=*`。也可以通过 JMX 访问。生产环境要注意**访问控制**。''',
'''### 健康检查（第 76 讲）

- 自定义健康检查：实现 **HealthIndicator** 接口，返回 **Health.up()** 或 **Health.down()**；
- 状态有四种：**UP**（正常）、**DOWN**（挂了）、**OUT_OF_SERVICE**（暂停服务）、**UNKNOWN**（未知）；
- 内置的健康检查：数据库（DataSourceHealthIndicator）、磁盘空间（DiskSpaceHealthIndicator）、Redis 等；
- 整体状态由所有检查**聚合**而来：只要有一个 DOWN，整体就是 DOWN；
- 显示详细信息：`management.endpoint.health.show-details`，可选 **never（默认）/ when-authorized / always**。'''
        ]},
        {'title': '指标、Spring Boot Admin、Web 容器', 'cards': [
'''### Micrometer：指标采集（第 77 讲）

**Micrometer 是指标采集的「统一接口」，号称「监控界的 SLF4J」**：写一套代码，就能把指标发到 Prometheus、Graphite、InfluxDB 等不同的监控系统。

| 指标类型 | 一句话 |
|---|---|
| **Counter** | 计数器，只增不减（如订单总数） |
| **Timer** | 计时器（如方法耗时） |
| **Gauge** | 当前值，可增可减（如在线人数） |
| DistributionSummary | 分布统计（如订单金额分布） |

- 用**标签（Tag）**区分维度；
- 自定义指标的入口：**MeterRegistry**；也可以实现 MeterBinder。

### Spring Boot Admin（第 78 讲）

**一个可视化的管理界面，把多个程序的 Actuator 信息集中展示。**（codecentric 公司开发，不是 Spring 官方的）

- 服务端：**@EnableAdminServer**；
- 客户端：配置 **spring.boot.admin.client.url** 指向服务端（或通过服务发现）；
- 需要开放 Actuator 端点，并注意加上访问认证。''',
'''### 定制 Web 容器（第 79 讲）

| 配置 | 作用 |
|---|---|
| **server.port** | 端口 |
| server.compression.enabled | 开启压缩 |
| server.tomcat.max-threads | Tomcat 最大线程数 |
| server.tomcat.max-connections | 最大连接数 |
| server.error.include-stacktrace | 错误页是否显示堆栈（生产环境别显示） |
| server.use-forward-headers | 在反向代理后面时，读取代理传来的头 |

用代码定制：实现 **WebServerFactoryCustomizer**。

### HTTPS 和 HTTP/2（第 80、81 讲）

- 生成证书：JDK 自带的 **keytool**；
- 配置 HTTPS：**server.ssl.key-store**（密钥库）、key-store-password、key-store-type（**PKCS12** 或 JKS）；
- 开启 HTTP/2：**server.http2.enabled=true**；浏览器上的 HTTP/2 **需要 HTTPS**；支持与否和 JDK、容器版本有关；
- 客户端可以用 **OkHttp** 访问 HTTP/2。'''
        ]},
        {'title': '命令行程序、可执行 jar、Docker', 'cards': [
'''### 命令行程序（第 82 讲）

不需要网页服务器时：`spring.main.web-application-type=none`（可选 **NONE / SERVLET / REACTIVE**）。

启动后执行一段任务：

| 接口 | 参数 |
|---|---|
| **CommandLineRunner** | 原始的字符串数组参数 |
| **ApplicationRunner** | 包装好的 **ApplicationArguments** |

- 多个 Runner 的顺序：**@Order**；
- 自定义退出码：**ExitCodeGenerator**。

### 可执行 jar 的秘密（第 83 讲）

**spring-boot-maven-plugin** 的 **repackage** 把程序重新打包成可执行 jar：

| jar 里的东西 | 作用 |
|---|---|
| **META-INF/MANIFEST.MF** | 清单：**Main-Class** 是启动器 **JarLauncher**，**Start-Class** 是你自己的 main 类 |
| org/springframework/boot/loader | 启动器代码 |
| **BOOT-INF/classes** | 你自己的代码 |
| **BOOT-INF/lib** | 依赖的 jar（嵌套在里面） |

> 📌 认准：**Main-Class = JarLauncher（启动器）；Start-Class = 你的程序入口。**运行仍需要 Java 环境；配置 executable 后还能在 Linux 上直接 `./xxx.jar` 运行。

### 打包成 Docker 镜像（第 84 讲）

写 **Dockerfile**：**FROM**（基础镜像，如 openjdk）→ **ADD / COPY**（把 jar 放进去）→ **ENTRYPOINT**（启动命令 `java -jar`）。课程还演示了用 Maven 插件（dockerfile-maven-plugin）构建。'''
        ]},
    ],
    'questions': [
        Q('ops-p1', 'Actuator 端点默认的访问前缀是？', ['/actuator', '/admin', '/manage', '/monitor'], 0,
          ['对', '不是', '不是', '不是'], '/actuator/health 等。', lesson=0),
        Q('ops-p2', '号称「监控界的 SLF4J」、提供统一指标接口的是？', ['Micrometer', 'Spring Boot Admin', 'Actuator', 'Druid'], 0,
          ['对', '可视化管理界面', '端点', '连接池'], 'Micrometer。', lesson=1),
        Q('ops-p3', '可执行 jar 的 MANIFEST.MF 中，Main-Class 指向的是？', ['JarLauncher', '你自己的 main 类', 'DispatcherServlet', 'Tomcat'], 0,
          ['启动器', '那是 Start-Class', '无关', '无关'], 'Main-Class 启动器，Start-Class 你的入口。', lesson=2),

        Q('ops-1', 'Spring Boot 2 中，通过 HTTP **默认开放**的 Actuator 端点是？', ['health', 'info', 'env', 'beans'], [0, 1],
          ['默认开放', '默认开放', '需配置开放', '需配置开放'], '默认只开 health 和 info。'),
        Q('ops-2', '开放所有 Actuator Web 端点的配置是？', ['management.endpoints.web.exposure.include=*', 'server.port=*', 'spring.actuator.all=true', 'management.health.enabled=true'], 0,
          ['对', '不对', '不存在', '不对'], 'exposure.include=*。'),
        Q('ops-3', '查看程序中所有请求映射（网址 → 方法）的端点是？', ['mappings', 'beans', 'env', 'metrics'], 0,
          ['对', '所有 Bean', '环境配置', '指标'], 'mappings。'),
        Q('ops-4', '查看自动配置条件评估结果的端点是？', ['conditions', 'configprops', 'beans', 'health'], 0,
          ['对', '配置属性', 'Bean', '健康'], 'conditions。'),
        Q('ops-5', '默认**不启用**、用于关闭程序的端点是？', ['shutdown', 'health', 'info', 'loggers'], 0,
          ['对', '默认开放', '默认开放', '日志'], 'shutdown 默认关闭。'),
        Q('ops-6', '可以查看并**在线修改日志级别**的端点是？', ['loggers', 'env', 'metrics', 'threaddump'], 0,
          ['对', '环境', '指标', '线程'], 'loggers。'),
        Q('ops-7', '自定义健康检查要实现的接口是？', ['HealthIndicator', 'HandlerInterceptor', 'CommandLineRunner', 'MeterBinder'], 0,
          ['对', '拦截器', '启动任务', '指标'], 'HealthIndicator。'),
        Q('ops-8', '健康检查的状态包括？', ['UP', 'DOWN', 'OUT_OF_SERVICE', 'UNKNOWN'], [0, 1, 2, 3],
          ['正常', '挂了', '暂停服务', '未知'], '四种状态。'),
        Q('ops-9', '`management.endpoint.health.show-details` 的默认值是？', ['never', 'always', 'when-authorized', 'true'], 0,
          ['默认不显示详情', '不是默认', '不是默认', '不是可选值'], 'never / when-authorized / always。'),
        Q('ops-10', 'Micrometer 中**只增不减**的计数指标是？', ['Counter', 'Gauge', 'Timer', 'DistributionSummary'], 0,
          ['计数器', '当前值，可增可减', '计时', '分布'], 'Counter。'),
        Q('ops-11', 'Micrometer 中表示**当前值、可增可减**（如在线人数）的指标是？', ['Gauge', 'Counter', 'Timer', 'Tag'], 0,
          ['仪表', '只增', '计时', '标签'], 'Gauge。'),
        Q('ops-12', 'Micrometer 中自定义指标的核心入口是？', ['MeterRegistry', 'HealthIndicator', 'DataSource', 'Environment'], 0,
          ['对', '健康', '数据源', '配置'], 'MeterRegistry。'),
        Q('ops-13', 'Spring Boot Admin 服务端开启的注解是？', ['@EnableAdminServer', '@EnableEurekaServer', '@EnableConfigServer', '@EnableCaching'], 0,
          ['对', '注册中心', '配置中心', '缓存'], '@EnableAdminServer。'),
        TF('ops-14', 'Spring Boot Admin 是 Spring 官方开发的项目', False, '错', '对：由 codecentric 开发', '第三方。'),
        Q('ops-15', '修改内嵌服务器端口的配置是？', ['server.port', 'spring.port', 'management.port', 'tomcat.port'], 0,
          ['对', '不存在', '那是管理端口相关', '不存在'], 'server.port。'),
        Q('ops-16', '用代码定制内嵌 Web 容器，实现？', ['WebServerFactoryCustomizer', 'WebMvcConfigurer', 'HealthIndicator', 'ApplicationRunner'], 0,
          ['对', 'MVC 配置', '健康', '启动任务'], 'WebServerFactoryCustomizer。'),
        Q('ops-17', '开启 HTTP/2 的配置是？', ['server.http2.enabled=true', 'server.ssl.enabled=true', 'spring.http2=true', 'server.compression.enabled=true'], 0,
          ['对', 'HTTPS', '不存在', '压缩'], 'server.http2.enabled。'),
        Q('ops-18', 'JDK 自带的、用来生成证书和密钥库的工具是？', ['keytool', 'javac', 'jar', 'jps'], 0,
          ['对', '编译', '打包', '看进程'], 'keytool。'),
        Q('ops-19', '让 Spring Boot 程序**不启动** Web 服务器的配置是？', ['spring.main.web-application-type=none', 'server.port=0', 'server.enabled=false', 'spring.web=false'], 0,
          ['对', '0 是随机端口', '不存在', '不存在'], 'NONE / SERVLET / REACTIVE。'),
        Q('ops-20', '程序启动后执行任务，参数是包装好的 ApplicationArguments 的接口是？', ['ApplicationRunner', 'CommandLineRunner', 'HealthIndicator', 'ExitCodeGenerator'], 0,
          ['对', '参数是原始字符串数组', '健康', '退出码'], 'ApplicationRunner 包装参数，CommandLineRunner 原始参数。'),
        Q('ops-21', '自定义程序退出码，用？', ['ExitCodeGenerator', 'CommandLineRunner', '@Order', 'HealthIndicator'], 0,
          ['对', '启动任务', '顺序', '健康'], 'ExitCodeGenerator。'),
        Q('ops-22', '可执行 jar 中，你自己写的代码放在？', ['BOOT-INF/classes', 'BOOT-INF/lib', 'META-INF', 'org/springframework/boot/loader'], 0,
          ['对', '依赖 jar', '清单', '启动器'], 'classes 自己的，lib 依赖。'),
        Q('ops-23', '把程序重新打包成可执行 jar 的是 spring-boot-maven-plugin 的哪个目标？', ['repackage', 'clean', 'compile', 'install'], 0,
          ['重新打包', '清理', '编译', '安装'], 'repackage。'),
        TF('ops-24', '可执行 jar 已经包含了 Java 运行环境，不需要安装 Java', False, '错', '对：运行仍需要 Java', '第 83 讲。'),
        Q('ops-25', 'Dockerfile 中指定基础镜像的指令是？', ['FROM', 'ENTRYPOINT', 'COPY', 'RUN'], 0,
          ['对', '启动命令', '复制文件', '构建时执行命令'], 'FROM → COPY/ADD → ENTRYPOINT。'),
    ],
}

CHEATSHEET = '''### Boot 运维（第 75—85 讲）

- Actuator 端点在 /actuator：health、info、beans、conditions、configprops、env、mappings、metrics、loggers（可改级别）、threaddump、heapdump、shutdown（默认关）。HTTP 默认只开 **health、info**；exposure.include=* 全开。
- HealthIndicator，Health.up() / down()；UP / DOWN / OUT_OF_SERVICE / UNKNOWN；有一个 DOWN 整体 DOWN；show-details 默认 never。
- **Micrometer = 监控界的 SLF4J**；Counter 只增，Gauge 当前值，Timer 计时；Tag 维度；MeterRegistry。
- Spring Boot Admin（codecentric）：@EnableAdminServer；spring.boot.admin.client.url。
- server.port、server.compression.enabled、server.tomcat.max-threads；WebServerFactoryCustomizer。HTTPS：keytool + server.ssl.key-store；HTTP/2：server.http2.enabled（浏览器需 HTTPS）。
- web-application-type=none；ApplicationRunner（ApplicationArguments）/ CommandLineRunner（原始参数）；@Order；ExitCodeGenerator。
- 可执行 jar：repackage；MANIFEST **Main-Class = JarLauncher，Start-Class = 你的入口**；BOOT-INF/classes、BOOT-INF/lib；仍需 Java。
- Dockerfile：FROM → COPY / ADD → ENTRYPOINT。
'''
