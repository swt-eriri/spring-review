# 模块：Spring MVC 机制（第 39—45、49—52 讲）。深度：认得出。
from qhelp import Q, TF

MODULE = {
    'id': 'mvc', 'title': 'Spring MVC：请求怎么被处理', 'short': 'Spring MVC',
    'group': '第六章 Spring MVC 实践', 'exam': '第 39—45、49—52 讲',
    'refs': [{'label': 'Spring 5.3 文档 · Web MVC', 'url': 'https://docs.spring.io/spring-framework/docs/5.3.x/reference/html/web.html#mvc'}],
    'lessons': [
        {'title': 'DispatcherServlet 和 Controller', 'cards': [
'''### 一句话

**Spring MVC 是 Spring 处理网页请求的框架。所有请求先到一个总入口 DispatcherServlet，再由它分派给对应的 Controller。**

DispatcherServlet 就像前台：自己不干活，负责把请求转给合适的人。

### 前台身边的几个帮手（认名字）

| 看到题目说…… | 就选 |
|---|---|
| 根据网址找到该由哪个方法处理 | **HandlerMapping**（映射） |
| 真正去调用那个处理方法 | **HandlerAdapter**（适配器） |
| 处理过程中出了异常，负责处理异常 | **HandlerExceptionResolver** |
| 把视图名字解析成真正的页面 | **ViewResolver**（视图解析器） |
| 处理文件上传 | **MultipartResolver** |
| 处理语言、地区 | LocaleResolver |''',
'''### Controller 常用注解（必背）

| 看到题目说…… | 就选 |
|---|---|
| 处理请求的类 | **@Controller** |
| 处理请求并**直接返回数据**（如 JSON） | **@RestController** = @Controller + @ResponseBody |
| 把网址映射到方法 | **@RequestMapping** |
| 只处理 GET / POST / PUT / DELETE 请求 | **@GetMapping / @PostMapping / @PutMapping / @DeleteMapping** |
| 方法返回值直接当响应内容 | **@ResponseBody** |
| 把请求体（如 JSON）转成对象 | **@RequestBody** |
| 取网址路径里的变量，如 /coffee/**{id}** | **@PathVariable** |
| 取网址问号后的参数，如 ?name=latte | **@RequestParam** |
| 取请求头 | **@RequestHeader** |
| 指定返回的 HTTP 状态码 | **@ResponseStatus** |

@RequestMapping 还可以按 **请求方法、参数、请求头、consumes（接收什么格式）、produces（返回什么格式）** 来限定。'''
        ]},
        {'title': '应用上下文和请求处理流程', 'cards': [
'''### 父子上下文（第 40 讲）

Web 程序里可能有两层「容器」：

- **父上下文（根上下文）**：放 Service、Repository 等；
- **子上下文（DispatcherServlet 的）**：放 Controller 等 Web 相关的。

规则：**子能看到父里的 Bean，父看不到子的。**

> ⚠️ 切面（AOP）只对**同一个上下文**里的 Bean 生效。切面放错了上下文，就会「不起作用」。

### 一个请求的处理顺序（第 41 讲）

1. 请求到达 **DispatcherServlet**；
2. 通过 **HandlerMapping** 找到处理方法（连同拦截器）；
3. 找到能调用它的 **HandlerAdapter**；
4. 执行拦截器的 **preHandle**；
5. 调用 Controller 方法；
6. 执行拦截器的 **postHandle**；
7. 处理返回值：解析视图并渲染，或者处理异常；
8. 执行拦截器的 **afterCompletion**。

> 📌 记顺序：**前台 → 找人（Mapping）→ 找调用方式（Adapter）→ 干活 → 出结果（视图 / 异常）。**'''
        ]},
        {'title': '参数转换、校验、视图和异常', 'cards': [
'''### 参数处理（第 43 讲）

| 看到题目说…… | 就选 |
|---|---|
| 把字符串参数转换成别的类型 | **Converter**（转换器）/ **Formatter**（格式化器） |
| 校验参数（如不能为空） | **@Valid** + 校验注解（@NotNull、@NotEmpty、@Min……） |
| 拿到校验结果（哪里不合格） | **BindingResult** |
| 接收上传的文件 | **MultipartFile** |

Spring Boot 会**自动注册**你写好的 Converter、Formatter Bean。

### 视图与返回值（第 44、45 讲）

- 返回**页面**：返回一个视图名，**ViewResolver** 把名字解析成 **View**，再渲染出页面；
- 返回**数据**（@ResponseBody）：由 **HttpMessageConverter**（消息转换器）把对象转成 JSON / XML；
- 根据请求想要的格式选择返回格式，叫**内容协商**；
- 视图名前加 **redirect:** 是重定向，加 **forward:** 是转发。

> 📌 认准：**返回页面靠 ViewResolver；返回 JSON 靠 HttpMessageConverter。**''',
'''### 异常处理（第 49 讲）

DispatcherServlet 把异常交给 **HandlerExceptionResolver** 处理。写法：

| 看到题目说…… | 就选 |
|---|---|
| 在 Controller 里写一个处理异常的方法 | **@ExceptionHandler** |
| **集中**处理所有 Controller 的异常 | **@ControllerAdvice**（返回数据用 **@RestControllerAdvice**） |

### 拦截器（第 50 讲）

**HandlerInterceptor** 在请求处理的三个时机插入逻辑：

| 方法 | 时机 |
|---|---|
| **preHandle** | 处理**之前**（返回 false 就不往下走了） |
| **postHandle** | 处理**之后**、渲染视图之前 |
| **afterCompletion** | **整个请求完成**之后（包括渲染完） |

注册拦截器：实现 **WebMvcConfigurer** 的 **addInterceptors** 方法。异步请求用 AsyncHandlerInterceptor。

### 课程答疑（第 52 讲）

从 H2 内存数据库换到 MySQL：改依赖和连接配置；**生产环境慎用自动建表**（ddl-auto）。'''
        ]},
    ],
    'questions': [
        Q('mvc-p1', 'Spring MVC 中所有请求的总入口是？', ['DispatcherServlet', 'HandlerMapping', 'ViewResolver', 'Controller'], 0,
          ['前台', '找处理方法', '解析视图', '具体干活的'], '总入口 DispatcherServlet。', lesson=0),
        Q('mvc-p2', '@RestController 相当于？', ['@Controller + @ResponseBody', '@Controller + @Service', '@Component + @Bean', '@RequestMapping + @GetMapping'], 0,
          ['对', '不是', '不是', '不是'], '直接返回数据。', lesson=0),
        Q('mvc-p3', '父子上下文中，下列说法正确的是？', ['子上下文能访问父上下文的 Bean', '父上下文能访问子上下文的 Bean', '两者互相都能访问', '两者互相都不能访问'], 0,
          ['对', '反了', '父看不到子', '子能看到父'], '子看父，父看不到子。', lesson=1),
        Q('mvc-p4', '集中处理所有 Controller 异常的注解是？', ['@ControllerAdvice', '@ExceptionHandler', '@ResponseStatus', '@Valid'], 0,
          ['集中', '单个方法', '状态码', '校验'], '@ControllerAdvice 集中处理。', lesson=2),

        Q('mvc-1', '根据请求网址找到对应处理方法的组件是？', ['HandlerMapping', 'HandlerAdapter', 'ViewResolver', 'MultipartResolver'], 0,
          ['Mapping = 映射', '负责调用', '视图', '文件上传'], '找人 Mapping，调用 Adapter。'),
        Q('mvc-2', '负责真正调用处理方法的组件是？', ['HandlerAdapter', 'HandlerMapping', 'HandlerExceptionResolver', 'LocaleResolver'], 0,
          ['Adapter = 适配器', '找方法', '异常', '语言地区'], 'HandlerAdapter。'),
        Q('mvc-3', '处理文件上传的组件是？', ['MultipartResolver', 'ViewResolver', 'LocaleResolver', 'HandlerMapping'], 0,
          ['Multipart = 多部分（上传文件的格式）', '视图', '语言', '映射'], 'MultipartResolver。'),
        Q('mvc-4', '获取网址 `/coffee/{id}` 中的 id，用？', ['@PathVariable', '@RequestParam', '@RequestBody', '@RequestHeader'], 0,
          ['路径变量', '问号后的参数', '请求体', '请求头'], '路径里 → @PathVariable。'),
        Q('mvc-5', '获取网址 `?name=latte` 中的 name，用？', ['@RequestParam', '@PathVariable', '@RequestBody', '@ResponseBody'], 0,
          ['请求参数', '路径变量', '请求体', '响应体'], '问号后 → @RequestParam。'),
        Q('mvc-6', '把请求中的 JSON 转成 Java 对象，用？', ['@RequestBody', '@ResponseBody', '@RequestParam', '@PathVariable'], 0,
          ['请求体', '响应体', '参数', '路径变量'], 'Request 进，Response 出。'),
        Q('mvc-7', '只处理 POST 请求的映射注解是？', ['@PostMapping', '@GetMapping', '@PutMapping', '@RequestBody'], 0,
          ['对', 'GET', 'PUT', '请求体'], 'Get / Post / Put / DeleteMapping。'),
        Q('mvc-8', '@RequestMapping 可以根据哪些条件限定映射？', ['请求路径', 'HTTP 方法', '请求头', 'produces / consumes（媒体类型）'], [0, 1, 2, 3],
          ['可以', '可以', '可以', '可以'], '还有请求参数。'),
        Q('mvc-9', '切面放在父上下文还是子上下文会影响它是否生效，原因是？', ['切面只对同一个上下文里的 Bean 生效', '切面只能放在父上下文', '切面只能放在子上下文', '切面与上下文无关'], 0,
          ['对', '不是', '不是', '有关'], '第 40 讲。'),
        Q('mvc-10', '拦截器中，在 Controller 方法**执行之前**调用的是？', ['preHandle', 'postHandle', 'afterCompletion', 'proceed'], 0,
          ['pre = 之前', '之后', '全部完成后', 'AOP 的'], 'pre 前，post 后，afterCompletion 完成后。'),
        Q('mvc-11', '拦截器中，**整个请求完成（视图渲染完）之后**调用的是？', ['afterCompletion', 'postHandle', 'preHandle', 'destroy'], 0,
          ['Completion = 完成', '处理后、渲染前', '处理前', '不是'], 'afterCompletion。'),
        TF('mvc-12', '拦截器的 preHandle 返回 false 时，请求不再继续往下处理', True, '对', '错', 'preHandle 返回 false 就拦下。'),
        Q('mvc-13', '注册拦截器，要实现 WebMvcConfigurer 的哪个方法？', ['addInterceptors', 'addFormatters', 'addResourceHandlers', 'configureViewResolvers'], 0,
          ['Interceptor = 拦截器', '注册格式化器', '静态资源', '视图解析器'], 'addInterceptors。'),
        Q('mvc-14', '参数校验时，拿到「哪里校验没通过」的结果用？', ['BindingResult', 'MultipartFile', 'Converter', 'ModelAndView'], 0,
          ['对', '上传文件', '类型转换', '模型和视图'], '@Valid + BindingResult。'),
        Q('mvc-15', '触发参数校验的注解是？', ['@Valid', '@RequestBody', '@ResponseStatus', '@ExceptionHandler'], 0,
          ['对', '请求体', '状态码', '异常'], '@Valid。'),
        Q('mvc-16', '接收上传文件的参数类型是？', ['MultipartFile', 'BindingResult', 'String', 'Converter'], 0,
          ['对', '校验结果', '不对', '转换器'], 'MultipartFile。'),
        Q('mvc-17', '把逻辑视图名解析成真正的视图的是？', ['ViewResolver', 'HttpMessageConverter', 'HandlerAdapter', 'Converter'], 0,
          ['视图解析器', '它负责把对象转成 JSON 等', '调用方法', '参数转换'], '页面 ViewResolver，数据 HttpMessageConverter。'),
        Q('mvc-18', '@ResponseBody 方法返回的对象被转换成 JSON，靠的是？', ['HttpMessageConverter', 'ViewResolver', 'Formatter', 'LocaleResolver'], 0,
          ['消息转换器', '视图', '格式化参数', '语言'], 'HttpMessageConverter。'),
        Q('mvc-19', 'Controller 返回 `"redirect:/coffee"` 的效果是？', ['重定向到 /coffee', '转发到 /coffee', '返回字符串 redirect:/coffee', '报错'], 0,
          ['redirect = 重定向', '转发是 forward:', '前缀会被识别', '不报错'], 'redirect: 重定向，forward: 转发。'),
        Q('mvc-20', '在 Controller 内部写一个专门处理某种异常的方法，贴？', ['@ExceptionHandler', '@ControllerAdvice', '@Valid', '@ResponseBody'], 0,
          ['对', '集中处理（类上）', '校验', '响应体'], '@ExceptionHandler。'),
        Q('mvc-21', '下面的请求处理步骤，正确顺序是？\n\n① HandlerAdapter 调用方法 ② HandlerMapping 找处理方法 ③ 请求到达 DispatcherServlet ④ 处理视图或异常',
          ['③②①④', '②③①④', '③①②④', '①②③④'], 0,
          ['对', '先到前台', '先找方法再调用', '不对'], '前台 → Mapping → Adapter → 结果。', adv=True),
        Q('mvc-22', '把字符串参数转换成其他类型，可以自定义？', ['Converter', 'Formatter', 'TypeHandler', 'RowMapper'], [0, 1],
          ['可以', '可以', 'MyBatis 的', 'JDBC 的'], 'Boot 会自动注册 Converter / Formatter Bean。'),
        TF('mvc-23', '生产环境中建议放心使用 JPA 自动建表', False, '错', '对：生产环境慎用自动建表', '第 52 讲。'),
    ],
}

CHEATSHEET = '''### Spring MVC（第 39—45、49—52 讲）

- 总入口 **DispatcherServlet**；HandlerMapping 找方法，HandlerAdapter 调方法，HandlerExceptionResolver 处理异常，ViewResolver 解析视图，MultipartResolver 上传。
- @RestController = @Controller + @ResponseBody；@RequestMapping / @GetMapping…；@PathVariable 路径变量，@RequestParam 问号参数，@RequestBody 请求体，@RequestHeader，@ResponseStatus。
- 父子上下文：**子看父，父看不到子**；切面只对同一上下文生效。
- 流程：DispatcherServlet → Mapping → Adapter → preHandle → 方法 → postHandle → 视图 / 异常 → afterCompletion。
- Converter / Formatter（Boot 自动注册）；@Valid + BindingResult；MultipartFile。
- 页面 ViewResolver → View；JSON **HttpMessageConverter**；内容协商；redirect: / forward:。
- @ExceptionHandler 单个，**@ControllerAdvice** 集中；拦截器 preHandle（false 拦下）/ postHandle / afterCompletion，WebMvcConfigurer.addInterceptors。
'''
