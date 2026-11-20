# 模块：Spring Cloud Stream 与链路追踪（第 114—122 讲）。深度：认得出。按课程所用的早期注解式编程模型。
from qhelp import Q, TF

MODULE = {
    'id': 'stream', 'title': '消息与链路追踪：Spring Cloud Stream、Sleuth、Zipkin', 'short': '消息与追踪',
    'group': '第十五、十六章 Stream 与链路追踪', 'exam': '第 114—122 讲',
    'refs': [{'label': 'Spring Cloud Sleuth 文档（Greenwich）', 'url': 'https://cloud.spring.io/spring-cloud-sleuth/2.1.x/single/spring-cloud-sleuth.html'}],
    'lessons': [
        {'title': 'Spring Cloud Stream：用统一的方式收发消息', 'cards': [
'''### 一句话

服务之间除了直接调用，还可以**发消息**：A 把消息放进消息中间件（如 RabbitMQ、Kafka），B 自己去取。好处是**解耦**，A 不用等 B。

**Spring Cloud Stream 让你用同一套写法收发消息，底下换 RabbitMQ 还是 Kafka 都不用改业务代码。**

### 两个核心概念（必背）

| 概念 | 一句话 |
|---|---|
| **Binder** | 连接**具体消息中间件**的「适配器」（有 RabbitMQ Binder、Kafka Binder） |
| **Binding** | 把程序里的**输入 / 输出通道**和中间件里的**目的地**绑在一起 |

> 📌 认准：**Binder 对接中间件；Binding 绑通道和目的地。**

### 课程用的早期注解写法（认名字）

| 看到题目说…… | 就选 |
|---|---|
| 开启绑定 | **@EnableBinding** |
| 监听消息 | **@StreamListener** |
| 定义输入 / 输出通道 | **@Input / @Output** |
| 内置的只发 / 只收 / 又收又发接口 | **Source / Sink / Processor** |
| 处理完把结果发到另一个通道 | **@SendTo** |''',
'''### 消费组（必背）

`spring.cloud.stream.bindings.<通道名>.group` 指定消费组：

- **不同的组**：每个组都会收到**一份**消息；
- **同一个组里**：一条消息**只会被其中一个实例**处理（大家分摊）。

例子：咖啡师服务部署了 3 台，放在同一个组里，一个订单只会被一台机器做，不会做三杯。

### RabbitMQ 和 Kafka（第 115、116 讲）

| 中间件 | 认关键词 |
|---|---|
| **RabbitMQ** | **交换机（Exchange）**、队列、**路由键（routing key）**、绑定 |
| **Kafka** | **主题（Topic）**、**broker**（服务节点）、消费组；当时版本需要 ZooKeeper |

### SpringBucks 进度（第 115—117 讲）

- Waiter（服务员）发「新订单」消息 → Barista（咖啡师）收到后做咖啡 → 做好后再发消息通知；
- 用消息**通知**代替**轮询**（不用一遍遍去问「好了没」）；
- 用 RabbitMQ 的**路由键**把订单完成消息发给对应的顾客实例；
- 第 116 讲还用到了**定时任务**（@Scheduled）和 **Spring 事件**（ApplicationEvent / @EventListener）来解耦业务。'''
        ]},
        {'title': '链路追踪：Dapper、Sleuth、Zipkin', 'cards': [
'''### 一句话

一个请求可能经过好几个服务，出了问题很难知道卡在哪。**链路追踪 = 给每个请求编号，记录它经过了哪些服务、每一步花了多久。**

### 两个核心概念（来自 Google 的 Dapper 论文，必背）

| 概念 | 一句话 | 编号 |
|---|---|---|
| **Trace** | **一次完整的请求**（从头到尾） | **Trace ID**，整条链路共用一个 |
| **Span** | 链路中的**一个工作单元**（如一次服务调用） | **Span ID**，每一步一个 |

- 一个 Trace 由多个 Span 组成，Span 之间有父子关系；
- **采样**：不是每个请求都记录，只记录一部分，减少开销。

### 四个时间点（了解）

**cs**（客户端发出）→ **sr**（服务端收到）→ **ss**（服务端发出）→ **cr**（客户端收到）。''',
'''### Sleuth + Zipkin（第 119、120 讲）

| 看到题目说…… | 就选 |
|---|---|
| Spring Cloud 的链路追踪组件 | **Spring Cloud Sleuth** |
| Sleuth 底层使用的追踪库 | **Brave** |
| 收集并**可视化展示**调用链的系统 | **Zipkin**（默认端口 9411） |
| Zipkin 地址配置 | **spring.zipkin.base-url** |
| 采样比例配置 | **spring.sleuth.sampler.probability**（默认 0.1，即 10%） |

- 加了 Sleuth 后，**日志里会自动带上 Trace ID 和 Span ID**，格式类似 `[应用名,TraceID,SpanID,是否上报]`，方便按编号搜索跨服务的日志；
- 追踪数据可以通过 **HTTP** 直接发给 Zipkin，也可以通过 **RabbitMQ / Kafka** 消息发送（spring.zipkin.sender.type）；
- 消息收发（如 RabbitMQ）的链路也能追踪，追踪信息随消息一起传递。

### 除了链路还要治理什么（第 121、122 讲）

容量规划、依赖关系、配置变更、发布审计、代码质量、监控告警……**链路追踪只是观察系统的一部分**。生产环境的采样比例要在开销和排查需要之间权衡。第 122 讲用 **Docker Compose** 把所有服务一起编排启动。

> 📌 必背：**Trace = 整个请求，Span = 其中一步；Sleuth 采集，Zipkin 展示；日志带 TraceID。**'''
        ]},
    ],
    'questions': [
        Q('stream-p1', 'Spring Cloud Stream 中，负责对接具体消息中间件的是？', ['Binder', 'Binding', 'Span', 'Trace'], 0,
          ['适配器', '绑定通道和目的地', '追踪', '追踪'], 'Binder 对接中间件。', lesson=0),
        Q('stream-p2', '同一个消费组里有 3 个实例，一条消息会被处理几次？', ['1 次', '3 次', '0 次', '随机'], 0,
          ['组内只有一个实例处理', '不同组才会各收一份', '会处理', '确定的'], '组内分摊。', lesson=0),
        Q('stream-p3', '链路追踪中，表示**一次完整请求**的是？', ['Trace', 'Span', 'Binder', 'Topic'], 0,
          ['对', '一个工作单元', '消息', 'Kafka'], 'Trace 整条，Span 一步。', lesson=1),

        Q('stream-1', 'Spring Cloud Stream 的作用是？', ['用统一的方式收发消息，屏蔽不同中间件的差异', '做链路追踪', '做服务注册', '做页面渲染'], 0,
          ['对', 'Sleuth', 'Eureka 等', '无关'], 'Stream = 统一的消息编程模型。'),
        Q('stream-2', 'Spring Cloud Stream 中，把程序的通道和中间件目的地绑在一起的是？', ['Binding', 'Binder', 'Exchange', 'Span'], 0,
          ['对', '对接中间件', 'RabbitMQ 的', '追踪'], 'Binding 绑定。'),
        Q('stream-3', '早期注解式写法中，开启绑定的注解是？', ['@EnableBinding', '@StreamListener', '@EnableKafka', '@EnableCaching'], 0,
          ['对', '监听消息', '不是', '缓存'], '@EnableBinding + @StreamListener。'),
        Q('stream-4', '早期注解式写法中，监听并处理消息的注解是？', ['@StreamListener', '@EnableBinding', '@Output', '@SendTo'], 0,
          ['对', '开启绑定', '输出通道', '发到另一个通道'], '@StreamListener。'),
        Q('stream-5', 'Spring Cloud Stream 内置的「只接收消息」的接口是？', ['Sink', 'Source', 'Processor', 'Binder'], 0,
          ['Sink = 水槽，只进', 'Source = 源头，只出', '又收又发', '适配器'], 'Source 发，Sink 收，Processor 都有。'),
        Q('stream-6', '设置消费组的配置项是？', ['spring.cloud.stream.bindings.<通道名>.group', 'spring.kafka.topic', 'spring.rabbitmq.host', 'spring.cloud.stream.binder'], 0,
          ['对', '不对', 'RabbitMQ 地址', '不对'], 'bindings.<通道名>.group。'),
        Q('stream-7', '两个**不同的**消费组都订阅了同一个目的地，一条消息会怎样？', ['每个组各收到一份', '只有一个组收到', '两个组都收不到', '随机'], 0,
          ['对', '组内才分摊', '会收到', '确定的'], '不同组各一份，同组分摊。'),
        Q('stream-8', '下列属于 RabbitMQ 的概念是？', ['交换机（Exchange）', '路由键（routing key）', '队列', '哈希槽'], [0, 1, 2],
          ['是', '是', '是', 'Redis Cluster 的'], 'RabbitMQ：交换机、队列、路由键。'),
        Q('stream-9', 'Kafka 中消息按什么分类？', ['主题（Topic）', '交换机', '哈希槽', 'Span'], 0,
          ['对', 'RabbitMQ', 'Redis', '追踪'], 'Kafka Topic。'),
        Q('stream-10', 'SpringBucks 中用消息通知代替了什么？', ['轮询', '数据库', '缓存', '事务'], 0,
          ['不用一遍遍去问', '不是', '不是', '不是'], '第 117 讲。'),
        Q('stream-11', '链路追踪的 Trace 和 Span 概念来自哪篇论文？', ['Google Dapper', 'Amazon Dynamo', 'Google MapReduce', 'Netflix Hystrix'], 0,
          ['对', '数据库', '大数据计算', '不是论文'], 'Dapper。'),
        Q('stream-12', '链路追踪中，表示链路里**一个工作单元**的是？', ['Span', 'Trace', 'Topic', 'Binder'], 0,
          ['对', '整条链路', 'Kafka', 'Stream'], 'Span。'),
        Q('stream-13', '只记录一部分请求的追踪数据以减少开销，叫？', ['采样', '熔断', '缓存', '限流'], 0,
          ['对', '不是', '不是', '不是'], '采样。'),
        Q('stream-14', 'Spring Cloud 的链路追踪组件是？', ['Spring Cloud Sleuth', 'Spring Cloud Stream', 'Spring Cloud Config', 'Spring Cloud Bus'], 0,
          ['Sleuth = 侦探', '消息', '配置', '总线'], 'Sleuth 采集。'),
        Q('stream-15', '收集追踪数据并可视化展示调用链的系统是？', ['Zipkin', 'Turbine', 'Spring Boot Admin', 'Eureka'], 0,
          ['对（端口 9411）', 'Hystrix 聚合', 'Actuator 管理界面', '注册中心'], 'Zipkin 展示。'),
        Q('stream-16', 'Sleuth 底层使用的追踪库是？', ['Brave', 'Hystrix', 'Ribbon', 'Lettuce'], 0,
          ['对', '熔断', '负载均衡', 'Redis 客户端'], 'Brave。'),
        Q('stream-17', '加了 Sleuth 后，日志里会自动带上？', ['Trace ID', 'Span ID', '数据库密码', '用户手机号'], [0, 1],
          ['是', '是', '不会', '不会'], '方便按编号查跨服务日志。'),
        Q('stream-18', 'Sleuth 设置采样比例的配置是？', ['spring.sleuth.sampler.probability', 'spring.zipkin.base-url', 'spring.sleuth.enabled', 'management.metrics'], 0,
          ['对（默认 0.1）', 'Zipkin 地址', '开关', '指标'], 'probability = 概率。'),
        Q('stream-19', 'Sleuth 把追踪数据发送给 Zipkin 的方式有？', ['HTTP', 'RabbitMQ', 'Kafka', '发邮件'], [0, 1, 2],
          ['可以', '可以', '可以', '不可以'], 'spring.zipkin.sender.type。'),
        TF('stream-20', '链路追踪就是服务治理的全部', False, '错', '对：还有容量、依赖、变更、审计、监控等', '第 121 讲。'),
        Q('stream-21', '第 122 讲中，用什么把咖啡店的所有服务和依赖一起编排启动？', ['Docker Compose', 'Maven', 'Spring Initializr', 'Turbine'], 0,
          ['对', '构建工具', '生成工程', 'Hystrix 聚合'], 'Docker Compose。'),
    ],
}

CHEATSHEET = '''### 消息与追踪（第 114—122 讲）

- Stream 统一收发消息；**Binder 对接中间件，Binding 绑通道和目的地**；@EnableBinding、@StreamListener、@Input / @Output、Source 发 / Sink 收 / Processor、@SendTo。
- **消费组**：不同组各收一份；同组只有一个实例处理（bindings.<通道>.group）。
- RabbitMQ：交换机、队列、路由键；Kafka：Topic、broker、消费组。消息通知代替轮询；@Scheduled、Spring 事件解耦。
- Dapper：**Trace = 一次完整请求（Trace ID），Span = 一个工作单元（Span ID）**；采样；cs / sr / ss / cr。
- **Sleuth 采集（底层 Brave），Zipkin 展示（9411）**；spring.zipkin.base-url；spring.sleuth.sampler.probability 默认 0.1；日志带 TraceID / SpanID；HTTP 或 RabbitMQ / Kafka 上报；消息链路也能追踪。
- 治理不只链路：容量、依赖、变更、审计、监控；Docker Compose 编排。
'''
