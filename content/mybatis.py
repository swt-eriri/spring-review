# 模块：MyBatis（第 20—22 讲）。深度：认得出。
from qhelp import Q, TF

MODULE = {
    'id': 'mybatis', 'title': 'MyBatis：自己写 SQL，以及两个好用的工具', 'short': 'MyBatis',
    'group': '第三章 O/R Mapping 实践', 'exam': '第 20—22 讲',
    'refs': [{'label': 'MyBatis-Spring-Boot-Starter 说明', 'url': 'https://mybatis.org/spring-boot-starter/mybatis-spring-boot-autoconfigure/'}],
    'lessons': [
        {'title': 'MyBatis 和 JPA 怎么选', 'cards': [
'''### 一句话

**MyBatis = SQL 由你自己写，它负责把结果对应到对象上。**JPA 则是你操作对象，SQL 由它生成。

| | JPA | MyBatis |
|---|---|---|
| SQL 谁写 | 框架自动生成 | **开发者自己写** |
| 适合 | 简单的增删改查 | **复杂查询**、需要精细控制 SQL、有 DBA 审核 SQL 的场景 |
| 国内使用 | 较少 | **很多** |

> 📌 认准：**想自己控制 SQL → MyBatis。**''',
'''### 在 Spring Boot 中使用（第 20 讲）

| 看到题目说…… | 就选 |
|---|---|
| MyBatis 的起步依赖 | **mybatis-spring-boot-starter** |
| 标记一个接口是 MyBatis 的 Mapper | **@Mapper** |
| 批量扫描某个包下的所有 Mapper | **@MapperScan** |
| 在接口方法上直接写查询 SQL | **@Select**（还有 @Insert、@Update、@Delete） |
| 插入后拿到自动生成的主键 | **@Options(useGeneratedKeys = true)** |
| 自定义 Java 类型和数据库类型的转换 | **TypeHandler**（类型处理器） |

常用配置（前缀 `mybatis.`）：
- **mapper-locations**：XML 映射文件在哪；
- **type-handlers-package**：类型处理器在哪个包；
- **configuration.map-underscore-to-camel-case**：把数据库的 `create_time` 自动对应到 Java 的 `createTime`（下划线转驼峰）。'''
        ]},
        {'title': 'MyBatis Generator 和 PageHelper', 'cards': [
'''### MyBatis Generator：自动生成代码（第 21 讲）

**根据数据库表结构，自动生成 Model（对应表的类）、Mapper 接口和 XML 映射文件。**简称 **MBG**。

- 配置文件：**generatorConfig.xml**，里面写清楚连哪个数据库、生成哪些表、生成到哪里、用哪些插件；
- 运行方式：命令行、**Maven 插件**、或 Java 代码；
- 生成的代码**仍然需要人工检查**。

### PageHelper：分页插件（第 22 讲）

**给 MyBatis 加上分页功能，支持多种数据库。**

- 起步依赖：**pagehelper-spring-boot-starter**；
- 发起分页的方式：传 **RowBounds** 参数、或在方法参数里直接传页码和每页条数；
- 分页结果信息可以用 **PageInfo** 包装（总条数、总页数等）。

> 📌 认准：**Generator = 生成代码；PageHelper = 分页。**'''
        ]},
    ],
    'questions': [
        Q('mybatis-p1', '需要开发者**自己控制 SQL** 的数据访问框架是？', ['MyBatis', 'Spring Data JPA', 'Hibernate', 'Spring Data REST'], 0,
          ['自己写 SQL', 'SQL 自动生成', 'JPA 实现，SQL 自动生成', '把 Repository 暴露为接口'], '自己写 SQL → MyBatis。', lesson=0),
        Q('mybatis-p2', '根据表结构自动生成 Model、Mapper、XML 的工具是？', ['MyBatis Generator', 'PageHelper', 'Lombok', 'Spring Initializr'], 0,
          ['生成代码', '分页', '少写 getter/setter', '生成工程'], 'Generator = 生成。', lesson=1),
        Q('mybatis-p3', '给 MyBatis 提供分页功能的插件是？', ['PageHelper', 'MyBatis Generator', 'HikariCP', 'Druid'], 0,
          ['分页', '生成代码', '连接池', '连接池'], 'PageHelper = 分页。', lesson=1),

        Q('mybatis-1', 'MyBatis 中标记 Mapper 接口的注解是？', ['@Mapper', '@Repository', '@Entity', '@Service'], 0,
          ['对', '那是 Spring 数据层注解', 'JPA 实体', '业务层'], '@Mapper，批量扫描用 @MapperScan。'),
        Q('mybatis-2', '批量扫描某个包下所有 Mapper 接口的注解是？', ['@MapperScan', '@ComponentScan', '@Mapper', '@EnableJpaRepositories'], 0,
          ['Mapper + Scan', '那是扫描 Spring 组件', '单个标记', 'JPA 的'], '@MapperScan。'),
        Q('mybatis-3', '在 Mapper 接口方法上直接写查询 SQL，用？', ['@Select', '@Query', '@Transactional', '@GetMapping'], 0,
          ['MyBatis 的', '那是 Spring Data 的', '事务', 'Web 的'], '@Select / @Insert / @Update / @Delete。'),
        Q('mybatis-4', 'MyBatis 插入后拿到自动生成的主键，用？', ['@Options(useGeneratedKeys = true)', '@GeneratedValue', '@Id', 'SimpleJdbcInsert'], 0,
          ['对', 'JPA 的', 'JPA 的', 'Spring JDBC 的'], 'use generated keys = 使用生成的主键。'),
        Q('mybatis-5', '自定义 Java 类型和数据库字段类型之间的转换，MyBatis 用？', ['TypeHandler', 'RowMapper', 'Converter', 'HttpMessageConverter'], 0,
          ['类型处理器', 'Spring JDBC 的', 'Spring 通用转换器', 'Web 消息转换'], 'MyBatis → TypeHandler。'),
        Q('mybatis-6', '让 `create_time` 自动对应到 `createTime`，MyBatis 的配置是？', ['map-underscore-to-camel-case', 'mapper-locations', 'type-handlers-package', 'show-sql'], 0,
          ['下划线 underscore 转驼峰 camel case', 'XML 位置', '类型处理器包', 'JPA 的'], '下划线转驼峰。'),
        Q('mybatis-7', 'MyBatis 指定 XML 映射文件位置的配置是？', ['mybatis.mapper-locations', 'mybatis.type-handlers-package', 'spring.datasource.url', 'spring.jpa.show-sql'], 0,
          ['locations = 位置', '类型处理器', '数据库地址', 'JPA'], 'mapper-locations。'),
        Q('mybatis-8', 'MyBatis 在 Spring Boot 中的起步依赖是？', ['mybatis-spring-boot-starter', 'spring-boot-starter-mybatis', 'spring-boot-starter-data-jpa', 'pagehelper-spring-boot-starter'], 0,
          ['第三方 starter 的命名：xxx-spring-boot-starter', '命名不对', 'JPA 的', '分页插件的'], '第三方起步依赖名字以 spring-boot-starter 结尾。'),
        Q('mybatis-9', 'MyBatis Generator 的配置文件通常叫？', ['generatorConfig.xml', 'pom.xml', 'application.yml', 'sql-error-codes.xml'], 0,
          ['对', 'Maven', 'Spring 配置', '错误码对照'], 'generatorConfig.xml。'),
        Q('mybatis-10', 'MyBatis Generator 可以通过哪些方式运行？', ['命令行', 'Maven 插件', 'Java 代码', '浏览器插件'], [0, 1, 2],
          ['可以', '可以', '可以', '不可以'], '三种方式。'),
        Q('mybatis-11', 'PageHelper 中可以用什么参数发起分页？', ['RowBounds', '在方法参数中传页码和每页条数', 'Pageable', 'Sort'], [0, 1],
          ['可以', '可以', 'Spring Data 的', 'Spring Data 的'], 'RowBounds 或方法参数。'),
        TF('mybatis-12', 'MyBatis Generator 生成的代码可以直接使用，不需要人工检查', False, '错', '对：仍需审查', '生成结果仍需审查。'),
        Q('mybatis-13', '相比 JPA，MyBatis 更适合的场景是？', ['复杂查询、需要精细控制 SQL', '完全不想写 SQL 的简单增删改查', '不使用数据库的程序', '只做页面展示'], 0,
          ['对', '那是 JPA 的长处', '无关', '无关'], '控制 SQL → MyBatis。'),
    ],
}

CHEATSHEET = '''### MyBatis（第 20—22 讲）

- MyBatis 自己写 SQL（复杂查询、精细控制）；JPA 自动生成 SQL（简单增删改查）。
- mybatis-spring-boot-starter；@Mapper / @MapperScan；@Select 等写 SQL；@Options(useGeneratedKeys=true) 拿主键；TypeHandler 类型转换。
- 配置：mapper-locations（XML 位置）、type-handlers-package、map-underscore-to-camel-case（下划线转驼峰）。
- **MyBatis Generator** 生成 Model / Mapper / XML，配置 generatorConfig.xml，命令行 / Maven 插件 / Java 运行，结果要审查。
- **PageHelper** 分页：pagehelper-spring-boot-starter，RowBounds 或方法参数，PageInfo。
'''
