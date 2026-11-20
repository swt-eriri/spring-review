# 模块：NoSQL 与缓存（第 24—30 讲）。深度：认得出。
from qhelp import Q, TF

MODULE = {
    'id': 'nosql', 'title': 'NoSQL 与缓存：Docker、MongoDB、Redis、缓存注解', 'short': 'NoSQL 与缓存',
    'group': '第四章 NoSQL 实践', 'exam': '第 24—30 讲',
    'refs': [{'label': 'Spring 5.3 文档 · 缓存抽象', 'url': 'https://docs.spring.io/spring-framework/docs/5.3.x/reference/html/integration.html#cache'}],
    'lessons': [
        {'title': 'Docker：一键启动数据库（了解）', 'cards': [
'''### 一句话

**Docker 让你不用安装，一条命令就把 MongoDB、Redis 这类软件跑起来。**课程用它来辅助开发。

| 词 | 一句话 |
|---|---|
| **镜像（image）** | 软件的「安装包」，只读 |
| **容器（container）** | 镜像**运行起来**的实例 |
| **端口映射** | 把容器里的端口对到电脑上，`-p 电脑端口:容器端口` |
| **数据卷（volume）** | 把数据存到容器外面，容器删了数据还在，`-v` |
| **环境变量** | 启动时传配置，`-e` |

| 命令 | 作用 |
|---|---|
| docker **pull** | 下载镜像 |
| docker **run** | 用镜像创建并启动容器 |
| docker **ps** | 看正在运行的容器 |
| docker **logs** | 看容器日志 |
| docker **stop / start** | 停止 / 启动容器 |

> 📌 认准：**镜像是安装包，容器是跑起来的程序。**'''
        ]},
        {'title': 'MongoDB 和 Redis', 'cards': [
'''### MongoDB：存「文档」的数据库（第 25 讲）

MongoDB 不用表，存的是类似 JSON 的**文档**。

| 看到题目说…… | 就选 |
|---|---|
| 标记一个类对应 MongoDB 里的文档 | **@Document** |
| 主键 | **@Id** |
| 操作 MongoDB 的工具类 | **MongoTemplate** |
| 只写接口就能操作 MongoDB | **MongoRepository** |
| 特殊类型（如金额）的读写转换 | 自定义**转换器**（Converter） |

> 💡 和 JPA 对比着记：JPA 是 @Entity + JpaRepository，MongoDB 是 **@Document + MongoRepository**，模板类叫 **MongoTemplate**。''',
'''### Redis：放在内存里的键值数据库（第 26、27、29 讲）

**Redis 很快，常用来做缓存。**数据结构有：**String（字符串）、List（列表）、Hash（哈希）、Set（集合）、ZSet（有序集合）**。

**Java 连 Redis 的两个客户端：**

| 客户端 | 特点 |
|---|---|
| **Jedis** | **不是线程安全的**，多线程要用连接池 **JedisPool** |
| **Lettuce** | 基于 Netty，线程安全，**Spring Boot 2 默认** |

**Redis 的两种高可用部署：**

| 模式 | 一句话 | Jedis 里用 |
|---|---|---|
| **哨兵（Sentinel）** | 哨兵**监控**主从节点，主挂了**自动切换** | JedisSentinelPool |
| **集群（Cluster）** | 数据**分片**存到多个节点，共 **16384 个哈希槽** | JedisCluster |

> ⚠️ 易混：**哨兵 = 监控 + 故障切换；集群 = 分片。**''',
'''### 在 Spring 里操作 Redis（第 29 讲）

| 看到题目说…… | 就选 |
|---|---|
| 操作 Redis 的模板类 | **RedisTemplate**（专门处理字符串的：**StringRedisTemplate**） |
| 操作字符串值 / 哈希 / 列表 | **opsForValue() / opsForHash() / opsForList()** |
| 用 Repository 的方式操作 Redis，实体上贴 | **@RedisHash** |
| 存进 Redis 时怎么把对象转成字节 | **序列化器**（RedisSerializer），可自定义，如转成 JSON |

> 💡 「ops」是 operations（操作）的缩写，后面跟数据结构名。'''
        ]},
        {'title': '缓存抽象：三个注解必背', 'cards': [
'''### 一句话

**在方法上贴个注解，Spring 就自动帮你缓存结果。**第二次调用时直接拿缓存，不再查数据库。

先用 **@EnableCaching** 打开缓存功能。然后：

| 注解 | 做什么 | 记法 |
|---|---|---|
| **@Cacheable** | 先查缓存，**有就直接返回**，没有才执行方法并放进缓存 | able = 可以缓存 |
| **@CachePut** | **总是执行方法**，然后把结果更新到缓存 | Put = 放进去 |
| **@CacheEvict** | **清除**缓存 | Evict = 赶走 |
| @Caching | 把上面几个组合起来 | |
| @CacheConfig | 贴在类上，写一些公共设置（如缓存名） | Config = 配置 |

> 📌 必背：**Cacheable 有缓存就不执行；CachePut 总是执行再更新；CacheEvict 清除。**''',
'''### 缓存放在哪

Spring 只定义了「怎么用缓存」，缓存具体存在哪可以换：

- 本地内存：ConcurrentHashMap、EhCache、Caffeine；
- 分布式：**Redis**（多个程序共用一份缓存）。

配置举例：`spring.cache.type=redis`（用 Redis 做缓存）、`spring.cache.redis.time-to-live`（缓存多久过期）。

**怎么选（第 28 讲）：**
- 只在一台机器上用、数据变化少 → 本地缓存；
- 多台机器要共享、数据量大 → Redis 这种分布式缓存；
- 都要考虑**数据一致性**和**过期策略**。

### SpringBucks 进度（第 30 讲）

咖啡店把**菜单**放进 Redis 缓存（菜单读多改少，很适合缓存），订单数据仍然用 JPA 存数据库。'''
        ]},
    ],
    'questions': [
        Q('nosql-p1', 'Docker 中，软件的「安装包」叫什么？', ['镜像', '容器', '数据卷', '端口'], 0,
          ['镜像 image', '容器是运行起来的实例', '存数据的', '网络'], '镜像是安装包，容器是跑起来的。', lesson=0),
        Q('nosql-p2', '标记一个类对应 MongoDB 中的文档，用？', ['@Document', '@Entity', '@RedisHash', '@Table'], 0,
          ['MongoDB', 'JPA', 'Redis', 'JPA 表名'], 'MongoDB → @Document。', lesson=1),
        Q('nosql-p3', '哪个 Redis 客户端**不是线程安全的**，需要配连接池使用？', ['Jedis', 'Lettuce', 'RedisTemplate', 'MongoTemplate'], 0,
          ['Jedis → JedisPool', 'Lettuce 线程安全', '它是 Spring 的模板', 'MongoDB 的'], 'Jedis 不安全，Lettuce 安全。', lesson=1),
        Q('nosql-p4', '先查缓存，有就直接返回、不执行方法的注解是？', ['@Cacheable', '@CachePut', '@CacheEvict', '@EnableCaching'], 0,
          ['对', '它总是执行方法', '它是清除', '它是打开缓存功能'], 'Cacheable。', lesson=2),

        Q('nosql-1', 'Docker 命令中，查看正在运行的容器用？', ['docker ps', 'docker pull', 'docker logs', 'docker run'], 0,
          ['对', '下载镜像', '看日志', '启动容器'], 'ps 看进程。'),
        Q('nosql-2', 'docker run 中把电脑端口映射到容器端口的参数是？', ['-p', '-v', '-e', '-d'], 0,
          ['port 端口', '数据卷', '环境变量', '后台运行'], '-p 端口，-v 数据卷，-e 环境变量。'),
        Q('nosql-3', '让容器删掉后数据仍然保留，用？', ['数据卷（-v）', '端口映射（-p）', '环境变量（-e）', 'docker logs'], 0,
          ['对', '网络', '配置', '日志'], '数据卷。'),
        Q('nosql-4', 'Spring 中操作 MongoDB 的模板类是？', ['MongoTemplate', 'RedisTemplate', 'JdbcTemplate', 'RestTemplate'], 0,
          ['对', 'Redis', '关系型数据库', '调用网络接口'], '各种 Template 按名字认。'),
        Q('nosql-5', '只写接口就能操作 MongoDB，继承？', ['MongoRepository', 'JpaRepository', 'CrudRepository 的 JPA 版', 'RedisTemplate'], 0,
          ['对', 'JPA 用的', '不对', '不是接口'], 'MongoRepository。'),
        Q('nosql-6', 'Redis 支持的数据结构有？', ['String', 'List', 'Hash', 'ZSet（有序集合）'], [0, 1, 2, 3],
          ['有', '有', '有', '有'], '还有 Set。'),
        Q('nosql-7', 'Spring Boot 2 默认的 Redis 客户端是？', ['Lettuce', 'Jedis', 'Druid', 'HikariCP'], 0,
          ['对', 'Boot 1 时代常用', '连接池', '连接池'], 'Boot 2 → Lettuce。'),
        Q('nosql-8', 'Redis 的哪种模式负责**监控主从并在主节点故障时自动切换**？', ['哨兵（Sentinel）', '集群（Cluster）', '单机', '主从复制本身'], 0,
          ['哨兵 = 监控 + 切换', '集群 = 分片', '无', '复制本身不会自动切换'], '哨兵 vs 集群。'),
        Q('nosql-9', 'Redis Cluster 通过什么方式分片？', ['16384 个哈希槽', '按表名', '按时间', '随机'], 0,
          ['对', '不是', '不是', '不是'], '哈希槽。'),
        Q('nosql-10', 'Spring 中专门操作字符串的 Redis 模板是？', ['StringRedisTemplate', 'RedisTemplate', 'MongoTemplate', 'JdbcTemplate'], 0,
          ['对', '通用的', 'MongoDB', 'JDBC'], 'String + RedisTemplate。'),
        Q('nosql-11', 'RedisTemplate 中操作哈希结构，用？', ['opsForHash()', 'opsForValue()', 'opsForList()', 'opsForSet()'], 0,
          ['对', '字符串值', '列表', '集合'], 'ops + 数据结构名。'),
        Q('nosql-12', '用 Repository 方式操作 Redis，实体上贴？', ['@RedisHash', '@Document', '@Entity', '@Cacheable'], 0,
          ['对', 'MongoDB', 'JPA', '缓存'], '@RedisHash。'),
        Q('nosql-13', '打开 Spring 缓存功能的注解是？', ['@EnableCaching', '@Cacheable', '@CacheConfig', '@EnableRedisRepositories'], 0,
          ['Enable = 打开', '用缓存', '类级公共配置', '打开 Redis Repository'], '@EnableCaching。'),
        Q('nosql-14', '**总是执行方法**，并把结果更新到缓存的注解是？', ['@CachePut', '@Cacheable', '@CacheEvict', '@Caching'], 0,
          ['Put = 放进去', '有缓存就不执行', '清除', '组合'], 'CachePut 总是执行。'),
        Q('nosql-15', '**清除**缓存的注解是？', ['@CacheEvict', '@CachePut', '@Cacheable', '@CacheConfig'], 0,
          ['Evict = 赶走', '更新', '读', '公共配置'], 'CacheEvict。'),
        Q('nosql-16', '贴在类上、为类中所有缓存注解提供公共设置（如缓存名）的是？', ['@CacheConfig', '@Caching', '@EnableCaching', '@Cacheable'], 0,
          ['Config = 配置', '组合多个注解', '打开功能', '读缓存'], '@CacheConfig。'),
        Q('nosql-17', '多台机器需要**共享**同一份缓存，适合用？', ['Redis', 'ConcurrentHashMap', 'Caffeine', 'EhCache 本地模式'], 0,
          ['分布式缓存', '本地内存', '本地缓存', '本地缓存'], '共享 → 分布式缓存。'),
        TF('nosql-18', '@Cacheable 标注的方法，每次调用都会执行方法体', False, '错', '对：有缓存时直接返回，不执行', '总是执行的是 @CachePut。'),
        Q('nosql-19', 'SpringBucks 中放进 Redis 缓存的是？', ['菜单', '订单', '支付密码', '日志'], 0,
          ['读多改少，适合缓存', '订单存数据库', '无', '无'], '第 30 讲。'),
        Q('nosql-20', '用 Redis 做 Spring 缓存时，设置缓存过期时间的配置是？', ['spring.cache.redis.time-to-live', 'spring.datasource.url', 'spring.cache.type', 'server.port'], 0,
          ['time to live = 存活时间', '数据库地址', '缓存类型', '端口'], 'TTL = 存活时间。'),
    ],
}

CHEATSHEET = '''### NoSQL 与缓存（第 24—30 讲）

- Docker：镜像 = 安装包，容器 = 运行实例；-p 端口，-v 数据卷，-e 环境变量；pull / run / ps / logs / stop。
- MongoDB：@Document + @Id，MongoTemplate，MongoRepository，自定义 Converter。
- Redis：String / List / Hash / Set / ZSet。**Jedis 线程不安全（JedisPool），Lettuce 线程安全、Boot 2 默认**。
- **哨兵 = 监控 + 自动切换**（JedisSentinelPool）；**集群 = 分片，16384 哈希槽**（JedisCluster）。
- RedisTemplate / StringRedisTemplate；opsForValue / opsForHash / opsForList；@RedisHash；可自定义序列化器。
- 缓存：@EnableCaching 打开；**@Cacheable 有就不执行；@CachePut 总执行再更新；@CacheEvict 清除**；@Caching 组合；@CacheConfig 类级配置。共享用 Redis，spring.cache.redis.time-to-live 过期。
'''
