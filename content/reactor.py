# 模块：Reactor 与响应式数据访问（第 31—35 讲）。深度：认得出。
from qhelp import Q, TF

MODULE = {
    'id': 'reactor', 'title': 'Reactor 响应式编程：Mono、Flux 和响应式数据库访问', 'short': 'Reactor 响应式',
    'group': '第五章 数据访问进阶', 'exam': '第 31—35 讲',
    'refs': [{'label': 'Project Reactor 文档', 'url': 'https://projectreactor.io/docs/core/release/reference/'}],
    'lessons': [
        {'title': '响应式编程和 Mono / Flux', 'cards': [
'''### 一句话

**响应式编程 = 把数据看成一条「流」，数据来了就处理，不傻等。**Spring 用的响应式库叫 **Project Reactor**，它实现了 **Reactive Streams** 规范。

### 两个核心类型（必背）

| 类型 | 表示 | 记法 |
|---|---|---|
| **Mono** | **0 个或 1 个**结果 | Mono = 单（mono 是「单一」） |
| **Flux** | **0 个到多个**结果 | Flux = 流 |

例子：按 id 查一杯咖啡 → Mono；查所有咖啡 → Flux。

### Reactive Streams 的四个角色（认名字）

**Publisher**（发布者，发数据）、**Subscriber**（订阅者，收数据）、**Subscription**（订阅关系）、**Processor**（既发又收）。''',
'''### 三个重要概念

| 概念 | 一句话 |
|---|---|
| **订阅才执行** | 写好的流水线，**不调用 subscribe() 就什么都不会发生** |
| **背压（backpressure）** | **下游告诉上游自己一次能处理多少**，防止被数据淹没（通过 request(n)） |
| **线程调度** | 用 **Schedulers** 指定在哪种线程上运行；**publishOn** 影响它后面的操作，**subscribeOn** 影响数据源头 |

### 常用操作符（认名字）

| 操作符 | 作用 |
|---|---|
| **map** | 把每个元素变成另一个（一对一） |
| **flatMap** | 把每个元素变成**一个新的流**再合并 |
| **filter** | 过滤 |
| **onErrorResume / onErrorReturn** | 出错时换一个流 / 返回一个默认值 |
| **doOnNext** | 每来一个元素时顺便做点事（如打日志） |

> 📌 必背：**Mono 0..1，Flux 0..N；不订阅不执行；背压 = 下游控制速度。**'''
        ]},
        {'title': '响应式访问 Redis、MongoDB 和关系型数据库', 'cards': [
'''### 对号入座（第 33—35 讲）

| 看到题目说…… | 就选 |
|---|---|
| 响应式操作 Redis 的模板 | **ReactiveRedisTemplate**（字符串版 ReactiveStringRedisTemplate） |
| 响应式访问 Redis 需要的客户端 | **Lettuce**（Jedis **不支持**响应式） |
| 响应式操作 MongoDB 的模板 | **ReactiveMongoTemplate** |
| 响应式访问**关系型数据库**的规范 | **R2DBC** |
| R2DBC 中的连接工厂 / 操作数据库的客户端 | **ConnectionFactory / DatabaseClient** |

- 记法：普通版前面加 **Reactive** 就是响应式版。
- **R2DBC** = Reactive Relational Database Connectivity（响应式关系数据库连接）。课程录制时它还在**孵化阶段**，支持的数据库驱动不多。
- 传统 JDBC 是**阻塞**的，所以响应式访问关系数据库需要 R2DBC。'''
        ]},
    ],
    'questions': [
        Q('reactor-p1', 'Reactor 中表示 **0 个或 1 个**结果的类型是？', ['Mono', 'Flux', 'List', 'Optional'], 0,
          ['对', 'Flux 是 0 到多个', '普通 Java 集合', '普通 Java 类型'], 'Mono 0..1，Flux 0..N。', lesson=0),
        Q('reactor-p2', '下游告诉上游「我一次能处理多少」的机制叫？', ['背压', '缓存', '事务', '熔断'], 0,
          ['backpressure', '无关', '无关', '无关'], '背压 = 下游控制速度。', lesson=0),
        Q('reactor-p3', '响应式访问**关系型数据库**的规范是？', ['R2DBC', 'JDBC', 'JPA', 'MyBatis'], 0,
          ['对', 'JDBC 是阻塞的', '不是响应式', '不是响应式'], 'R2DBC。', lesson=1),

        Q('reactor-1', 'Reactor 中表示 **0 到多个**结果的类型是？', ['Flux', 'Mono', 'Future', 'Optional'], 0,
          ['Flux = 流', '0..1', '普通 Java', '普通 Java'], 'Flux。'),
        Q('reactor-2', 'Project Reactor 实现的规范是？', ['Reactive Streams', 'JPA', 'Servlet', 'JDBC'], 0,
          ['对', '持久化规范', 'Web 规范', '数据库连接规范'], 'Reactive Streams。'),
        Q('reactor-3', 'Reactive Streams 中的角色包括？', ['Publisher', 'Subscriber', 'Subscription', 'Repository'], [0, 1, 2],
          ['发布者', '订阅者', '订阅关系', 'Spring Data 的'], '还有 Processor。'),
        TF('reactor-4', '在 Reactor 中，定义好流之后，即使不订阅也会立即执行', False, '错', '对：不订阅什么都不会发生', '订阅才执行。'),
        Q('reactor-5', '把每个元素变成**一个新的流**再合并起来的操作符是？', ['flatMap', 'map', 'filter', 'doOnNext'], 0,
          ['对', 'map 是一对一转换', '过滤', '顺便做点事'], 'map 一对一，flatMap 变成流再合并。'),
        Q('reactor-6', '把每个元素一对一地转换成另一个值的操作符是？', ['map', 'flatMap', 'filter', 'subscribe'], 0,
          ['对', '转换成流', '过滤', '订阅'], 'map。'),
        Q('reactor-7', '出错时返回一个**默认值**的操作符是？', ['onErrorReturn', 'onErrorResume', 'map', 'filter'], 0,
          ['Return = 返回一个值', 'Resume = 换一个流继续', '转换', '过滤'], 'Return 返回值，Resume 换流。'),
        Q('reactor-8', 'Reactor 中用于指定运行线程的工具是？', ['Schedulers', 'DataSource', 'Executor 注解', 'RestTemplate'], 0,
          ['对', '数据源', '不是', '无关'], 'Schedulers。'),
        Q('reactor-9', '影响它**后面**操作所在线程的是？', ['publishOn', 'subscribeOn', 'map', 'filter'], 0,
          ['对', 'subscribeOn 影响数据源头', '不切线程', '不切线程'], 'publishOn 管后面，subscribeOn 管源头。'),
        Q('reactor-10', '响应式访问 Redis 必须使用哪个客户端？', ['Lettuce', 'Jedis', 'Druid', 'HikariCP'], 0,
          ['对', 'Jedis 不支持响应式', '连接池', '连接池'], 'Lettuce 支持响应式。'),
        Q('reactor-11', '响应式操作 MongoDB 的模板类是？', ['ReactiveMongoTemplate', 'MongoTemplate', 'ReactiveRedisTemplate', 'JdbcTemplate'], 0,
          ['Reactive + MongoTemplate', '普通版', 'Redis 的', 'JDBC'], '前面加 Reactive。'),
        Q('reactor-12', '响应式操作 Redis 的模板类是？', ['ReactiveRedisTemplate', 'RedisTemplate', 'ReactiveMongoTemplate', 'WebClient'], 0,
          ['对', '普通版', 'MongoDB', '调网络接口'], '前面加 Reactive。'),
        Q('reactor-13', 'R2DBC 中，用来操作数据库的客户端类是？', ['DatabaseClient', 'JdbcTemplate', 'MongoTemplate', 'RestTemplate'], 0,
          ['对', 'JDBC', 'MongoDB', '网络'], 'ConnectionFactory + DatabaseClient。'),
        TF('reactor-14', '课程录制时，Spring Data R2DBC 还处于孵化阶段，支持的驱动有限', True, '对', '错', '第 35 讲。'),
        Q('reactor-15', '按 id 查一杯咖啡（最多一个结果），响应式返回类型应该是？', ['Mono', 'Flux', 'List', 'void'], 0,
          ['0..1', '多个', '不是响应式', '没有返回值'], '一个 → Mono。'),
    ],
}

CHEATSHEET = '''### Reactor 响应式（第 31—35 讲）

- Reactor 实现 Reactive Streams（Publisher / Subscriber / Subscription / Processor）。
- **Mono 0..1，Flux 0..N**；**不订阅不执行**；**背压 = 下游用 request(n) 控制速度**。
- map 一对一，flatMap 变流再合并，filter 过滤，onErrorReturn 默认值 / onErrorResume 换流，doOnNext 顺便做事。
- Schedulers 指定线程；publishOn 管后面，subscribeOn 管源头。
- ReactiveRedisTemplate（只能用 Lettuce），ReactiveMongoTemplate，**R2DBC**（ConnectionFactory、DatabaseClient，当时在孵化）。
'''
