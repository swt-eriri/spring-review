# 模块：Web 开发进阶（第 58—66 讲）。深度：认得出。状态码、幂等性按 HTTP 规范补充。
from qhelp import Q, TF

MODULE = {
    'id': 'rest', 'title': 'Web 进阶：REST、HATEOAS、分布式 Session、WebFlux', 'short': 'REST 与 WebFlux',
    'group': '第八章 Web 开发进阶', 'exam': '第 58—66 讲',
    'refs': [{'label': 'Richardson 成熟度模型（Martin Fowler）', 'url': 'https://martinfowler.com/articles/richardsonMaturityModel.html'}],
    'lessons': [
        {'title': 'RESTful：成熟度模型、方法、状态码', 'cards': [
'''### 一句话

**REST 是一种设计网络接口的风格：把东西看成「资源」，用网址表示资源，用 HTTP 方法表示操作。**

### Richardson 成熟度模型：四个等级（必背）

| 等级 | 名字 | 一句话 |
|---|---|---|
| Level 0 | POX（普通 XML / RPC） | 一个网址干所有事 |
| Level 1 | **资源** | 不同资源用不同网址 |
| Level 2 | **HTTP 方法** | 用 GET / POST / PUT / DELETE 表示不同操作 |
| Level 3 | **超媒体控制（HATEOAS）** | 响应里带上「接下来能做什么」的链接 |

### 网址设计

- 用**名词**表示资源，不用动词：`/coffee` 而不是 `/getCoffee`；
- 资源一般用**复数**，有层级：`/customers/1/orders`。''',
'''### HTTP 方法：安全和幂等（必背）

- **安全**：不会修改数据（只读）；
- **幂等**：做一次和做多次，**结果一样**。

| 方法 | 用途 | 安全 | 幂等 |
|---|---|---|---|
| **GET** | 查询 | 是 | 是 |
| **POST** | 新建 | 否 | **否** |
| **PUT** | 整体更新（替换） | 否 | 是 |
| **DELETE** | 删除 | 否 | 是 |
| PATCH | 部分更新 | 否 | 否 |
| HEAD / OPTIONS | 只要响应头 / 问支持哪些方法 | 是 | 是 |

> 📌 记法：**只有 GET（和 HEAD、OPTIONS）是安全的；POST 和 PATCH 不幂等，其他都幂等。**

### 常用状态码

| 状态码 | 意思 |
|---|---|
| **200** OK | 成功 |
| **201** Created | 新建成功 |
| 204 No Content | 成功，但没有返回内容 |
| 304 Not Modified | 内容没变，用缓存 |
| **400** Bad Request | 请求有错 |
| **401** Unauthorized | **没登录**（没认证） |
| **403** Forbidden | 登录了但**没权限** |
| **404** Not Found | 找不到 |
| 405 Method Not Allowed | 不支持这个请求方法 |
| **500** Internal Server Error | 服务器内部出错 |

> 💡 2 开头成功，3 开头重定向/缓存，**4 开头是客户端的错，5 开头是服务器的错**。'''
        ]},
        {'title': 'HATEOAS 和 Spring Data REST', 'cards': [
'''### HATEOAS（第 60 讲）

**HATEOAS = 服务端在返回的数据里附上链接，告诉客户端「接下来可以做什么」**，客户端顺着链接走就行，不用提前写死网址。它是成熟度模型的**最高级（Level 3）**。

### HAL：表示链接的一种格式

HAL（Hypertext Application Language）用两个特殊字段：
- **_links**：链接；
- **_embedded**：嵌入的其他资源。

### Spring Data REST（第 61、62 讲）

**把 Repository 直接暴露成 REST 接口，不用自己写 Controller。**

| 看到题目说…… | 就选 |
|---|---|
| 起步依赖 | **spring-boot-starter-data-rest** |
| 自定义暴露的路径 | **@RepositoryRestResource** |
| 返回格式 | 默认 **HAL** |
| 自定义查询方法会出现在 | **/search** 路径下 |

客户端（第 62 讲）配置好 HAL 解析，就可以读取响应里的链接，顺着链接访问、修改资源。'''
        ]},
        {'title': '分布式 Session 和 WebFlux', 'cards': [
'''### 分布式环境的 Session 问题（第 63 讲）

Session 用来记住「用户是谁」（如登录状态）。程序部署在**多台机器**上时，用户这次访问 A、下次访问 B，B 不认识他。三种解决办法：

| 方案 | 一句话 |
|---|---|
| **粘性会话**（Sticky Session） | 让同一个用户**总是访问同一台**机器 |
| **会话复制**（Session Replication） | 各台机器之间**互相复制** Session |
| **集中存储**（Session 集中化） | Session 统一存到 **Redis** 等外部存储，大家都去那里读 |

**Spring Session** 就是用来做集中存储的：支持 **Redis**、JDBC、Hazelcast 等；用 Redis 时开启注解 **@EnableRedisHttpSession**。

### WebFlux：用响应式代替 Spring MVC（第 64—66 讲）

| | Spring MVC | **WebFlux** |
|---|---|---|
| 模型 | 阻塞，一个请求占一个线程 | **非阻塞**，基于 Reactor（Mono / Flux） |
| 默认服务器 | Tomcat | **Netty** |
| 优点 | 简单、生态成熟 | **用很少的线程扛更多并发** |

- WebFlux **不一定让单个请求更快**，好处是同样资源下能处理更多请求；
- 整条链路都要是非阻塞的才有意义（数据库要用 R2DBC 等）；
- 写法可以和 MVC 一样用 @RestController 注解，也可以用**函数式**的 RouterFunction。'''
        ]},
    ],
    'questions': [
        Q('rest-p1', 'Richardson 成熟度模型中，引入 HTTP 方法（GET、POST 等）表示操作的是第几级？', ['Level 0', 'Level 1', 'Level 2', 'Level 3'], 2,
          ['一个网址干所有事', '资源', 'HTTP 方法', '超媒体'], '0 RPC → 1 资源 → 2 方法 → 3 超媒体。', lesson=0),
        Q('rest-p2', '下列 HTTP 方法中**不是幂等**的是？', ['POST', 'GET', 'PUT', 'DELETE'], 0,
          ['新建，做两次会新建两个', '幂等', '幂等', '幂等'], 'POST、PATCH 不幂等。', lesson=0),
        Q('rest-p3', '把 Repository 直接暴露为 REST 接口的是？', ['Spring Data REST', 'Spring Session', 'WebFlux', 'RestTemplate'], 0,
          ['对', '会话共享', '响应式 Web', 'HTTP 客户端'], 'Spring Data REST。', lesson=1),
        Q('rest-p4', '把 Session 统一存到 Redis 中，用？', ['Spring Session', 'Spring Data REST', 'Spring Cache', 'Spring Cloud Stream'], 0,
          ['对', '暴露 Repository', '缓存', '消息'], 'Spring Session。', lesson=2),

        Q('rest-1', 'Richardson 成熟度模型的最高级（Level 3）是？', ['超媒体控制（HATEOAS）', '资源', 'HTTP 方法', 'POX'], 0,
          ['对', 'Level 1', 'Level 2', 'Level 0'], 'Level 3 = HATEOAS。'),
        Q('rest-2', 'RESTful 网址设计，下列更合适的是？', ['/coffee', '/getCoffee', '/deleteCoffeeById', '/doQuery'], 0,
          ['名词', '网址里不放动词', '网址里不放动词', '网址里不放动词'], '用名词，操作交给 HTTP 方法。'),
        Q('rest-3', '下列 HTTP 方法中，属于**安全**方法（不修改数据）的是？', ['GET', 'HEAD', 'POST', 'DELETE'], [0, 1],
          ['只读', '只要响应头', '会新建', '会删除'], '还有 OPTIONS。'),
        Q('rest-4', '下列哪些 HTTP 方法是**幂等**的？', ['GET', 'PUT', 'DELETE', 'POST'], [0, 1, 2],
          ['是', '是', '是', '不是'], 'POST、PATCH 不幂等。'),
        Q('rest-5', '新建资源成功，通常返回状态码？', ['201', '200', '204', '404'], 0,
          ['Created', '一般成功', '无内容', '找不到'], '201 Created。'),
        Q('rest-6', '用户**没有登录**（未认证），返回状态码？', ['401', '403', '404', '500'], 0,
          ['Unauthorized', '登录了但没权限', '找不到', '服务器错误'], '401 没登录，403 没权限。'),
        Q('rest-7', '用户登录了，但**没有权限**访问，返回状态码？', ['403', '401', '400', '405'], 0,
          ['Forbidden', '没登录', '请求有错', '方法不支持'], '403。'),
        Q('rest-8', '服务器内部出错，返回状态码？', ['500', '400', '404', '304'], 0,
          ['5 开头是服务器错', '4 开头是客户端错', '找不到', '没变化'], '500。'),
        Q('rest-9', '状态码 4 开头表示？', ['客户端的错误', '服务器的错误', '成功', '重定向'], 0,
          ['对', '那是 5 开头', '那是 2 开头', '那是 3 开头'], '4 客户端，5 服务器。'),
        Q('rest-10', 'HATEOAS 的核心思想是？', ['响应里带上链接，告诉客户端接下来能做什么', '所有接口只用 POST', '把数据都缓存起来', '用 XML 代替 JSON'], 0,
          ['对', '不是', '不是', '不是'], '超媒体驱动。'),
        Q('rest-11', 'HAL 格式中，表示链接的字段是？', ['_links', '_embedded', 'href', 'data'], 0,
          ['对', '嵌入的资源', '链接里的地址字段，不是 HAL 的顶层字段', '不是'], '_links 链接，_embedded 嵌入。'),
        Q('rest-12', 'Spring Data REST 中自定义 Repository 暴露路径的注解是？', ['@RepositoryRestResource', '@RestController', '@RequestMapping', '@Repository'], 0,
          ['对', '自己写 Controller 时用', '自己写 Controller 时用', '数据层标记'], '@RepositoryRestResource。'),
        Q('rest-13', 'Spring Data REST 中，Repository 的自定义查询方法出现在哪个路径下？', ['/search', '/query', '/find', '/api'], 0,
          ['对', '不是', '不是', '不是'], '/search。'),
        Q('rest-14', '让同一个用户总是访问同一台机器的 Session 方案是？', ['粘性会话', '会话复制', '集中存储', 'HATEOAS'], 0,
          ['Sticky = 粘', '互相复制', '存到 Redis', '无关'], '粘性会话。'),
        Q('rest-15', '分布式环境中解决 Session 问题的方案有？', ['粘性会话', '会话复制', '集中存储（如 Redis）', '把 Session 存在浏览器地址栏'], [0, 1, 2],
          ['是', '是', '是', '不是'], '三种方案。'),
        Q('rest-16', 'Spring Session 使用 Redis 时开启的注解是？', ['@EnableRedisHttpSession', '@EnableCaching', '@EnableRedisRepositories', '@EnableWebFlux'], 0,
          ['对', '缓存', 'Redis Repository', 'WebFlux'], '@EnableRedisHttpSession。'),
        Q('rest-17', 'WebFlux 默认使用的服务器是？', ['Netty', 'Tomcat', 'Jetty', 'Nginx'], 0,
          ['对', 'MVC 默认', '另一种容器', '反向代理'], 'WebFlux → Netty。'),
        Q('rest-18', '关于 WebFlux，下列说法正确的是？', ['基于非阻塞和响应式流', '一定让每个请求都更快', '必须配合阻塞的 JDBC 使用', '不能使用 @RestController'], 0,
          ['对', '不一定，好处是并发', '应该全链路非阻塞', '可以使用'], 'WebFlux：非阻塞、少线程扛高并发。'),
        Q('rest-19', 'WebFlux 除了注解方式，还支持哪种写法？', ['函数式路由（RouterFunction）', 'XML 配置路由', 'SQL 路由', '只支持注解'], 0,
          ['对', '不是', '不是', '不是'], 'RouterFunction。'),
        TF('rest-20', '使用 WebFlux 后，单个请求的处理速度一定比 Spring MVC 快', False, '错', '对：不一定，优势在于用更少线程处理更多并发', '第 64 讲。'),
    ],
}

CHEATSHEET = '''### REST 与 WebFlux（第 58—66 讲）

- 成熟度：0 POX → 1 资源 → 2 HTTP 方法 → **3 超媒体（HATEOAS）**。网址用名词复数、分层级。
- **安全**：GET、HEAD、OPTIONS；**不幂等**：POST、PATCH（其余幂等）。
- 状态码：200 成功，201 新建，204 无内容，304 没变，400 请求错，**401 没登录，403 没权限**，404，405，500。4 客户端错，5 服务器错。
- HATEOAS 响应带链接；HAL：_links、_embedded。Spring Data REST：spring-boot-starter-data-rest，@RepositoryRestResource，/search。
- Session：粘性会话 / 会话复制 / 集中存储；Spring Session + Redis，@EnableRedisHttpSession。
- WebFlux：非阻塞、Reactor、默认 Netty；不一定更快，少线程高并发；全链路非阻塞（R2DBC）；注解或 RouterFunction。
'''
