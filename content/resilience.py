# 模块：服务熔断与限流（第 100—106 讲）。深度：认得出。默认值按 Resilience4j 0.13 / Hystrix 1.5 补充。
from qhelp import Q, TF

MODULE = {
    'id': 'resilience', 'title': '熔断与限流：断路器、Hystrix、Resilience4j', 'short': '熔断与限流',
    'group': '第十三章 服务熔断', 'exam': '第 100—106 讲',
    'refs': [{'label': 'Resilience4j 文档', 'url': 'https://resilience4j.readme.io/docs'}],
    'lessons': [
        {'title': '断路器是什么', 'cards': [
'''### 一句话

下游服务挂了，如果还一直去调它，调用方的线程会被卡住，最后**一个挂掉拖垮一片**（雪崩）。**断路器就像家里的保险丝：失败太多就先「断开」，不再调用，直接返回一个备用结果。**

### 断路器的三种状态（必背）

| 状态 | 意思 |
|---|---|
| **关闭（Closed）** | 正常调用，同时统计失败情况 |
| **打开（Open）** | 失败太多，**直接拒绝调用**，返回备用结果（降级） |
| **半开（Half-Open）** | 过一段时间后，**放少量请求试探**：成功就关闭，失败就重新打开 |

> 📌 记法：**电路「关闭」时电流通过 = 正常调用；「打开」= 断了。**这和平时说的「开 / 关」正好相反，最容易记错。

- **降级（fallback）**：调用失败或被拒绝时，返回一个备用结果（如默认值、缓存的数据）。'''
        ]},
        {'title': 'Hystrix 和熔断监控', 'cards': [
'''### Hystrix（第 101 讲）

**Netflix 开源的断路器**，课程用它做演示。**现在已进入维护状态，不再开发新功能。**

| 看到题目说…… | 就选 |
|---|---|
| 开启断路器 | **@EnableCircuitBreaker**（或 @EnableHystrix） |
| 给一个方法加上熔断保护 | **@HystrixCommand** |
| 指定失败时的备用方法 | **@HystrixCommand(fallbackMethod = "...")** |
| 两种隔离方式 | **线程池隔离**（THREAD）和**信号量隔离**（SEMAPHORE） |
| 和 Feign 一起用 | **feign.hystrix.enabled=true**，在 @FeignClient 里指定 **fallback** |

### 观察熔断（第 102 讲）

| 看到题目说…… | 就选 |
|---|---|
| Hystrix 的可视化仪表盘 | **Hystrix Dashboard**（@EnableHystrixDashboard） |
| 仪表盘的数据来源端点 | **/actuator/hystrix.stream** |
| **聚合**多个实例的熔断数据 | **Turbine** |'''
        ]},
        {'title': 'Resilience4j：断路器、Bulkhead、RateLimiter', 'cards': [
'''### Resilience4j（第 103 讲）

**一个轻量级的容错库，受 Hystrix 启发，基于 Java 8 函数式编程。**按模块引入，用哪个引哪个：

| 模块 | 作用 |
|---|---|
| **CircuitBreaker** | 断路器 |
| **Bulkhead** | 限制**同时**进行的调用数量 |
| **RateLimiter** | 限制**一段时间内**的调用次数 |
| Retry | 重试 |
| TimeLimiter | 超时控制 |
| Cache | 缓存 |

断路器常用配置：**failureRateThreshold**（失败率阈值，默认 50%）、**waitDurationInOpenState**（打开状态保持多久后转半开）、统计窗口大小。

可以用注解（如 **@CircuitBreaker(name = "...")**）或编程方式接入，还能导出指标给 Micrometer。''',
'''### 三种保护手段：最容易混（必背，第 104—106 讲）

| 手段 | 管什么 | 打个比方 |
|---|---|---|
| **断路器 CircuitBreaker** | 根据**失败率**，暂停调用并试探恢复 | 保险丝 |
| **Bulkhead（舱壁 / 并发隔离）** | 限制**同时**在执行的调用数 | 船的隔水舱，一个舱进水不沉全船 |
| **RateLimiter（限流）** | 限制**单位时间内**的调用次数 | 每分钟只放 100 人进门 |

- Bulkhead 配置：**maxConcurrentCalls**（最大并发数）、maxWaitTime（排队最多等多久）；满了抛 BulkheadFullException；
- RateLimiter 配置：**limitForPeriod**（每个周期允许几次）、**limitRefreshPeriod**（周期多长）、timeoutDuration（等许可最多多久）；超了抛 RequestNotPermitted。

> 📌 认准：**看失败率 → 断路器；看同时有几个 → Bulkhead；看每秒（每段时间）几次 → RateLimiter。**三者可以一起用。'''
        ]},
    ],
    'questions': [
        Q('res-p1', '断路器处于哪个状态时，会**直接拒绝调用**？', ['打开（Open）', '关闭（Closed）', '半开（Half-Open）', '任何状态都不拒绝'], 0,
          ['对', '关闭 = 正常调用', '半开放少量请求试探', '会拒绝'], '打开 = 断了。', lesson=0),
        Q('res-p2', '指定 Hystrix 失败时的备用方法，用？', ['@HystrixCommand(fallbackMethod = "...")', '@EnableCircuitBreaker', '@FeignClient', '@Cacheable'], 0,
          ['对', '开启断路器', 'Feign', '缓存'], 'fallbackMethod。', lesson=1),
        Q('res-p3', '限制**同时**进行的调用数量的是？', ['Bulkhead', 'RateLimiter', 'CircuitBreaker', 'Retry'], 0,
          ['舱壁', '单位时间次数', '失败率', '重试'], '同时 → Bulkhead。', lesson=2),

        Q('res-1', '断路器的三种状态是？', ['关闭', '打开', '半开', '暂停'], [0, 1, 2],
          ['是', '是', '是', '不是'], 'Closed / Open / Half-Open。'),
        Q('res-2', '断路器处于**关闭（Closed）**状态时？', ['正常调用，并统计失败情况', '拒绝所有调用', '只放少量请求', '程序关闭'], 0,
          ['电路接通 = 正常', '那是打开', '那是半开', '无关'], '最容易记反。'),
        Q('res-3', '断路器的**半开（Half-Open）**状态的作用是？', ['放少量请求试探下游是否恢复', '拒绝所有请求', '正常处理所有请求', '重启下游服务'], 0,
          ['对', '那是打开', '那是关闭', '无关'], '成功就关闭，失败就重新打开。'),
        Q('res-4', '调用失败时返回一个备用结果，叫？', ['降级（fallback）', '回滚', '重试', '注册'], 0,
          ['对', '事务', '再试一次', '无关'], 'fallback。'),
        Q('res-5', '断路器主要防止什么问题？', ['一个服务故障拖垮整条调用链（雪崩）', 'SQL 注入', '数据重复', '页面乱码'], 0,
          ['对', '无关', '无关', '无关'], '限制故障扩散。'),
        Q('res-6', 'Hystrix 由哪家公司开源？', ['Netflix', '阿里巴巴', 'HashiCorp', 'Pivotal'], 0,
          ['对', 'Nacos、Druid', 'Consul', 'Spring 的公司'], 'Netflix 全家：Eureka、Ribbon、Hystrix、Zuul。'),
        Q('res-7', 'Hystrix 的两种隔离方式是？', ['线程池隔离', '信号量隔离', '数据库隔离', '进程隔离'], [0, 1],
          ['THREAD', 'SEMAPHORE', '不是', '不是'], '线程池 / 信号量。'),
        Q('res-8', 'Feign 中启用 Hystrix 的配置是？', ['feign.hystrix.enabled=true', 'hystrix.enabled=true', 'feign.enabled=true', 'spring.hystrix=true'], 0,
          ['对', '不对', '不对', '不对'], '并在 @FeignClient 里指定 fallback。'),
        Q('res-9', '聚合多个实例的 Hystrix 熔断数据的工具是？', ['Turbine', 'Hystrix Dashboard', 'Zipkin', 'Spring Boot Admin'], 0,
          ['聚合', '单个展示', '链路追踪', 'Actuator 管理界面'], 'Turbine 聚合。'),
        Q('res-10', 'Hystrix Dashboard 读取数据的端点是？', ['/actuator/hystrix.stream', '/actuator/health', '/actuator/metrics', '/actuator/env'], 0,
          ['对', '健康', '指标', '环境'], 'hystrix.stream。'),
        TF('res-11', 'Hystrix 目前已进入维护状态，不再开发新功能', True, '对', '错', '课程推荐了 Resilience4j。'),
        Q('res-12', '关于 Resilience4j，说法正确的是？', ['轻量级，受 Hystrix 启发，基于 Java 8 函数式', '是 Netflix 的主力产品', '只能做断路器', '必须引入全部模块'], 0,
          ['对', '不是 Netflix 的', '还有 Bulkhead、RateLimiter、Retry 等', '按需引入'], 'Resilience4j。'),
        Q('res-13', '限制**单位时间内**调用次数的是？', ['RateLimiter', 'Bulkhead', 'CircuitBreaker', 'TimeLimiter'], 0,
          ['限流', '同时并发数', '失败率', '超时'], '每段时间几次 → RateLimiter。'),
        Q('res-14', '根据**失败率**决定是否暂停调用的是？', ['CircuitBreaker', 'Bulkhead', 'RateLimiter', 'Cache'], 0,
          ['断路器', '并发', '频率', '缓存'], '失败率 → 断路器。'),
        Q('res-15', 'Resilience4j 断路器中，设置失败率阈值的配置是？', ['failureRateThreshold', 'maxConcurrentCalls', 'limitForPeriod', 'limitRefreshPeriod'], 0,
          ['failure rate = 失败率', 'Bulkhead 的', 'RateLimiter 的', 'RateLimiter 的'], 'failureRateThreshold，默认 50%。'),
        Q('res-16', 'Bulkhead 中设置最大并发调用数的配置是？', ['maxConcurrentCalls', 'limitForPeriod', 'failureRateThreshold', 'waitDurationInOpenState'], 0,
          ['concurrent = 同时', '限流', '断路器', '断路器'], 'maxConcurrentCalls。'),
        Q('res-17', 'RateLimiter 中设置每个周期允许几次调用的配置是？', ['limitForPeriod', 'limitRefreshPeriod', 'maxConcurrentCalls', 'timeoutDuration'], 0,
          ['每周期限额', '周期多长', 'Bulkhead', '等多久'], 'limitForPeriod 次数，limitRefreshPeriod 周期。'),
        Q('res-18', '断路器打开后多久转为半开，在 Resilience4j 中由哪个配置决定？', ['waitDurationInOpenState', 'failureRateThreshold', 'maxConcurrentCalls', 'limitForPeriod'], 0,
          ['在打开状态等待多久', '失败率', '并发', '限流'], 'waitDurationInOpenState。'),
        Q('res-19', 'Bulkhead 满了以后抛出的异常是？', ['BulkheadFullException', 'RequestNotPermitted', 'DuplicateKeyException', 'TimeoutException'], 0,
          ['Full = 满了', 'RateLimiter 的', '数据库', '不是'], '名字就是意思。', adv=True),
        TF('res-20', '断路器、Bulkhead、RateLimiter 解决的问题不同，可以配合使用', True, '对', '错', '第 106 讲。'),
    ],
}

CHEATSHEET = '''### 熔断与限流（第 100—106 讲）

- 断路器防雪崩：**关闭 = 正常调用；打开 = 直接拒绝；半开 = 放少量试探**；降级 fallback。
- Hystrix（Netflix，已维护）：@EnableCircuitBreaker，@HystrixCommand(fallbackMethod)，线程池 / 信号量隔离；Feign：feign.hystrix.enabled + fallback；Dashboard 读 /actuator/hystrix.stream，**Turbine 聚合**。
- Resilience4j：轻量、Java 8 函数式、按模块引入（CircuitBreaker、Bulkhead、RateLimiter、Retry、TimeLimiter、Cache）。
- **失败率 → 断路器**（failureRateThreshold 默认 50%，waitDurationInOpenState）；**同时几个 → Bulkhead**（maxConcurrentCalls，BulkheadFullException）；**每段时间几次 → RateLimiter**（limitForPeriod、limitRefreshPeriod，RequestNotPermitted）。可配合使用。
'''
