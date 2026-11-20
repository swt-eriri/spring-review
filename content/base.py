# 模块：初识 Spring（第 01—04、13 讲）。深度：认得出。细节按 Spring 5 / Boot 2.1 补充。
from qhelp import Q, TF

MODULE = {
    'id': 'base', 'title': '初识 Spring：全家桶、Bean 和第一个程序', 'short': '初识 Spring',
    'group': '第一章 初识 Spring', 'exam': '第 01—04、13 讲',
    'refs': [{'label': 'Spring Initializr（生成工程的网站）', 'url': 'https://start.spring.io/'}],
    'lessons': [
        {'title': '全家桶里都有谁', 'cards': [
'''### 一句话

**Spring 全家桶 = 一组帮你写 Java 后端程序的工具。**三个最重要的成员一层叠一层：

| 成员 | 一句话 | 看到题目说…… |
|---|---|---|
| **Spring Framework** | 地基：管理对象、AOP、事务、Web 等基础能力 | IoC、AOP、「核心」「基础」 |
| **Spring Boot** | 让程序**快速搭起来、直接跑起来** | 自动配置、起步依赖、「快速」「开箱即用」 |
| **Spring Cloud** | 解决**很多个服务**一起工作的问题 | 服务发现、配置中心、熔断、「分布式」「微服务」 |

> 💡 **怎么学这个站**：每个模块只要求「认得出」。看到题目里的描述，能选出对应的名字就够了。

> 📌 记法：**Framework 是地基，Boot 是快速盖房，Cloud 是管一片小区。**''',
'''### 课程的贯穿案例：SpringBucks

课程一直在做一个咖啡店程序，叫 **SpringBucks**（模仿星巴克 Starbucks）。题目里看到「咖啡」「订单」「Waiter（服务员）」「Barista（咖啡师）」，都是这个案例里的东西，不用管业务细节。

### 技术趋势（第 03 讲，了解即可）

- **Spring 5** 开始要求 **Java 8** 以上，支持 **Kotlin** 语言，加入了**响应式编程**（WebFlux，后面会讲）。
- 选择依赖的开源组件时，要看它**还有没有人维护**。'''
        ]},
        {'title': 'IoC、Bean 和常用注解', 'cards': [
'''### 两个最基础的词

| 词 | 一句话 |
|---|---|
| **IoC（控制反转）** | 对象不用你自己 new，**交给 Spring 创建和管理** |
| **DI（依赖注入）** | 一个对象需要另一个对象时，**Spring 自动塞给它** |
| **Bean** | **被 Spring 管理的对象**就叫 Bean |
| **容器 / 应用上下文**（ApplicationContext） | 装所有 Bean 的地方 |

> 📌 认准：**IoC = 交给 Spring 管；DI = Spring 自动塞；Bean = 被管的对象。**''',
'''### 常用注解：对号入座

| 看到题目说…… | 就选 |
|---|---|
| 把一个类交给 Spring 管理（通用） | **@Component** |
| 业务层的类 | **@Service** |
| 数据访问层的类 | **@Repository** |
| 处理网页请求的类 | **@Controller** |
| 让 Spring 自动塞一个 Bean 进来 | **@Autowired** |
| 这个类是「配置类」 | **@Configuration** |
| 在配置类里，用方法造一个 Bean | **@Bean** |
| 让 Spring 去扫描某些包，找出带注解的类 | **@ComponentScan** |

- @Service、@Repository、@Controller 其实都是 **@Component 的特殊版本**，只是名字表明了它在哪一层。
- **@SpringBootApplication** 一个顶三个：**@Configuration + @EnableAutoConfiguration + @ComponentScan**（第 13 讲，补充）。'''
        ]},
        {'title': '第一个 Spring 程序', 'cards': [
'''### 用网站生成工程（第 04 讲）

1. 打开 **Spring Initializr**（网址 start.spring.io），勾选需要的功能，比如 **Web**、**Actuator**；
2. 下载生成好的工程，写一个 Controller（处理请求的类）；
3. 直接运行——Spring Boot **自带网页服务器**（默认 Tomcat），不需要另外装。

| 看到题目说…… | 就选 |
|---|---|
| 在线生成 Spring Boot 工程的网站 | **Spring Initializr** |
| 查看程序是否健康的地址 | **/actuator/health**（需要 Actuator 依赖） |
| 统一管理一堆依赖的版本 | **父 POM**（spring-boot-starter-parent）或 **BOM** |
| 把程序打成能直接 `java -jar` 运行的包 | **spring-boot-maven-plugin** 插件 |

> 💡 POM 是 Maven（Java 的依赖管理工具）的配置文件，BOM 是「版本清单」。只要记住：**父 POM / BOM 管版本，maven 插件打可执行 jar。**'''
        ]},
    ],
    'questions': [
        Q('base-p1', '解决服务发现、配置中心、熔断等**分布式**问题的是？', ['Spring Framework', 'Spring Boot', 'Spring Cloud', 'Spring Data'], 2,
          ['它是地基', '它负责快速搭建', '分布式、微服务 → Cloud', '它负责数据访问'], 'Framework 地基，Boot 快速，Cloud 分布式。', lesson=0),
        Q('base-p2', '被 Spring 管理的对象叫什么？', ['Bean', 'POM', 'Starter', 'Jar'], 0,
          ['对', 'POM 是 Maven 配置文件', 'Starter 是起步依赖', 'Jar 是打包文件'], '被管的对象 = Bean。', lesson=1),
        Q('base-p3', '让 Spring 自动把需要的 Bean 塞进来，用哪个注解？', ['@Component', '@Autowired', '@Bean', '@Service'], 1,
          ['它是把类交给 Spring 管', 'Autowired = 自动装配', '它是在配置类里造 Bean', '它是标记业务层'], '自动塞 → @Autowired。', lesson=1),
        Q('base-p4', '在线生成 Spring Boot 工程的网站是？', ['Spring Initializr', 'Maven Central', 'Spring Boot Admin', 'Docker Hub'], 0,
          ['start.spring.io', '那是下载依赖的仓库', '那是监控程序的工具', '那是下载镜像的仓库'], '生成工程 → Initializr。', lesson=2),

        Q('base-1', '提供 IoC、AOP 等**基础能力**的是？', ['Spring Framework', 'Spring Boot', 'Spring Cloud', 'Spring Session'], 0,
          ['地基', 'Boot 是快速搭建', 'Cloud 是分布式', 'Session 是会话共享'], 'Framework = 地基。'),
        Q('base-2', '主打「自动配置、起步依赖、快速运行」的是？', ['Spring Framework', 'Spring Boot', 'Spring Cloud', 'Spring Security'], 1,
          ['地基', '快速搭建 → Boot', '分布式', '安全'], 'Boot = 快速盖房。'),
        Q('base-3', 'IoC（控制反转）的意思是？', ['对象交给 Spring 创建和管理', '把代码倒过来执行', '数据库自动建表', '请求自动转发'], 0,
          ['对', '无关', '无关', '无关'], 'IoC = 交给 Spring 管。'),
        Q('base-4', 'DI（依赖注入）的意思是？', ['一个对象需要别的对象时，由 Spring 自动塞给它', '把数据插入数据库', '向网页注入脚本', '把依赖下载到本地'], 0,
          ['对', '无关', '那是安全攻击', '那是 Maven 的事'], 'DI = Spring 自动塞。'),
        Q('base-5', '标记**数据访问层**的类，通常用？', ['@Service', '@Repository', '@Controller', '@Configuration'], 1,
          ['业务层', 'Repository = 仓库，数据访问层', '处理请求', '配置类'], '分层注解：Controller → Service → Repository。'),
        Q('base-6', '标记**业务层**的类，通常用？', ['@Service', '@Repository', '@Controller', '@Bean'], 0,
          ['Service = 服务，业务层', '数据访问层', '处理请求', '在配置类里造 Bean'], '业务层 → @Service。'),
        Q('base-7', '在 @Configuration 配置类里，用一个**方法**来创建 Bean，方法上贴？', ['@Component', '@Bean', '@Autowired', '@ComponentScan'], 1,
          ['它贴在类上', '方法造 Bean → @Bean', '它是自动塞', '它是扫描包'], '@Bean 贴方法，@Component 贴类。'),
        Q('base-8', '@SpringBootApplication 包含了哪些注解？', ['@Configuration', '@EnableAutoConfiguration', '@ComponentScan', '@Transactional'], [0, 1, 2],
          ['包含', '包含', '包含', '不包含，事务另外贴'], '一个顶三个。'),
        Q('base-9', '@Service、@Repository、@Controller 和 @Component 的关系是？', ['它们都是 @Component 的特殊版本', '它们互相冲突，只能用一个', '它们和 Spring 无关', '只有 @Component 能让 Spring 管理'], 0,
          ['对，只是名字表明所在的层', '不冲突', '都是 Spring 注解', '它们都能让 Spring 管理'], '分层注解都是 @Component。'),
        Q('base-10', '装着所有 Bean 的「容器」，在 Spring 中叫？', ['ApplicationContext（应用上下文）', 'DataSource', 'DispatcherServlet', 'JdbcTemplate'], 0,
          ['对', '数据源', '处理网页请求的入口', '访问数据库的工具'], '容器 = 应用上下文。'),
        Q('base-11', 'Spring Boot 程序不需要另外安装网页服务器，是因为？', ['自带内嵌的网页服务器（默认 Tomcat）', '它不处理网页请求', '它用浏览器当服务器', '它把程序部署到云上'], 0,
          ['对', '它能处理', '无关', '无关'], '内嵌容器，默认 Tomcat。'),
        Q('base-12', '查看 Spring Boot 程序是否健康的默认地址是？', ['/actuator/health', '/health/check', '/status', '/admin'], 0,
          ['需要 Actuator 依赖', '不是', '不是', '不是'], 'Actuator 的健康端点。'),
        Q('base-13', '把 Spring Boot 程序打成可以 `java -jar` 直接运行的包，靠的是？', ['spring-boot-maven-plugin', 'Spring Initializr', 'Actuator', 'Lombok'], 0,
          ['Maven 打包插件', '生成工程的网站', '监控', '减少样板代码的工具'], '打可执行 jar → maven 插件。'),
        Q('base-14', '统一管理多个依赖版本，可以用？', ['父 POM（spring-boot-starter-parent）', 'BOM', 'Actuator', '@Autowired'], [0, 1],
          ['可以', '可以', '它是监控', '它是自动塞'], '父 POM / BOM 管版本。'),
        Q('base-15', 'Spring 5 要求的最低 Java 版本是？', ['Java 6', 'Java 7', 'Java 8', 'Java 11'], 2,
          ['太低', '太低', 'Spring 5 要求 Java 8+', '不是最低要求'], '第 03 讲：Spring 5 基于 Java 8。'),
        TF('base-16', 'Spring 5 加入了对响应式编程（WebFlux）的支持', True, '对', '错', 'Spring 5 的新特性：Java 8、Kotlin、响应式。'),
    ],
}

CHEATSHEET = '''### 初识 Spring（第 01—04、13 讲）

- Framework 地基（IoC、AOP），Boot 快速搭建（自动配置、起步依赖），Cloud 分布式（发现、配置、熔断）。
- IoC = 交给 Spring 管；DI = Spring 自动塞；Bean = 被管的对象；容器 = ApplicationContext。
- 分层注解：@Controller → @Service → @Repository，都是 @Component；@Autowired 自动塞；@Configuration + @Bean 用方法造 Bean。
- @SpringBootApplication = @Configuration + @EnableAutoConfiguration + @ComponentScan。
- start.spring.io = Initializr；/actuator/health 看健康；父 POM / BOM 管版本；spring-boot-maven-plugin 打可执行 jar。Spring 5 要 Java 8+。
'''
