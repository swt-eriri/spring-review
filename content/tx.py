# 模块：Spring 事务（课程第 10、11、14 讲）
# 深度：「认得出」——看到描述能选对名字，记住默认值、易混对、几个坑。不要求读懂代码。
# 出处说明：GPT 逐讲要点只有概括；默认值、回滚规则、失效场景等细节按 Spring 5（课程所用版本）的官方行为补充。
# 题目：tags 含 'basic' 的是主线题，模拟考只抽这些；tags 含 '进阶' 的是推理题，可跳过。

MODULE = {
    'id': 'tx',
    'title': 'Spring 事务',
    'short': '事务',
    'group': '第二章 JDBC 必知必会',
    'exam': '第 10、11、14 讲',
    'refs': [
        {'label': 'Spring 5.3 文档 · 事务管理', 'url': 'https://docs.spring.io/spring-framework/docs/5.3.x/reference/html/data-access.html#transaction'},
    ],
    'lessons': [
        # ---------------------------------------------------------------- 0
        {'title': '事务是什么，谁负责管它', 'cards': [
'''### 一句话

**事务 = 一组数据库操作，要么全部成功，要么全部撤销。**

例子：下单要做两步，「插入订单」和「扣库存」。如果只做成了一步，数据就乱了。所以把两步捆在一起：

- 都成功 → **提交**（正式保存）
- 有一步失败 → **回滚**（全部撤销，当没发生过）

> 💡 **怎么学这个站**：每个模块只要求「认得出」。看到题目里的描述，能选出对应的名字就够了。不用看懂代码，不用背原理。''',

'''### 对号入座：三个核心接口（必背）

Spring 用三个「接口」来管事务。接口你可以理解成「一个角色的名字」，不用管它是怎么写出来的。

| 看到题目说…… | 就选 | 记法 |
|---|---|---|
| 负责**开启、提交、回滚** | **PlatformTransactionManager** | Manager = 经理，干活的 |
| 描述事务的**规则**（传播、隔离、超时、只读） | **TransactionDefinition** | Definition = 定义，规则说明书 |
| 表示事务**当前的状态** | **TransactionStatus** | Status = 状态 |

> 📌 认准三个英文词：**Manager 干活，Definition 定规则，Status 看状态。**''',

'''### 对号入座：不同技术用不同的「经理」

| 用的是…… | 事务经理叫 |
|---|---|
| JDBC、JdbcTemplate、MyBatis | **DataSource**TransactionManager |
| JPA | **Jpa**TransactionManager |
| Hibernate | **Hibernate**TransactionManager |
| 跨多个数据库（分布式事务） | **Jta**TransactionManager |

记法：**名字前半截就是它对应的技术**，只有 JDBC 和 MyBatis 用的是 DataSource（数据源）。

为什么要这样设计？一句话：**上层代码只认「经理」这个角色，底层换技术时只换经理，上层不用改。**这就是题目里说的「Spring 的事务抽象」。

Spring Boot 会**自动**帮你配好对应的经理，不用自己写。'''
        ]},
        # ---------------------------------------------------------------- 1
        {'title': '事务的四条规则：传播、隔离、超时、只读', 'cards': [
'''### 四条规则（都写在 TransactionDefinition 里）

| 规则 | 管什么 | **默认值（必背）** |
|---|---|---|
| **传播行为** | 一个有事务的方法调用另一个方法时，两者共不共用事务 | **REQUIRED** |
| **隔离级别** | 同时进行的多个事务，互相能看到多少 | **DEFAULT**（跟着数据库自己的设置走） |
| 超时 | 最多执行几秒，超时就回滚 | -1（不限制） |
| 只读 | 是不是只查不改 | false（不是只读） |

> 📌 考得最多的是两个默认值：**传播 REQUIRED，隔离 DEFAULT。**''',

'''### 传播行为：7 种，名字就是意思

场景：方法 A 已经开了事务，A 去调用方法 B。B 的传播行为决定 B 怎么做。

| 名字 | 中文意思 | B 的做法 |
|---|---|---|
| **REQUIRED**（默认） | 需要 | 有事务就加入，没有就新建 |
| **REQUIRES_NEW** | 需要**新的** | **总是**另开一个新事务 |
| **NESTED** | 嵌套 | 在 A 的事务里「存个档」，嵌套执行 |
| SUPPORTS | 支持 | 有就加入，没有就算了 |
| NOT_SUPPORTED | 不支持 | 有也不用，不带事务执行 |
| MANDATORY | 强制 | 必须已经有事务，**没有就报错** |
| NEVER | 绝不 | 绝不能有事务，**有就报错** |

> 💡 不用硬背表格，把英文单词翻成中文，意思基本就出来了。

> ⚠️ 最容易混的一对：**REQUIRES_NEW = 另开一个独立的新事务；NESTED = 还在原来的事务里，只是存了个档。**''',

'''### 隔离级别：先认三个「问题」，再认四个级别

多个事务同时运行，可能出三种问题：

| 问题 | 一句话 | 关键字 |
|---|---|---|
| **脏读** | 读到了别人**还没提交**的数据 | 未提交 |
| **不可重复读** | 同一行数据，两次读到的**值不一样** | 值变了 |
| **幻读** | 同样的查询，两次查到的**行数不一样** | 行数变了 |

四个级别从低到高，每升一级多挡住一个问题：

| 级别 | 挡住了 |
|---|---|
| READ_UNCOMMITTED（读未提交） | 什么都挡不住 |
| **READ_COMMITTED**（读已提交） | 脏读 |
| **REPEATABLE_READ**（可重复读） | 脏读、不可重复读 |
| **SERIALIZABLE**（串行化） | 全部三个 |

> 💡 记法：级别的名字就是它挡住的问题。「读已提交」→ 只读别人提交过的，所以没有脏读；「可重复读」→ 重复读同一行结果不变，所以没有不可重复读。'''
        ]},
        # ---------------------------------------------------------------- 2
        {'title': '两种写法，和三个必背的坑', 'cards': [
'''### 两种写法：认准名字就行

| 写法 | 怎么写 | 认法 |
|---|---|---|
| **编程式事务** | 在代码里用 **TransactionTemplate** 包住要做的事 | 看到 Template |
| **声明式事务** | 在方法上方贴一个 **@Transactional** | 看到 @Transactional |

- 开头带 `@` 的叫**注解**，就是贴在代码上的一个标签，告诉 Spring「这个方法要放进事务里」。
- 编程式里想手动回滚，用 **setRollbackOnly()**（字面意思：设为只能回滚）。
- 传统 Spring 要写 **@EnableTransactionManagement** 打开注解功能；**Spring Boot 自动打开**，不用写。

声明式事务是怎么实现的？一个词：**AOP 代理**。Spring 在你的方法外面套了一层「代理」，由代理负责开事务、提交、回滚。你只要记住「**声明式事务靠代理**」，下一页的坑都是从这来的。''',

'''### 坑一：不是所有错误都会回滚（必背）

方法贴了 @Transactional，执行中出错了，会不会回滚？**看错误的名字：**

| 题目里出现的错误名字 | 结果 |
|---|---|
| 带 **Runtime** 的（如 `RuntimeException`） | **回滚** |
| 不带 Runtime 的（如 `Exception`、`IOException`、`SQLException`） | **不回滚**，照样提交 |

除非注解里写了 **rollbackFor**：`@Transactional(rollbackFor = Exception.class)`，那遇到 Exception 也会回滚。

> 📌 一句话：**默认只有 Runtime 类的错误才回滚；想让别的错误也回滚，写 rollbackFor。**

> ⚠️ 判断题陷阱：「@Transactional 方法出任何错都会回滚」——**错**。''',

'''### 坑二、坑三：事务「失效」了

**坑二：同一个类里，自己调自己，事务不生效。**（第 11、14 讲专门讲过）

一个类里有两个方法 a 和 b，b 贴了 @Transactional，a 没贴。外面调用 a，a 再调用 b → **b 的事务不生效**。

原因一句话：事务是外面那层代理加的，**a 调 b 是在类里面直接调的，没经过代理**。

修法：给 a 也贴上 @Transactional，或者让调用经过代理。

**坑三：错误被自己「接住」了，事务不回滚。**

方法里用 try / catch 把错误接住了（catch 就是「接住错误」的意思），外面的代理就不知道出过错，**照样提交**。

**另外记一条**：@Transactional 要贴在 **public** 方法上，贴在 private 方法上不生效。

> 📌 三个坑：**① 不带 Runtime 的错误默认不回滚 ② 类里自己调自己不生效 ③ 错误被 catch 接住了不回滚。**'''
        ]},
    ],
    'questions': [
        # ---------- 随堂练习 ----------
        {'id': 'tx-p1', 'type': 'single', 'lesson': 0,
         'stem': '事务的意思是？',
         'options': ['一组操作要么全部成功，要么全部撤销', '把数据备份到另一台服务器', '让查询变得更快', '定时自动执行的任务'], 'answer': [0],
         'why': ['这就是事务', '那是备份', '那是缓存、索引做的事', '那是定时任务'],
         'explain': '事务：全成功就提交，有失败就回滚。'},
        {'id': 'tx-p2', 'type': 'single', 'lesson': 0,
         'stem': '负责**开启、提交、回滚**事务的是？',
         'options': ['TransactionDefinition', 'TransactionStatus', 'PlatformTransactionManager', 'DataSource'], 'answer': [2],
         'why': ['Definition 是规则说明书', 'Status 是状态', 'Manager = 干活的经理', 'DataSource 是数据源，不是事务接口'],
         'explain': 'Manager 干活，Definition 定规则，Status 看状态。'},
        {'id': 'tx-p3', 'type': 'single', 'lesson': 1,
         'stem': '传播行为的默认值是？',
         'options': ['REQUIRES_NEW', 'REQUIRED', 'NESTED', 'SUPPORTS'], 'answer': [1],
         'why': ['总是新建，不是默认', '默认：有就加入，没有就新建', '嵌套，不是默认', '不是默认'],
         'explain': '默认值两个必背：传播 REQUIRED，隔离 DEFAULT。'},
        {'id': 'tx-p4', 'type': 'single', 'lesson': 1,
         'stem': '读到了别的事务**还没提交**的数据，这叫？',
         'options': ['脏读', '不可重复读', '幻读', '回滚'], 'answer': [0],
         'why': ['关键字「未提交」→ 脏读', '不可重复读是同一行值变了', '幻读是行数变了', '回滚不是并发问题'],
         'explain': '未提交 → 脏读；值变了 → 不可重复读；行数变了 → 幻读。'},
        {'id': 'tx-p5', 'type': 'single', 'lesson': 2,
         'stem': '在方法上贴 `@Transactional`，属于哪种事务写法？',
         'options': ['编程式事务', '声明式事务', '分布式事务', '只读事务'], 'answer': [1],
         'why': ['编程式是 TransactionTemplate', '贴注解 = 声明式', '分布式是 JTA', '只读是一条规则，不是写法'],
         'explain': '看到 Template → 编程式；看到 @Transactional → 声明式。'},
        {'id': 'tx-p6', 'type': 'single', 'lesson': 2,
         'stem': '`@Transactional` 方法执行中抛出 `IOException`（没写 rollbackFor），结果是？',
         'options': ['回滚', '不回滚，照样提交', '程序直接退出', '自动重试'], 'answer': [1],
         'why': ['名字里不带 Runtime，默认不回滚', '默认只有 Runtime 类错误才回滚', '不会退出', '不会重试'],
         'explain': '看名字：带 Runtime 回滚，不带不回滚，除非写 rollbackFor。'},

        # ---------- 刷题单：主线（basic） ----------
        {'id': 'tx-1', 'type': 'multi', 'tags': ['basic'],
         'stem': 'Spring 事务抽象的三个核心接口是？',
         'options': ['PlatformTransactionManager', 'TransactionDefinition', 'TransactionStatus', 'TransactionTemplate'], 'answer': [0, 1, 2],
         'why': ['经理：开启、提交、回滚', '定义：规则', '状态', 'Template 是编程式事务的工具，不是三个核心接口之一'],
         'explain': 'Manager、Definition、Status。'},
        {'id': 'tx-2', 'type': 'single', 'tags': ['basic'],
         'stem': '描述事务的传播行为、隔离级别、超时、只读等规则的是？',
         'options': ['PlatformTransactionManager', 'TransactionDefinition', 'TransactionStatus', 'JdbcTemplate'], 'answer': [1],
         'why': ['Manager 是干活的', 'Definition = 规则说明书', 'Status 是状态', 'JdbcTemplate 是访问数据库的工具'],
         'explain': 'Definition 定规则。'},
        {'id': 'tx-3', 'type': 'single', 'tags': ['basic'],
         'stem': '使用 MyBatis 或 JdbcTemplate 时，对应的事务管理器是？',
         'options': ['JpaTransactionManager', 'DataSourceTransactionManager', 'JtaTransactionManager', 'HibernateTransactionManager'], 'answer': [1],
         'why': ['JPA 用的', 'JDBC、JdbcTemplate、MyBatis 都用 DataSource', '分布式事务用的', 'Hibernate 用的'],
         'explain': '名字前半截是对应技术，只有 JDBC 和 MyBatis 用 DataSource。'},
        {'id': 'tx-4', 'type': 'single', 'tags': ['basic'],
         'stem': '使用 Spring Data JPA 时，对应的事务管理器是？',
         'options': ['DataSourceTransactionManager', 'JpaTransactionManager', 'JtaTransactionManager', '不需要事务管理器'], 'answer': [1],
         'why': ['那是 JDBC / MyBatis 的', 'JPA → JpaTransactionManager', '那是分布式事务的', '需要，Boot 会自动配'],
         'explain': '名字前半截就是技术名。'},
        {'id': 'tx-5', 'type': 'single', 'tags': ['basic'],
         'stem': '跨多个数据库的**分布式事务**，使用哪个事务管理器？',
         'options': ['DataSourceTransactionManager', 'JpaTransactionManager', 'JtaTransactionManager', 'HibernateTransactionManager'], 'answer': [2],
         'why': ['单个数据源用的', 'JPA 用的', 'JTA = 分布式事务', 'Hibernate 用的'],
         'explain': '分布式 → Jta。'},
        {'id': 'tx-6', 'type': 'single', 'tags': ['basic'],
         'stem': 'Spring 隔离级别的默认值 DEFAULT 表示？',
         'options': ['读未提交', '读已提交', '串行化', '使用数据库自己的默认隔离级别'], 'answer': [3],
         'why': ['不是固定某一级', '不是固定某一级', '不是固定某一级', 'DEFAULT = 跟着数据库走'],
         'explain': '例如 MySQL 默认是可重复读。'},
        {'id': 'tx-7', 'type': 'single', 'tags': ['basic'],
         'stem': '哪种传播行为表示「**总是**另开一个新的独立事务」？',
         'options': ['REQUIRED', 'REQUIRES_NEW', 'NESTED', 'SUPPORTS'], 'answer': [1],
         'why': ['有就加入，没有才新建', 'REQUIRES_NEW = 需要新的', '是在原事务里存档，不是独立新事务', '有就加入，没有就算了'],
         'explain': '名字就是意思：REQUIRES_NEW「需要新的」。'},
        {'id': 'tx-8', 'type': 'single', 'tags': ['basic'],
         'stem': '哪种传播行为表示「必须已经有事务，**没有就报错**」？',
         'options': ['MANDATORY', 'NEVER', 'SUPPORTS', 'NOT_SUPPORTED'], 'answer': [0],
         'why': ['MANDATORY = 强制', 'NEVER 是「有事务就报错」，正好相反', '有没有都行', '有也不用'],
         'explain': 'MANDATORY 没有就报错；NEVER 有就报错。'},
        {'id': 'tx-9', 'type': 'single', 'tags': ['basic'],
         'stem': '哪种传播行为表示「绝不能在事务里运行，**有事务就报错**」？',
         'options': ['MANDATORY', 'NEVER', 'NOT_SUPPORTED', 'REQUIRED'], 'answer': [1],
         'why': ['那是没有就报错', 'NEVER = 绝不', 'NOT_SUPPORTED 是有也不用，但不报错', '有就加入'],
         'explain': '注意 NEVER（报错）和 NOT_SUPPORTED（不报错，只是不用）的区别。'},
        {'id': 'tx-10', 'type': 'single', 'tags': ['basic'],
         'stem': '关于 REQUIRES_NEW 和 NESTED，说法正确的是？',
         'options': ['两者完全一样', 'REQUIRES_NEW 另开独立新事务；NESTED 在原事务里存档嵌套执行', 'NESTED 另开独立新事务；REQUIRES_NEW 在原事务里存档', '两者都不使用事务'], 'answer': [1],
         'why': ['区别是考点', 'NEW = 新的独立事务；NESTED = 嵌套、存档', '说反了', '两者都用事务'],
         'explain': '最容易混的一对，记住「NEW 是新的，NESTED 是存档」。'},
        {'id': 'tx-11', 'type': 'single', 'tags': ['basic'],
         'stem': '同一个事务里，两次读同一行数据，**值不一样**了。这是？',
         'options': ['脏读', '不可重复读', '幻读', '死锁'], 'answer': [1],
         'why': ['脏读是读到未提交的', '值变了 → 不可重复读', '幻读是行数变了', '死锁是互相等待'],
         'explain': '未提交 → 脏读；值变了 → 不可重复读；行数变了 → 幻读。'},
        {'id': 'tx-12', 'type': 'single', 'tags': ['basic'],
         'stem': '同样的条件查询两次，**查到的行数不一样**了。这是？',
         'options': ['脏读', '不可重复读', '幻读', '超时'], 'answer': [2],
         'why': ['脏读是读到未提交的', '不可重复读是值变了', '行数变了 → 幻读', '超时是执行太久'],
         'explain': '行数变了 → 幻读。'},
        {'id': 'tx-13', 'type': 'single', 'tags': ['basic'],
         'stem': '能挡住**全部三种**并发问题（脏读、不可重复读、幻读）的隔离级别是？',
         'options': ['READ_UNCOMMITTED', 'READ_COMMITTED', 'REPEATABLE_READ', 'SERIALIZABLE'], 'answer': [3],
         'why': ['什么都挡不住', '只挡脏读', '挡脏读和不可重复读', '串行化，最高级别，全挡'],
         'explain': '级别从低到高，每升一级多挡一个问题。'},
        {'id': 'tx-14', 'type': 'single', 'tags': ['basic'],
         'stem': 'READ_COMMITTED（读已提交）能挡住哪个问题？',
         'options': ['脏读', '不可重复读', '幻读', '全部'], 'answer': [0],
         'why': ['只读别人提交过的，所以不会读到未提交的 → 没有脏读', '挡不住', '挡不住', '只有 SERIALIZABLE 全挡'],
         'explain': '名字就是它挡住的问题。'},
        {'id': 'tx-15', 'type': 'single', 'tags': ['basic'],
         'stem': '使用 `TransactionTemplate` 管理事务，属于？',
         'options': ['编程式事务', '声明式事务', '分布式事务', '只读事务'], 'answer': [0],
         'why': ['看到 Template → 编程式', '声明式是贴 @Transactional', '不是', '不是'],
         'explain': 'Template → 编程式；@Transactional → 声明式。'},
        {'id': 'tx-16', 'type': 'single', 'tags': ['basic'],
         'stem': '声明式事务（@Transactional）在 Spring 中是靠什么实现的？',
         'options': ['数据库触发器', 'AOP 代理', '修改你的 SQL', '多线程'], 'answer': [1],
         'why': ['无关', 'Spring 在方法外面套一层代理来开事务、提交、回滚', 'Spring 不改 SQL', '无关'],
         'explain': '声明式事务靠 AOP 代理。'},
        {'id': 'tx-17', 'type': 'single', 'tags': ['basic'],
         'stem': '传统 Spring（不用 Spring Boot）中，用哪个注解**打开**注解式事务功能？',
         'options': ['@EnableTransactionManagement', '@Transactional', '@EnableAutoConfiguration', '@Service'], 'answer': [0],
         'why': ['Enable = 打开，TransactionManagement = 事务管理', '它是贴在方法上用的，不是打开功能的开关', '那是 Boot 自动配置的开关', '那是标记业务类的'],
         'explain': 'Spring Boot 会自动打开，不用写。'},
        {'id': 'tx-18', 'type': 'single', 'tags': ['basic'],
         'stem': '@Transactional 方法中抛出哪种错误时，**默认会回滚**？',
         'options': ['RuntimeException', 'IOException', 'SQLException', 'Exception'], 'answer': [0],
         'why': ['名字带 Runtime → 回滚', '不带 Runtime → 默认不回滚', '不带 Runtime → 默认不回滚', '不带 Runtime → 默认不回滚'],
         'explain': '看名字：带 Runtime 回滚，不带不回滚。'},
        {'id': 'tx-19', 'type': 'single', 'tags': ['basic'],
         'stem': '想让 @Transactional 遇到 `Exception` 时也回滚，应该在注解里加？',
         'options': ['timeout', 'readOnly', 'rollbackFor', 'propagation'], 'answer': [2],
         'why': ['超时设置', '只读设置', 'rollbackFor = 遇到什么要回滚', '传播行为'],
         'explain': '`@Transactional(rollbackFor = Exception.class)`。'},
        {'id': 'tx-20', 'type': 'single', 'tags': ['basic'],
         'stem': '判断：「@Transactional 方法出现任何错误，事务都会回滚」',
         'options': ['正确', '错误'], 'answer': [1],
         'why': ['不带 Runtime 的错误默认不回滚', '默认只有 Runtime 类错误（和 Error）才回滚'],
         'explain': '常见陷阱题。'},
        {'id': 'tx-21', 'type': 'multi', 'tags': ['basic'],
         'stem': '下面哪些情况，@Transactional 的事务**不会**按预期回滚？',
         'options': ['同一个类里，没贴注解的方法调用了贴注解的方法', '方法里用 try/catch 把错误接住了', '抛出 IOException，且没写 rollbackFor', '抛出 RuntimeException 且没有被接住'], 'answer': [0, 1, 2],
         'why': ['类里自己调自己，没经过代理，不生效', '错误被接住，代理不知道，照样提交', '不带 Runtime，默认不回滚', '这是标准的会回滚的情况'],
         'explain': '三个坑：自己调自己、错误被接住、不带 Runtime 的错误。'},
        {'id': 'tx-22', 'type': 'single', 'tags': ['basic'],
         'stem': '@Transactional 贴在哪种方法上才生效（课程所用版本）？',
         'options': ['public 方法', 'private 方法', '任何方法都一样', '只能贴在类上'], 'answer': [0],
         'why': ['贴在 public 方法上才生效', '贴在 private 上不生效', '不一样', '方法和类上都可以贴'],
         'explain': '记住：public 才生效。'},
        {'id': 'tx-23', 'type': 'single', 'tags': ['basic'],
         'stem': '编程式事务中，想手动让事务回滚，调用？',
         'options': ['setRollbackOnly()', 'commit()', 'setReadOnly()', 'close()'], 'answer': [0],
         'why': ['字面意思：设为只能回滚', '那是提交', '那是只读', '不是事务方法'],
         'explain': 'setRollbackOnly = 设为只能回滚。'},

        # ---------- 刷题单：进阶（推理题，可跳过） ----------
        {'id': 'tx-a1', 'type': 'single', 'tags': ['进阶'],
         'stem': '【进阶，可跳过】A 有事务，A 调用 B（REQUIRES_NEW）插入一条日志，B 正常结束。之后 A 出错回滚。日志还在吗？',
         'options': ['在', '不在', '看隔离级别', '看是否只读'], 'answer': [0],
         'why': ['B 是独立的新事务，B 结束时已经提交了，A 回滚管不到它', 'NESTED 才会被一起回滚', '无关', '无关'],
         'explain': 'REQUIRES_NEW：独立事务，先提交了就留下。'},
        {'id': 'tx-a2', 'type': 'single', 'tags': ['进阶'],
         'stem': '【进阶，可跳过】同上一题，但 B 改成 NESTED。A 回滚后日志还在吗？',
         'options': ['在', '不在', '报错', 'B 变成 REQUIRES_NEW'], 'answer': [1],
         'why': ['NESTED 还在 A 的事务里，没有单独提交', 'A 回滚，存档里的内容一起撤销', '不会报错', '不会自动转换'],
         'explain': 'NESTED 是同一个事务里的存档，外层回滚连带它。'},
        {'id': 'tx-a3', 'type': 'single', 'tags': ['进阶'],
         'stem': '【进阶，可跳过】外面调用 `invoke()`，表里会不会留下 BBB？\n\n```java\n@Transactional(rollbackFor = RollbackException.class)\npublic void insertThenRollback() throws RollbackException {\n    插入 BBB;\n    throw new RollbackException();\n}\n\npublic void invoke() throws RollbackException {\n    insertThenRollback();   // 同一个类里直接调用\n}\n```',
         'options': ['会留下', '不会留下', '启动报错', '不确定'], 'answer': [0],
         'why': ['类里自己调自己，没经过代理，事务没开，BBB 直接保存了', '要经过代理才会回滚', '能正常启动', '结果是确定的'],
         'explain': '第 11、14 讲的经典例子：自己调自己，事务失效。'},
        {'id': 'tx-a4', 'type': 'multi', 'tags': ['进阶'],
         'stem': '【进阶，可跳过】A 有事务，调用 B，B 出了 RuntimeException，A 用 try/catch 接住后继续正常结束。A 自己插入的数据**能保存下来**的是？',
         'options': ['B 是 REQUIRES_NEW', 'B 是 NESTED', 'B 是 REQUIRED'], 'answer': [0, 1],
         'why': ['B 只回滚自己的独立事务', 'B 只回滚到存档点', 'B 和 A 共用一个事务，B 出错已经把整个事务标记成只能回滚，A 结束时也会回滚'],
         'explain': '（补充）REQUIRED 下内层出错会把共用的事务标记为只能回滚，外层接住也没用。'},
    ],
}

CHEATSHEET = '''### 事务（第 10、11、14 讲）

- 事务 = 一组操作要么全成功（提交），要么全撤销（回滚）。
- **Manager 干活**（PlatformTransactionManager：开启/提交/回滚），**Definition 定规则**（TransactionDefinition），**Status 看状态**（TransactionStatus）。
- 经理名字前半截 = 技术：JDBC / MyBatis → **DataSource**；JPA → **Jpa**；分布式 → **Jta**。
- 默认值：传播 **REQUIRED**，隔离 **DEFAULT（跟数据库走）**，超时 -1，只读 false。
- 传播：REQUIRES_NEW = 总是新的独立事务；NESTED = 原事务里存档；MANDATORY 没有就报错；NEVER 有就报错。
- 并发问题：未提交 → 脏读；值变了 → 不可重复读；行数变了 → 幻读。SERIALIZABLE 全挡。
- Template → 编程式（手动回滚 setRollbackOnly）；@Transactional → 声明式，靠 **AOP 代理**；传统 Spring 用 @EnableTransactionManagement 打开，Boot 自动打开。
- 回滚：**带 Runtime 的错误回滚，不带的不回滚**，除非写 rollbackFor。
- 三个坑：类里自己调自己不生效；错误被 catch 接住不回滚；贴在非 public 方法上不生效。
'''
