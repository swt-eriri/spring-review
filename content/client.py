# 模块：访问 Web 资源（第 53—57 讲）。深度：认得出。
from qhelp import Q, TF

MODULE = {
    'id': 'client', 'title': '访问 Web 资源：RestTemplate 与 WebClient', 'short': 'HTTP 客户端',
    'group': '第七章 访问 Web 资源', 'exam': '第 53—57 讲',
    'refs': [{'label': 'Spring Boot 2.1 文档 · 调用 REST 服务', 'url': 'https://docs.spring.io/spring-boot/docs/2.1.x/reference/html/boot-features-resttemplate.html'}],
    'lessons': [
        {'title': 'RestTemplate：同步调用别的服务', 'cards': [
'''### 一句话

**RestTemplate = 在 Java 程序里调用别人的网络接口（HTTP）的工具。**它是**同步、阻塞**的：发出请求后一直等到结果回来。

> ⚠️ Spring Boot **不会自动创建** RestTemplate，但会提供 **RestTemplateBuilder**，用它来创建。

### 方法对号入座

| 看到题目说…… | 就选 |
|---|---|
| GET 请求，直接拿到对象 | **getForObject()** |
| GET 请求，拿到带状态码、响应头的完整响应 | **getForEntity()** |
| POST 请求 | **postForObject() / postForEntity()** |
| PUT / DELETE | **put() / delete()** |
| 最灵活，可以自定义请求方法和请求头 | **exchange()** |

> 💡 记法：**ForObject 只要内容；ForEntity 要完整响应（ResponseEntity）。**''',
'''### 高级用法（第 54 讲）

| 看到题目说…… | 就选 |
|---|---|
| 构造一个带请求头的完整请求 | **RequestEntity** |
| 完整的响应（状态码 + 响应头 + 内容） | **ResponseEntity** |
| 拼接网址 | **UriComponentsBuilder** |
| 返回值是 `List<Coffee>` 这种**泛型**类型 | **ParameterizedTypeReference** |

### 定制 RestTemplate（第 55 讲）

RestTemplate 底层真正发请求的 HTTP 库可以换：

| 底层 | 对应的工厂类 |
|---|---|
| JDK 自带（默认） | SimpleClientHttpRequestFactory |
| **Apache HttpClient** | **HttpComponentsClientHttpRequestFactory** |
| OkHttp | OkHttp3ClientHttpRequestFactory |

换底层后可以配置**连接池**、**连接超时**、**读取超时**。

> ⚠️ 一定要设超时：下游服务很慢时，不设超时会把自己的线程全部卡住。'''
        ]},
        {'title': 'WebClient：响应式的非阻塞客户端', 'cards': [
'''### 一句话

**WebClient = 非阻塞、响应式的 HTTP 客户端**（Spring 5 新增），返回 **Mono / Flux**（Reactor 模块讲过）。

| | RestTemplate | WebClient |
|---|---|---|
| 方式 | 同步、阻塞 | **异步、非阻塞** |
| 返回 | 普通对象 | **Mono / Flux** |
| 底层（默认） | JDK HttpURLConnection | **Reactor Netty** |

写法认关键词：`WebClient.create()` 或 `WebClient.builder()` 创建 → `.get().uri(...)` → **`.retrieve()`** 取响应 → **`bodyToMono()` / `bodyToFlux()`** 转成结果。

### SpringBucks 进度（第 57 讲）

新增 **Customer Service（顾客服务）**，用 HTTP 客户端去调用 Waiter Service：**获取菜单、创建订单**。

> 📌 认准：**RestTemplate 同步阻塞；WebClient 非阻塞、返回 Mono / Flux。**'''
        ]},
    ],
    'questions': [
        Q('client-p1', 'Spring Boot 中创建 RestTemplate 推荐用？', ['RestTemplateBuilder', 'new 一个 DataSource', 'WebClient', 'JdbcTemplate'], 0,
          ['Boot 不自动建 RestTemplate，但提供 Builder', '无关', '另一个客户端', '无关'], 'RestTemplateBuilder。', lesson=0),
        Q('client-p2', '非阻塞、返回 Mono / Flux 的 HTTP 客户端是？', ['WebClient', 'RestTemplate', 'JdbcTemplate', 'Feign'], 0,
          ['对', '同步阻塞', '数据库', '声明式客户端（后面讲）'], 'WebClient。', lesson=1),

        Q('client-1', 'RestTemplate 发 GET 请求并**直接拿到对象**，用？', ['getForObject()', 'getForEntity()', 'exchange()', 'postForObject()'], 0,
          ['只要内容', '完整响应', '最灵活', 'POST'], 'ForObject 只要内容。'),
        Q('client-2', 'RestTemplate 发 GET 请求，需要拿到**状态码和响应头**，用？', ['getForEntity()', 'getForObject()', 'put()', 'delete()'], 0,
          ['返回 ResponseEntity', '只有内容', 'PUT', 'DELETE'], 'ForEntity 要完整响应。'),
        Q('client-3', 'RestTemplate 中最灵活、可自定义请求方法和请求头的方法是？', ['exchange()', 'getForObject()', 'postForEntity()', 'put()'], 0,
          ['对', '只能 GET', '只能 POST', '只能 PUT'], 'exchange。'),
        Q('client-4', '包含状态码、响应头和内容的完整响应对象是？', ['ResponseEntity', 'RequestEntity', 'Mono', 'RowMapper'], 0,
          ['响应', '请求', '响应式类型', 'JDBC'], 'Request 请求，Response 响应。'),
        Q('client-5', '返回值是 `List<Coffee>` 这种泛型类型时，RestTemplate 需要借助？', ['ParameterizedTypeReference', 'UriComponentsBuilder', 'RequestEntity', 'RowMapper'], 0,
          ['对', '拼网址', '构造请求', 'JDBC'], 'ParameterizedTypeReference。'),
        Q('client-6', '拼接请求网址，可以用？', ['UriComponentsBuilder', 'RestTemplateBuilder', 'WebClient', 'ResponseEntity'], 0,
          ['Uri = 网址', '创建 RestTemplate', '另一个客户端', '响应'], 'UriComponentsBuilder。'),
        Q('client-7', '让 RestTemplate 底层使用 Apache HttpClient，用哪个工厂类？', ['HttpComponentsClientHttpRequestFactory', 'SimpleClientHttpRequestFactory', 'OkHttp3ClientHttpRequestFactory', 'ConnectionFactory'], 0,
          ['HttpComponents 是 Apache HttpClient 的项目名', 'JDK 默认', 'OkHttp', 'R2DBC'], '认 HttpComponents。'),
        Q('client-8', '定制 RestTemplate 时，通常要设置哪些？', ['连接池', '连接超时', '读取超时', '数据库隔离级别'], [0, 1, 2],
          ['要', '要', '要', '无关'], '超时一定要设。'),
        Q('client-9', '调用的下游服务很慢、又没设超时，会出现什么问题？', ['调用方的线程被大量占住', '下游自动变快', '数据库自动回滚', '没有影响'], 0,
          ['对', '不会', '无关', '有影响'], '第 55 讲。'),
        Q('client-10', 'WebClient 中把响应体转成 Mono 的方法是？', ['bodyToMono()', 'getForObject()', 'subscribe()', 'block()'], 0,
          ['对', 'RestTemplate 的', '订阅', '阻塞等待'], 'bodyToMono / bodyToFlux。'),
        Q('client-11', 'WebClient 默认的底层是？', ['Reactor Netty', 'JDK HttpURLConnection', 'Apache HttpClient', 'Tomcat'], 0,
          ['对', 'RestTemplate 默认', '可选', '服务器'], 'Reactor Netty。'),
        TF('client-12', 'Spring Boot 会自动创建一个 RestTemplate Bean', False, '错', '对：只提供 RestTemplateBuilder', '需要自己用 Builder 建。'),
        TF('client-13', 'RestTemplate 是同步阻塞的', True, '对', '错', '发出请求后等结果回来。'),
        Q('client-14', 'SpringBucks 中新增的 Customer Service 用 HTTP 客户端做了什么？', ['获取菜单', '创建订单', '直接改数据库', '发送邮件'], [0, 1],
          ['对', '对', '不是', '不是'], '第 57 讲。'),
    ],
}

CHEATSHEET = '''### HTTP 客户端（第 53—57 讲）

- **RestTemplate** 同步阻塞；Boot 不自动建，用 **RestTemplateBuilder**。
- getForObject 只要内容，getForEntity 要完整响应（ResponseEntity）；postForObject / put / delete；**exchange** 最灵活。
- RequestEntity 构造请求，UriComponentsBuilder 拼网址，ParameterizedTypeReference 处理泛型。
- 底层换 Apache HttpClient：HttpComponentsClientHttpRequestFactory；配连接池、连接 / 读取超时（下游慢会卡住线程）。
- **WebClient** 非阻塞，返回 Mono / Flux，底层 Reactor Netty；retrieve() → bodyToMono / bodyToFlux。
'''
