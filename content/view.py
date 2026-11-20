# 模块：常用视图与静态资源（第 46—48 讲）。深度：认得出。
from qhelp import Q, TF

MODULE = {
    'id': 'view', 'title': '常用视图与静态资源：JSON、XML、Thymeleaf', 'short': '视图与静态资源',
    'group': '第六章 Spring MVC 实践', 'exam': '第 46—48 讲',
    'refs': [{'label': 'Spring Boot 2.1 文档 · Web', 'url': 'https://docs.spring.io/spring-boot/docs/2.1.x/reference/html/boot-features-developing-web-applications.html'}],
    'lessons': [
        {'title': 'JSON、XML 和 Thymeleaf', 'cards': [
'''### 返回 JSON / XML（第 46 讲）

- Spring Boot 默认用 **Jackson** 库把对象转成 JSON（自动配置好了）；
- 想返回 **XML**：加 **jackson-dataformat-xml** 依赖；
- 自定义某个类型怎么转成 JSON：用 **@JsonComponent** 写自己的序列化器。

### Thymeleaf：服务端模板（第 47 讲）

**Thymeleaf 是一种「页面模板」，在服务器上把数据填进 HTML 再发给浏览器。**

| 看到题目说…… | 就选 |
|---|---|
| Thymeleaf 的起步依赖 | **spring-boot-starter-thymeleaf** |
| 模板文件默认放在 | **classpath:/templates/** |
| 模板文件默认后缀 | **.html** |
| 开发时改了模板马上看到效果，关闭 | **模板缓存**（spring.thymeleaf.cache=false） |

Controller 返回模板的**名字**，Thymeleaf 找到对应的 HTML 文件，填入数据后返回。'''
        ]},
        {'title': '静态资源与缓存', 'cards': [
'''### 静态资源（第 48 讲）

图片、CSS、JS 这类不变的文件叫**静态资源**。

Spring Boot 默认从这几个目录找静态资源：
**classpath:/static/、/public/、/resources/、/META-INF/resources/**

| 配置 | 作用 |
|---|---|
| spring.mvc.static-path-pattern | 静态资源的访问路径（默认 `/**`） |
| spring.resources.static-locations | 静态资源放在哪些目录 |
| spring.resources.cache.cachecontrol.max-age | 让浏览器缓存多久 |

### HTTP 缓存

通过响应头 **Cache-Control** 告诉浏览器缓存多久，下次不用重新下载。

### 课程建议

实际部署时，静态资源最好交给**专门的设施**，比如 **CDN** 或 **Nginx**，不要都让 Java 程序来提供。'''
        ]},
    ],
    'questions': [
        Q('view-p1', 'Spring Boot 默认用哪个库处理 JSON？', ['Jackson', 'Gson', 'Thymeleaf', 'Lombok'], 0,
          ['对', '另一个 JSON 库，不是默认', '模板引擎', '少写代码的工具'], 'Jackson。', lesson=0),
        Q('view-p2', 'Spring Boot 默认的静态资源目录包括？', ['classpath:/static/', 'classpath:/public/', 'classpath:/templates/', 'classpath:/resources/'], [0, 1, 3],
          ['是', '是', '那是 Thymeleaf 模板目录', '是'], 'templates 放模板，不放静态资源。', lesson=1),

        Q('view-1', '让 Spring MVC 返回 XML，需要加的依赖是？', ['jackson-dataformat-xml', 'spring-boot-starter-thymeleaf', 'lombok', 'druid'], 0,
          ['对', '模板', '无关', '连接池'], 'jackson-dataformat-xml。'),
        Q('view-2', '自定义某个类型的 JSON 序列化方式，可以用？', ['@JsonComponent', '@Component', '@RestController', '@Entity'], 0,
          ['对', '通用的', 'Web', 'JPA'], '@JsonComponent。'),
        Q('view-3', 'Thymeleaf 是什么？', ['服务端页面模板引擎', 'JSON 库', '连接池', '数据库'], 0,
          ['对', '不是', '不是', '不是'], '把数据填进 HTML。'),
        Q('view-4', 'Thymeleaf 模板文件默认放在？', ['classpath:/templates/', 'classpath:/static/', 'classpath:/public/', 'WEB-INF/'], 0,
          ['对', '静态资源', '静态资源', '不是默认'], 'templates。'),
        Q('view-5', '开发时修改 Thymeleaf 模板后想立即生效，应该？', ['关闭模板缓存', '打开模板缓存', '重装 JDK', '删除静态资源'], 0,
          ['spring.thymeleaf.cache=false', '反了', '无关', '无关'], '开发时关缓存。'),
        Q('view-6', '告诉浏览器资源可以缓存多久的 HTTP 响应头是？', ['Cache-Control', 'Content-Type', 'Accept', 'Host'], 0,
          ['对', '内容类型', '客户端想要的格式', '主机'], 'Cache-Control。'),
        Q('view-7', '课程建议，生产环境中的静态资源最好由谁提供？', ['CDN 或 Nginx 等专门设施', 'Java 程序', '数据库', 'Redis'], 0,
          ['对', '不推荐', '不合适', '不合适'], '第 48 讲。'),
        Q('view-8', 'Thymeleaf 的起步依赖是？', ['spring-boot-starter-thymeleaf', 'spring-boot-starter-web', 'thymeleaf-spring-boot-starter', 'spring-boot-starter-json'], 0,
          ['官方起步依赖：spring-boot-starter-xxx', 'Web', '命名不对', 'JSON'], '官方的以 spring-boot-starter 开头。'),
        Q('view-9', '设置静态资源**访问路径**的配置是？', ['spring.mvc.static-path-pattern', 'spring.resources.static-locations', 'server.port', 'spring.thymeleaf.cache'], 0,
          ['path pattern = 路径模式', '存放目录', '端口', '模板缓存'], 'path-pattern 访问路径，locations 存放目录。'),
        TF('view-10', 'Thymeleaf 中 Controller 返回的是模板的名字，而不是 JSON 数据', True, '对', '错', '返回模板名，由 Thymeleaf 渲染。'),
    ],
}

CHEATSHEET = '''### 视图与静态资源（第 46—48 讲）

- JSON 默认 Jackson；XML 加 jackson-dataformat-xml；@JsonComponent 自定义序列化。
- Thymeleaf：spring-boot-starter-thymeleaf，模板在 classpath:/templates/，后缀 .html，开发时 spring.thymeleaf.cache=false。
- 静态资源目录：/static、/public、/resources、/META-INF/resources；static-path-pattern 访问路径，static-locations 目录；Cache-Control 缓存；生产交给 CDN / Nginx。
'''
