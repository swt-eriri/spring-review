# 模块：重新认识 Spring Boot（第 67—74 讲）。深度：认得出。配置优先级按 Boot 2.1 文档补充。
from qhelp import Q, TF

MODULE = {
    'id': 'boot', 'title': 'Spring Boot 原理：自动配置、起步依赖、配置加载', 'short': 'Boot 原理',
    'group': '第九章 重新认识 Spring Boot', 'exam': '第 67—74 讲',
    'refs': [{'label': 'Spring Boot 2.1 文档 · 外部化配置', 'url': 'https://docs.spring.io/spring-boot/docs/2.1.x/reference/html/boot-features-external-config.html'}],
    'lessons': [
        {'title': 'Spring Boot 由什么组成', 'cards': [
'''### 一句话

**Spring Boot 帮你快速做出一个能独立运行的 Spring 程序。**

### 四个组成部分（必背，第 67 讲）

| 组成 | 一句话 |
|---|---|
| **自动配置**（Auto Configuration） | 根据你引入了什么，**自动**帮你配好 Bean |
| **起步依赖**（Starter） | 把一个功能需要的依赖**打包成一个**，引一个就够 |
| **命令行工具**（CLI） | 在命令行里快速运行 Groovy 脚本（了解） |
| **Actuator** | 监控和管理运行中的程序 |

### Spring Boot **不是**什么（常考判断）

- 不是应用服务器（它内嵌了服务器，但本身不是）；
- 不是 Java EE 规范的实现；
- 不是代码生成器；
- 不是 Spring Framework 的替代品（它建立在 Spring Framework 之上）。'''
        ]},
        {'title': '自动配置的原理', 'cards': [
'''### 自动配置怎么找到要配什么（第 68 讲，认关键词）

1. **@EnableAutoConfiguration**（包含在 @SpringBootApplication 里）开启自动配置；
2. 它通过 **AutoConfigurationImportSelector**（导入选择器）去读取
3. 各个 jar 包里的 **META-INF/spring.factories** 文件，找到所有候选的自动配置类；
4. 每个配置类上有**条件注解**，条件满足才生效。

> 📌 一句话：**@EnableAutoConfiguration → 读 spring.factories → 按条件注解决定生不生效。**

### 条件注解：对号入座（必背）

| 注解 | 什么时候生效 |
|---|---|
| **@ConditionalOnClass** | 类路径里**有**某个类 |
| @ConditionalOnMissingClass | 类路径里**没有**某个类 |
| @ConditionalOnBean | 容器里**有**某个 Bean |
| **@ConditionalOnMissingBean** | 容器里**没有**某个 Bean（**你自己配了，就用你的**） |
| **@ConditionalOnProperty** | 配置文件里有某个配置 / 等于某个值 |
| @ConditionalOnWebApplication | 是 Web 程序 |
| @ConditionalOnResource | 有某个资源文件 |''',
'''### 自己写自动配置（第 69、70 讲）

1. 写一个配置类，里面用 @Bean 造 Bean；
2. 加上**条件注解**控制何时生效；
3. 在 **spring.factories** 里登记它。

- 控制顺序：**@AutoConfigureBefore / @AutoConfigureAfter / @AutoConfigureOrder**；
- 允许用户覆盖：用 **@ConditionalOnMissingBean**，用户自己配了就不再配；
- 查看哪些自动配置生效了：启动时加 **--debug**，会打印「条件评估报告」；
- 不要某个自动配置：**exclude**。

**低版本 Spring（没有条件注解）怎么做**：用 **BeanFactoryPostProcessor** 等扩展点，在启动时检查并注册 Bean（第 70 讲）。'''
        ]},
        {'title': '起步依赖和配置加载', 'cards': [
'''### 起步依赖（第 71、72 讲）

**Starter 把一个功能需要的依赖打包好**，版本由 **BOM**（spring-boot-dependencies）统一管理。

**命名规则（常考）：**

| 谁做的 | 命名 | 例子 |
|---|---|---|
| **官方** | **spring-boot-starter-xxx** | spring-boot-starter-web |
| **第三方 / 自己** | **xxx-spring-boot-starter** | mybatis-spring-boot-starter |

自己做 Starter 时：
- 通常拆成两个模块：**autoconfigure 模块**（放自动配置代码）+ **starter 模块**（只负责引入依赖）；
- 配置前缀不要用 spring 开头，和官方区分开。

依赖冲突时：用 **mvn dependency:tree** 看依赖树，用 **exclusion** 排除。''',
'''### 配置加载的优先级（第 73 讲，记大方向）

同一个配置在多个地方都写了，**优先级高的覆盖低的**。从高到低大致是：

1. **命令行参数**（如 `--server.port=8081`）
2. Java 系统属性（-D）
3. **操作系统环境变量**
4. jar 包**外面**的 application-{profile} 配置文件
5. jar 包**里面**的 application-{profile} 配置文件
6. jar 包**外面**的 application 配置文件
7. jar 包**里面**的 application 配置文件
8. @PropertySource 指定的文件
9. 默认属性

> 📌 记三条：**命令行最高；带 profile 的高于不带的；jar 外高于 jar 内。**

- **Profile**：区分环境（如 dev、prod），用 **spring.profiles.active** 指定；
- **宽松绑定**：`spring.jpa.database-platform`、`spring.jpa.databasePlatform`、环境变量 `SPRING_JPA_DATABASEPLATFORM` 都能对上，推荐用**中划线**写法。''',
'''### PropertySource 抽象（第 74 讲）

- 所有配置来源都被统一抽象成 **PropertySource**，汇总在 **Environment**（环境）里；
- 把一组配置绑定到一个 Java 对象：**@ConfigurationProperties(prefix = "...")**；
- 读取单个配置值：**@Value("${...}")**；
- 加一个自定义的配置来源：实现 **EnvironmentPostProcessor**，并在 spring.factories 里登记。

> 📌 认准：**一组配置 → @ConfigurationProperties；单个值 → @Value。**'''
        ]},
    ],
    'questions': [
        Q('boot-p1', 'Spring Boot 的组成部分包括？', ['自动配置', '起步依赖', 'Actuator', '应用服务器规范'], [0, 1, 2],
          ['是', '是', '是', 'Boot 不是应用服务器'], '还有命令行 CLI。', lesson=0),
        Q('boot-p2', '自动配置的候选配置类登记在哪个文件里（课程所用版本）？', ['META-INF/spring.factories', 'application.properties', 'pom.xml', 'sql-error-codes.xml'], 0,
          ['对', '应用配置', 'Maven', '错误码'], 'spring.factories。', lesson=1),
        Q('boot-p3', '官方起步依赖的命名格式是？', ['spring-boot-starter-xxx', 'xxx-spring-boot-starter', 'starter-xxx', 'xxx-starter-spring'], 0,
          ['官方', '第三方', '不对', '不对'], '官方前缀，第三方后缀。', lesson=2),

        Q('boot-1', '下列关于 Spring Boot 的说法，**错误**的是？', ['Spring Boot 是一个应用服务器', 'Spring Boot 能内嵌服务器', 'Spring Boot 建立在 Spring Framework 之上', 'Spring Boot 提供自动配置'], 0,
          ['错：它不是应用服务器', '对', '对', '对'], 'Boot 不是：应用服务器、Java EE 实现、代码生成器、Spring 替代品。'),
        Q('boot-2', '开启自动配置的注解是？', ['@EnableAutoConfiguration', '@ComponentScan', '@Configuration', '@ConditionalOnClass'], 0,
          ['对', '扫描组件', '配置类', '条件'], '包含在 @SpringBootApplication 里。'),
        Q('boot-3', '读取 spring.factories 中候选自动配置类的是？', ['AutoConfigurationImportSelector', 'DispatcherServlet', 'HandlerMapping', 'JdbcTemplate'], 0,
          ['导入选择器', 'Web 入口', 'Web', '数据库'], '第 68 讲。'),
        Q('boot-4', '类路径中**存在**某个类时才生效的条件注解是？', ['@ConditionalOnClass', '@ConditionalOnMissingClass', '@ConditionalOnBean', '@ConditionalOnProperty'], 0,
          ['有某个类', '没有某个类', '有某个 Bean', '有某个配置'], 'OnClass。'),
        Q('boot-5', '容器中**没有**某个 Bean 时才生效、让用户可以覆盖默认配置的是？', ['@ConditionalOnMissingBean', '@ConditionalOnBean', '@ConditionalOnClass', '@Primary'], 0,
          ['用户配了就用用户的', '有 Bean 才生效', '有类才生效', '指定主 Bean'], 'OnMissingBean。'),
        Q('boot-6', '根据配置文件中某个配置项的值决定是否生效的是？', ['@ConditionalOnProperty', '@ConditionalOnResource', '@ConditionalOnWebApplication', '@ConditionalOnClass'], 0,
          ['Property = 属性 / 配置', '资源文件', 'Web 程序', '类'], 'OnProperty。'),
        Q('boot-7', '控制自动配置类之间先后顺序的注解有？', ['@AutoConfigureBefore', '@AutoConfigureAfter', '@AutoConfigureOrder', '@Primary'], [0, 1, 2],
          ['是', '是', '是', '那是指定主 Bean'], 'AutoConfigure + Before / After / Order。'),
        Q('boot-8', '想查看哪些自动配置生效、哪些没生效，启动时加？', ['--debug', '--port', '--profile', '--help'], 0,
          ['打印条件评估报告', '不对', '不对', '不对'], '--debug。'),
        Q('boot-9', '在没有条件注解的低版本 Spring 中实现类似自动配置，可以用？', ['BeanFactoryPostProcessor', '@ConditionalOnClass', 'spring.factories', 'Actuator'], 0,
          ['扩展点', '低版本没有', '那是 Boot 的', '无关'], '第 70 讲。'),
        Q('boot-10', '第三方（或自己做的）起步依赖的命名格式是？', ['xxx-spring-boot-starter', 'spring-boot-starter-xxx', 'spring-xxx', 'boot-xxx'], 0,
          ['第三方', '官方专用', '不对', '不对'], '如 mybatis-spring-boot-starter。'),
        Q('boot-11', '自己做 Starter 时，通常拆成哪两个模块？', ['autoconfigure 模块和 starter 模块', 'web 模块和 db 模块', '前端和后端', '测试和生产'], 0,
          ['对', '不是', '不是', '不是'], '自动配置代码 + 依赖入口。'),
        Q('boot-12', '查看依赖树、排查依赖冲突的 Maven 命令是？', ['mvn dependency:tree', 'mvn clean', 'mvn package', 'mvn deploy'], 0,
          ['对', '清理', '打包', '发布'], 'dependency:tree，排除用 exclusion。'),
        Q('boot-13', '下列配置来源中，优先级**最高**的是？', ['命令行参数', 'jar 包内的 application.properties', 'jar 包外的 application.properties', '@PropertySource'], 0,
          ['最高', '最低之一', '高于 jar 内，低于命令行', '很低'], '命令行最高。'),
        Q('boot-14', 'jar 包外的 application.properties 和 jar 包内的，谁优先？', ['jar 包外', 'jar 包内', '一样', '看文件大小'], 0,
          ['外高于内', '反了', '不一样', '无关'], 'jar 外 > jar 内。'),
        Q('boot-15', 'application-prod.properties 和 application.properties（同在 jar 内），谁优先？', ['application-prod.properties', 'application.properties', '一样', '后加载的'], 0,
          ['带 profile 的优先', '反了', '不一样', '不对'], '带 profile 的 > 不带的。'),
        Q('boot-16', '指定当前激活哪个环境（profile）的配置是？', ['spring.profiles.active', 'spring.application.name', 'server.port', 'spring.config.name'], 0,
          ['对', '应用名', '端口', '配置文件名'], 'spring.profiles.active。'),
        Q('boot-17', '配置项写法 `spring.jpa.database-platform` 和环境变量 `SPRING_JPA_DATABASEPLATFORM` 能对上，这叫？', ['宽松绑定', '自动配置', '内容协商', '背压'], 0,
          ['Relaxed Binding', '不是', '不是', '不是'], '推荐中划线写法。'),
        Q('boot-18', '把一组前缀相同的配置绑定到一个 Java 对象上，用？', ['@ConfigurationProperties', '@Value', '@PropertySource', '@Configuration'], 0,
          ['一组 → ConfigurationProperties', '单个值', '指定配置文件', '配置类'], '一组 vs 单个。'),
        Q('boot-19', 'Spring 中统一表示「一个配置来源」的抽象是？', ['PropertySource', 'DataSource', 'Resource', 'Repository'], 0,
          ['对', '数据源', '资源', '数据访问'], '汇总在 Environment 中。'),
        Q('boot-20', '添加自定义的配置来源，可以实现？', ['EnvironmentPostProcessor', 'HandlerInterceptor', 'RowMapper', 'HealthIndicator'], 0,
          ['对，并在 spring.factories 登记', '拦截器', 'JDBC', '健康检查'], 'EnvironmentPostProcessor。'),
    ],
}

CHEATSHEET = '''### Boot 原理（第 67—74 讲）

- 四部分：**自动配置、起步依赖、CLI、Actuator**。Boot 不是：应用服务器、Java EE 实现、代码生成器、Spring 替代品。
- **@EnableAutoConfiguration → AutoConfigurationImportSelector → META-INF/spring.factories → 条件注解**。
- 条件：OnClass / OnMissingClass / OnBean / **OnMissingBean（用户可覆盖）** / OnProperty / OnWebApplication / OnResource。
- 顺序 @AutoConfigureBefore / After / Order；--debug 看条件报告；exclude 排除；低版本用 BeanFactoryPostProcessor。
- Starter：**官方 spring-boot-starter-xxx，第三方 xxx-spring-boot-starter**；拆 autoconfigure + starter；BOM 管版本；mvn dependency:tree + exclusion。
- 优先级：**命令行最高；带 profile > 不带；jar 外 > jar 内**；spring.profiles.active；宽松绑定（推荐中划线）。
- PropertySource → Environment；**@ConfigurationProperties 一组，@Value 单个**；EnvironmentPostProcessor 加配置源。
'''
