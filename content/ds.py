# 模块：数据源与连接池（第 05—08 讲）。深度：认得出。默认值按 Spring Boot 2.1 / HikariCP 3 补充。
from qhelp import Q, TF

MODULE = {
    'id': 'ds', 'title': '数据源与连接池：单数据源、多数据源、HikariCP、Druid', 'short': '数据源与连接池',
    'group': '第二章 JDBC 必知必会', 'exam': '第 05—08 讲',
    'refs': [{'label': 'HikariCP 官方说明', 'url': 'https://github.com/brettwooldridge/HikariCP'}],
    'lessons': [
        {'title': '数据源是什么，Boot 帮你配了哪些', 'cards': [
'''### 一句话

- **数据源（DataSource）** = 程序拿数据库连接的地方。
- **连接池** = 提前开好一批数据库连接放着，用的时候借，用完还回去，省得每次重新连接。

### 单数据源：Boot 自动配好三样东西（第 05 讲）

只要引入 JDBC 依赖和数据库驱动，Spring Boot 会**自动**配置：

| 自动配好的 | 作用 |
|---|---|
| **DataSource** | 数据源（连接池） |
| **DataSourceTransactionManager** | 事务管理器（事务模块讲过） |
| **JdbcTemplate** | 操作数据库的工具（下个模块讲） |

连接信息写在配置文件里：`spring.datasource.url`、`spring.datasource.username`、`spring.datasource.password`。

程序启动时可以自动执行 **schema.sql**（建表）和 **data.sql**（插入数据）。

> 📌 对比：**传统 Spring 要自己一个个写出来，Spring Boot 自动配。**''',
'''### 多数据源（第 06 讲）

一个程序连两个数据库时，Boot 不知道该自动配哪个，要你自己来。两种办法：

1. **排除自动配置，全部自己配**：每个数据库各配一套 DataSource、事务管理器等；
2. **用 @Primary 指定主数据源**：Boot 的自动配置就围绕主数据源进行。

| 看到题目说…… | 就选 |
|---|---|
| 多个同类型 Bean 里，指定**默认用哪个** | **@Primary** |
| 不想用某个自动配置 | 在 @SpringBootApplication 里写 **exclude** |

> ⚠️ 多数据源时，**每个数据源要有自己的事务管理器**。'''
        ]},
        {'title': 'HikariCP：Spring Boot 2 的默认连接池', 'cards': [
'''### 一句话

**HikariCP 是 Spring Boot 2.x 默认的连接池，主打「快」。**（Hikari 是日语「光」。Spring Boot 1.x 默认的是 Tomcat 连接池。）

### 为什么快（了解，认得出关键词就行）

- 字节码层面做了精简优化；
- 用自己写的 **FastList** 代替 ArrayList；
- 用无锁的 **ConcurrentBag** 管理连接。

### 常用配置（前缀 `spring.datasource.hikari.`）

| 配置 | 意思 | 默认值（补充） |
|---|---|---|
| **maximumPoolSize** | 最多多少个连接 | 10 |
| minimumIdle | 最少保留多少空闲连接 | 和最大值一样 |
| connectionTimeout | 借连接最多等多久 | 30 秒 |
| idleTimeout | 空闲连接多久后关掉 | 10 分钟 |
| maxLifetime | 一个连接最长活多久 | 30 分钟 |

> 📌 记住：**Boot 2 默认 HikariCP；最大连接数 maximumPoolSize。**'''
        ]},
        {'title': 'Druid：阿里巴巴的连接池，主打监控', 'cards': [
'''### 一句话

**Druid 是阿里巴巴开源的连接池，最大特点是「能监控」。**

| 看到题目说…… | 就选 |
|---|---|
| 阿里巴巴开源的连接池 | **Druid** |
| 连接池 + SQL 监控、统计 | **Druid** |
| Spring Boot 2 默认连接池、主打快 | **HikariCP** |

### Druid 的能力（第 08、14 讲）

- **SQL 监控和统计**：哪条 SQL 执行了多少次、多慢；
- **慢 SQL 记录**：超过设定时间的 SQL 记下来；
- **防 SQL 注入**：WallFilter（Wall = 防火墙）；
- **数据库密码加密**：配置文件里不写明文密码；
- **Filter（过滤器）扩展**：可以自己写 Filter 插入额外逻辑。

接入方式：引入 **druid-spring-boot-starter**。

> 💡 选连接池要综合看：稳定性、性能、能不能监控、还有没有人维护。'''
        ]},
    ],
    'questions': [
        Q('ds-p1', '引入 JDBC 依赖后，Spring Boot 会自动配置哪些？', ['DataSource', 'DataSourceTransactionManager', 'JdbcTemplate', 'RestTemplate'], [0, 1, 2],
          ['数据源', '事务管理器', '数据库工具', 'RestTemplate 是调用网络接口的，Boot 不会因为 JDBC 自动配它'], '单数据源三件套。', lesson=0),
        Q('ds-p2', 'Spring Boot 2.x 默认的连接池是？', ['Druid', 'HikariCP', 'C3P0', 'DBCP'], 1,
          ['阿里的，主打监控', 'Boot 2 默认', '老牌连接池', '老牌连接池'], 'Boot 2 → HikariCP。', lesson=1),
        Q('ds-p3', '阿里巴巴开源、主打 SQL 监控的连接池是？', ['HikariCP', 'Druid', 'Tomcat JDBC', 'Lettuce'], 1,
          ['主打快', '阿里 + 监控 → Druid', 'Boot 1.x 默认', 'Lettuce 是 Redis 客户端'], 'Druid = 监控。', lesson=2),

        Q('ds-1', '数据库连接信息（地址、用户名、密码）配置项的前缀是？', ['spring.datasource', 'spring.jpa', 'server', 'spring.redis'], 0,
          ['对', 'JPA 的配置', '服务器配置', 'Redis 配置'], 'spring.datasource.url / username / password。'),
        Q('ds-2', '连接池的作用是？', ['提前建好一批连接，借用和归还，避免频繁新建', '把多个数据库合并成一个', '加密数据库', '自动建表'], 0,
          ['对', '无关', '无关', '无关'], '连接池 = 借和还。'),
        Q('ds-3', 'Spring Boot 启动时，可以自动执行哪些文件来建表、插数据？', ['schema.sql', 'data.sql', 'pom.xml', 'application.properties'], [0, 1],
          ['建表', '插入数据', 'Maven 配置文件', '配置文件，不是 SQL'], 'schema 建表，data 插数据。'),
        Q('ds-4', '多个同类型的 Bean 中，指定默认使用哪一个，用？', ['@Primary', '@Autowired', '@Bean', '@Service'], 0,
          ['Primary = 主要的', '自动塞', '造 Bean', '业务层'], '多数据源常用 @Primary 指定主数据源。'),
        Q('ds-5', '配置多数据源时，下列说法正确的是？', ['每个数据源要配自己的事务管理器', 'Boot 会自动为每个数据源配好一切', '多数据源不能使用事务', '只能有一个 DataSource Bean'], 0,
          ['对', '多数据源时 Boot 不知道配哪个，需要自己配', '可以用事务', '可以有多个'], '多数据源：自己配，或 @Primary 指定主的。'),
        Q('ds-6', '不想让 Spring Boot 自动配置某个功能，可以？', ['在 @SpringBootApplication 中用 exclude 排除', '删掉 Spring Boot', '改用 @Primary', '加 @Autowired'], 0,
          ['对', '没必要', '那是指定主 Bean', '那是自动塞'], 'exclude = 排除。'),
        Q('ds-7', 'HikariCP 中设置**最大连接数**的配置是？', ['maximumPoolSize', 'minimumIdle', 'idleTimeout', 'maxLifetime'], 0,
          ['最大池大小', '最少空闲数', '空闲超时', '连接最长寿命'], '看英文：maximum pool size。'),
        Q('ds-8', 'HikariCP 中，**一个连接最长能活多久**的配置是？', ['maximumPoolSize', 'connectionTimeout', 'maxLifetime', 'minimumIdle'], 2,
          ['最大连接数', '借连接最多等多久', 'life time = 寿命', '最少空闲数'], 'maxLifetime = 最长寿命。'),
        Q('ds-9', 'HikariCP 中，**借连接时最多等多久**的配置是？', ['connectionTimeout', 'idleTimeout', 'maxLifetime', 'maximumPoolSize'], 0,
          ['connection timeout = 获取连接超时', '空闲多久后关闭', '最长寿命', '最大连接数'], 'connectionTimeout。'),
        Q('ds-10', '下列哪些是 HikariCP 速度快的原因？', ['字节码精简优化', '用 FastList 代替 ArrayList', '无锁的 ConcurrentBag', '自带 SQL 监控页面'], [0, 1, 2],
          ['是', '是', '是', '监控是 Druid 的特点'], 'Hikari 主打快，Druid 主打监控。'),
        Q('ds-11', 'Druid 中用于**防 SQL 注入**的是？', ['WallFilter', 'StatFilter', 'FastList', 'RowMapper'], 0,
          ['Wall = 防火墙', 'StatFilter 做统计', 'Hikari 的内部结构', 'JdbcTemplate 的结果映射'], 'Wall = 防火墙。'),
        Q('ds-12', 'Druid 提供了哪些能力？', ['SQL 监控统计', '慢 SQL 记录', '防 SQL 注入', '数据库密码加密'], [0, 1, 2, 3],
          ['有', '有', '有', '有'], 'Druid 主打监控和扩展。'),
        Q('ds-13', '在 Spring Boot 中接入 Druid，通常引入？', ['druid-spring-boot-starter', 'spring-boot-starter-actuator', 'spring-boot-starter-web', 'HikariCP'], 0,
          ['Druid 的起步依赖', '监控端点', 'Web', '另一个连接池'], '第三方起步依赖的命名：xxx-spring-boot-starter。'),
        TF('ds-14', 'Spring Boot 1.x 和 2.x 的默认连接池都是 HikariCP', False, '错', '对：1.x 默认是 Tomcat 连接池，2.x 才改为 HikariCP', 'Boot 2 → HikariCP。'),
        TF('ds-15', '传统 Spring（不用 Boot）需要自己显式配置 DataSource、事务管理器等 Bean', True, '对', '错', 'Boot 自动配，传统 Spring 手动配。'),
    ],
}

CHEATSHEET = '''### 数据源与连接池（第 05—08 讲）

- 单数据源：Boot 自动配 **DataSource + DataSourceTransactionManager + JdbcTemplate**；配置前缀 spring.datasource；schema.sql 建表、data.sql 插数据。
- 多数据源：每个配自己的事务管理器；排除自动配置（exclude）或用 **@Primary** 指定主数据源。
- **HikariCP** = Boot 2 默认，主打快（字节码精简、FastList、ConcurrentBag）；maximumPoolSize 最大连接数（默认 10），maxLifetime 寿命，connectionTimeout 等待。Boot 1 默认 Tomcat 连接池。
- **Druid** = 阿里，主打监控：SQL 统计、慢 SQL、WallFilter 防注入、密码加密、Filter 扩展；druid-spring-boot-starter。
'''
