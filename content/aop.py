# 模块：AOP（第 36—38 讲）。深度：认得出。
from qhelp import Q, TF

MODULE = {
    'id': 'aop', 'title': 'AOP：在方法前后自动加一段逻辑', 'short': 'AOP',
    'group': '第五章 数据访问进阶', 'exam': '第 36—38 讲',
    'refs': [{'label': 'Spring 5.3 文档 · AOP', 'url': 'https://docs.spring.io/spring-framework/docs/5.3.x/reference/html/core.html#aop'}],
    'lessons': [
        {'title': 'AOP 的几个词', 'cards': [
'''### 一句话

**AOP（面向切面编程）= 不改原来的代码，在方法执行的前后自动加一段逻辑。**

典型用途：打日志、统计耗时、**事务**（事务模块讲过，@Transactional 就是靠 AOP 实现的）。这些逻辑到处都要用，叫「**横切逻辑**」。

### 术语对号入座（必背）

| 看到题目说…… | 就选 | 记法 |
|---|---|---|
| 要加的那段逻辑 + 加在哪，打包在一起 | **切面（Aspect）** | 一整块 |
| 要加的那段逻辑本身（什么时候做、做什么） | **通知（Advice）** | 做什么 |
| 规定**加在哪些方法上**的规则 | **切点（Pointcut）** | 在哪 |
| 程序执行中可以加逻辑的点（Spring 里就是方法执行） | **连接点（Join Point）** | 可选的点 |
| 被加了逻辑的原始对象 | **目标对象（Target）** | |
| 把切面加到目标对象上的过程 | **织入（Weaving）** | |
| Spring 生成的、带着额外逻辑的对象 | **AOP 代理（Proxy）** | |

> 📌 最常考的三个：**切面 = 通知 + 切点；通知 = 做什么；切点 = 在哪做。**'''
        ]},
        {'title': '五种通知和怎么写', 'cards': [
'''### 五种通知（必背）

| 注解 | 什么时候执行 |
|---|---|
| **@Before** | 方法执行**之前** |
| **@AfterReturning** | 方法**正常返回**之后 |
| **@AfterThrowing** | 方法**抛出异常**之后 |
| **@After** | 方法结束后，**不管成功还是出错都执行**（像 finally） |
| **@Around** | **包住**整个方法，前后都能做事，甚至决定方法执不执行 |

- @Around 里要调用 **ProceedingJoinPoint.proceed()** 才会真正执行原方法；
- 统计方法耗时，最适合用 **@Around**（前面记开始时间，后面算差值）。''',
'''### 怎么写一个切面

| 看到题目说…… | 就选 |
|---|---|
| 标记一个类是切面 | **@Aspect**（还要加 @Component 交给 Spring 管理） |
| 打开 @Aspect 注解支持 | **@EnableAspectJAutoProxy**（Boot 自动打开） |
| 多个切面谁先执行 | **@Order**，**数字越小越先执行** |

**切点表达式**（写「加在哪些方法上」）常见几种：
- `execution(...)`：按方法签名匹配，**最常用**；
- `within(...)`：某个包或类里的所有方法；
- `@annotation(...)`：贴了某个注解的方法；
- `bean(...)`：某个名字的 Bean。

### 代理的两种方式（认关键词）

| 方式 | 适用 |
|---|---|
| **JDK 动态代理** | 目标类**实现了接口** |
| **CGLIB** | 没有接口，直接给**类**生成子类代理 |

课程案例：用 AOP 给所有 Repository 方法打印**执行耗时**（第 37 讲）。'''
        ]},
    ],
    'questions': [
        Q('aop-p1', 'AOP 中，规定「把逻辑加在哪些方法上」的是？', ['切点（Pointcut）', '通知（Advice）', '目标对象（Target）', '织入（Weaving）'], 0,
          ['在哪 → 切点', '做什么 → 通知', '被加逻辑的对象', '加的过程'], '切点 = 在哪。', lesson=0),
        Q('aop-p2', '方法执行前后都能做事，还能决定方法执不执行的通知是？', ['@Around', '@Before', '@After', '@AfterReturning'], 0,
          ['包住整个方法', '只在之前', '只在之后', '只在正常返回后'], '@Around。', lesson=1),
        Q('aop-p3', '多个切面时，用什么控制执行顺序？', ['@Order', '@Primary', '@Aspect', '@Bean'], 0,
          ['数字越小越先执行', '那是指定主 Bean', '标记切面', '造 Bean'], '@Order。', lesson=1),

        Q('aop-1', 'AOP 适合处理哪类逻辑？', ['日志、耗时统计、事务等横切逻辑', '页面布局', '数据库表设计', '前端样式'], 0,
          ['对', '无关', '无关', '无关'], '横切逻辑。'),
        Q('aop-2', 'AOP 中，「要加的那段逻辑本身」叫？', ['通知（Advice）', '切点（Pointcut）', '连接点（Join Point）', '代理（Proxy）'], 0,
          ['做什么 → 通知', '在哪', '可选的点', '生成的对象'], '通知 = 做什么。'),
        Q('aop-3', '切面（Aspect）由什么组成？', ['通知 + 切点', '目标对象 + 代理', '连接点 + 织入', 'Bean + 注解'], 0,
          ['对', '不是', '不是', '不是'], '切面 = 通知 + 切点。'),
        Q('aop-4', '把切面应用到目标对象上的过程叫？', ['织入（Weaving）', '切点', '通知', '代理'], 0,
          ['Weaving = 编织', '在哪', '做什么', '结果对象'], '织入。'),
        Q('aop-5', '在 Spring AOP 中，连接点（Join Point）指的是？', ['方法的执行', '数据库连接', '网络连接', '线程'], 0,
          ['Spring 只支持方法级连接点', '无关', '无关', '无关'], 'Spring 里连接点 = 方法执行。'),
        Q('aop-6', '方法**不管成功还是出错**都会执行的通知是？', ['@After', '@AfterReturning', '@AfterThrowing', '@Before'], 0,
          ['像 finally', '只在正常返回', '只在出错', '之前'], '@After 一定执行。'),
        Q('aop-7', '方法**抛出异常后**执行的通知是？', ['@AfterThrowing', '@AfterReturning', '@After', '@Before'], 0,
          ['Throwing = 抛出', '正常返回', '都执行', '之前'], '@AfterThrowing。'),
        Q('aop-8', '方法**正常返回后**执行的通知是？', ['@AfterReturning', '@AfterThrowing', '@Around', '@Before'], 0,
          ['Returning = 返回', '出错', '包住', '之前'], '@AfterReturning。'),
        Q('aop-9', '@Around 通知中，执行原方法要调用？', ['ProceedingJoinPoint.proceed()', 'run()', 'execute()', 'invoke()'], 0,
          ['proceed = 继续', '不是', '不是', '不是'], 'proceed()。'),
        Q('aop-10', '统计方法执行耗时，最适合用哪种通知？', ['@Around', '@Before', '@AfterThrowing', '@AfterReturning'], 0,
          ['前后都能拿到时间', '只有之前', '只在出错', '只有之后'], '@Around。'),
        Q('aop-11', '标记一个类是切面的注解是？', ['@Aspect', '@Pointcut', '@Component', '@Around'], 0,
          ['对', '定义切点', '交给 Spring 管（也要加，但不表示切面）', '通知'], '@Aspect + @Component。'),
        Q('aop-12', '打开 @Aspect 注解支持的注解是？', ['@EnableAspectJAutoProxy', '@EnableCaching', '@EnableTransactionManagement', '@EnableAutoConfiguration'], 0,
          ['对（Boot 自动打开）', '缓存', '事务', 'Boot 自动配置'], 'Enable + AspectJ + AutoProxy。'),
        Q('aop-13', '最常用的、按方法签名匹配的切点表达式是？', ['execution(...)', 'within(...)', 'bean(...)', '@annotation(...)'], 0,
          ['对', '按包或类', '按 Bean 名', '按注解'], 'execution。'),
        Q('aop-14', '目标类实现了接口时，可以用哪种方式生成代理？', ['JDK 动态代理', 'CGLIB', '两者都可以', '都不行'], 2,
          ['可以', 'CGLIB 也可以', '有接口两种都行；没接口只能 CGLIB', '可以'], '没有接口只能用 CGLIB。', adv=True),
        Q('aop-15', '目标类**没有实现接口**时，Spring 用什么生成代理？', ['CGLIB', 'JDK 动态代理', '不能代理', '数据库触发器'], 0,
          ['生成子类', 'JDK 代理需要接口', '可以', '无关'], '没接口 → CGLIB。'),
        Q('aop-16', '@Order 的数字和执行顺序的关系是？', ['数字越小越先执行', '数字越大越先执行', '无关', '只能是 0 或 1'], 0,
          ['对', '反了', '有关', '不是'], '越小越优先。'),
        TF('aop-17', '声明式事务 @Transactional 是基于 AOP 实现的', True, '对', '错', '事务模块讲过。'),
    ],
}

CHEATSHEET = '''### AOP（第 36—38 讲）

- AOP = 不改代码，在方法前后加横切逻辑（日志、耗时、事务）。
- **切面 = 通知 + 切点；通知 = 做什么；切点 = 在哪**；连接点 = 方法执行；织入 = 应用过程；目标对象；AOP 代理。
- 通知：@Before 前，@AfterReturning 正常返回后，@AfterThrowing 出错后，@After 都执行（finally），**@Around 包住**（proceed() 执行原方法，适合统计耗时）。
- @Aspect + @Component；@EnableAspectJAutoProxy（Boot 自动）；**@Order 越小越先**。
- 切点表达式：execution（最常用）、within、@annotation、bean。
- 有接口 JDK 动态代理或 CGLIB；没接口 CGLIB。
'''
