# 模块：Spring JDBC 与异常抽象（第 09、12 讲）。深度：认得出。
from qhelp import Q, TF

MODULE = {
    'id': 'jdbc', 'title': 'Spring JDBC：JdbcTemplate 与异常抽象', 'short': 'JdbcTemplate 与异常',
    'group': '第二章 JDBC 必知必会', 'exam': '第 09、12 讲',
    'refs': [{'label': 'Spring 5.3 文档 · JDBC', 'url': 'https://docs.spring.io/spring-framework/docs/5.3.x/reference/html/data-access.html#jdbc'}],
    'lessons': [
        {'title': 'JdbcTemplate：直接写 SQL 的好帮手', 'cards': [
'''### 一句话

**JdbcTemplate = Spring 提供的「写 SQL 操作数据库」的工具。**它帮你处理打开连接、关闭连接这些杂事，你只管写 SQL。

### 方法对号入座

| 看到题目说…… | 就选 |
|---|---|
| 增、删、改 | **update()** |
| 查询，结果是多条 | **query()** / **queryForList()** |
| 查询，结果只有一个（如一个数字、一个对象） | **queryForObject()** |
| 批量执行多条 | **batchUpdate()** |
| 执行任意语句（如建表） | **execute()** |

> 💡 记法：**改数据都用 update**，不管是插入、修改还是删除。''',
'''### 几个配套工具

| 看到题目说…… | 就选 |
|---|---|
| 把查询结果的**一行**变成一个 Java 对象 | **RowMapper** |
| 插入数据并**拿到自动生成的主键** | **SimpleJdbcInsert** |
| SQL 里用 **:名字** 代替 **?** 当参数 | **NamedParameterJdbcTemplate** |

例子：`SELECT * FROM FOO WHERE ID = ?` 用问号占位；NamedParameterJdbcTemplate 可以写成 `WHERE ID = :id`，更好读。

> 📌 本节要点：**update 改、query 查、RowMapper 转对象、SimpleJdbcInsert 拿主键、Named… 用名字当参数。**'''
        ]},
        {'title': '异常抽象：数据库报错统一翻译', 'cards': [
'''### 一句话

不同数据库（MySQL、Oracle……）报错的代码各不相同。**Spring 把它们统一翻译成自己的一套异常，根叫 DataAccessException。**

| 看到题目说…… | 就选 |
|---|---|
| Spring 数据访问异常的**统一父类** | **DataAccessException** |
| 违反唯一约束（主键重复） | **DuplicateKeyException** |
| 负责把数据库错误码翻译成 Spring 异常 | **SQLErrorCodeSQLExceptionTranslator** |
| 记录各数据库错误码对照的文件 | **sql-error-codes.xml** |

- DataAccessException 是**运行时异常**（名字链上有 Runtime），所以在事务里**会回滚**。
- 想**自定义翻译**：在自己项目里放一个 sql-error-codes.xml，覆盖默认的对照表。

> 📌 好处一句话：**换数据库，上层代码捕获的异常不用改。**'''
        ]},
    ],
    'questions': [
        Q('jdbc-p1', 'JdbcTemplate 中，插入、修改、删除数据都用哪个方法？', ['query()', 'update()', 'execute()', 'queryForObject()'], 1,
          ['查询', '改数据都用 update', '执行任意语句，一般用来建表', '查单个结果'], '改数据 → update。', lesson=0),
        Q('jdbc-p2', '把查询结果的每一行转成一个 Java 对象，用？', ['RowMapper', 'DataSource', 'SimpleJdbcInsert', 'TransactionTemplate'], 0,
          ['Row = 行，Mapper = 映射', '数据源', '插入并拿主键', '编程式事务'], 'RowMapper = 行 → 对象。', lesson=0),
        Q('jdbc-p3', 'Spring 数据访问异常的统一父类是？', ['SQLException', 'DataAccessException', 'RuntimeException', 'IOException'], 1,
          ['那是 JDBC 原生异常', 'Spring 的统一父类', '它更上层，太宽泛', '无关'], '根 = DataAccessException。', lesson=1),

        Q('jdbc-1', 'JdbcTemplate 查询**单个结果**（如统计总数），用？', ['queryForObject()', 'queryForList()', 'update()', 'batchUpdate()'], 0,
          ['单个 → ForObject', '多条', '改数据', '批量'], 'queryForObject 查一个。'),
        Q('jdbc-2', 'JdbcTemplate 批量执行多条语句，用？', ['batchUpdate()', 'update()', 'execute()', 'query()'], 0,
          ['batch = 批量', '单条', '任意语句', '查询'], 'batchUpdate。'),
        Q('jdbc-3', '插入数据后想**拿到数据库自动生成的主键**，可以用？', ['SimpleJdbcInsert', 'RowMapper', 'DataAccessException', 'NamedParameterJdbcTemplate'], 0,
          ['对', '行转对象', '异常', '命名参数'], 'SimpleJdbcInsert 能返回生成的主键。'),
        Q('jdbc-4', 'SQL 中用 `:id` 这种**名字**代替 `?` 作为参数，用？', ['NamedParameterJdbcTemplate', 'SimpleJdbcInsert', 'RowMapper', 'DataSource'], 0,
          ['Named Parameter = 命名参数', '插入拿主键', '行转对象', '数据源'], '名字参数 → Named…'),
        Q('jdbc-5', 'JdbcTemplate 帮开发者处理了什么？', ['打开和关闭连接等资源管理', '自动设计表结构', '自动生成业务代码', '页面渲染'], 0,
          ['对', '不会', '不会', '无关'], '只管写 SQL，杂事它干。'),
        Q('jdbc-6', '插入数据违反唯一约束（主键重复），Spring 会抛出？', ['DuplicateKeyException', 'NullPointerException', 'IOException', 'TimeoutException'], 0,
          ['Duplicate Key = 重复的键', '空指针', '无关', '超时'], '重复键 → DuplicateKeyException。'),
        Q('jdbc-7', '负责把数据库错误码翻译成 Spring 异常的是？', ['SQLErrorCodeSQLExceptionTranslator', 'RowMapper', 'JdbcTemplate', 'HikariCP'], 0,
          ['名字里有 ErrorCode 和 Translator（翻译器）', '行转对象', '它使用翻译器，但不是翻译器本身', '连接池'], '认 Translator = 翻译器。'),
        Q('jdbc-8', '记录各数据库错误码对照关系的文件是？', ['sql-error-codes.xml', 'schema.sql', 'pom.xml', 'application.yml'], 0,
          ['对', '建表脚本', 'Maven 配置', '配置文件'], '自定义翻译也是放一个 sql-error-codes.xml。'),
        Q('jdbc-9', 'Spring 异常抽象的好处是？', ['换数据库时，上层捕获的异常不用改', '让 SQL 执行更快', '不再需要数据库', '自动修复错误'], 0,
          ['对', '无关', '无关', '无关'], '统一翻译。'),
        TF('jdbc-10', 'DataAccessException 是受检异常，在事务中默认不会回滚', False, '错', '对：它是运行时异常，默认会回滚', 'DataAccessException 继承自 RuntimeException。'),
        Q('jdbc-11', '下列哪些是 JdbcTemplate 的方法？', ['query()', 'update()', 'batchUpdate()', 'getForObject()'], [0, 1, 2],
          ['是', '是', '是', '那是 RestTemplate 的方法'], 'getForObject 是 RestTemplate（调网络接口）的。'),
    ],
}

CHEATSHEET = '''### JdbcTemplate 与异常（第 09、12 讲）

- update 增删改；query / queryForList 查多条；queryForObject 查一个；batchUpdate 批量；execute 任意语句。
- RowMapper 行 → 对象；SimpleJdbcInsert 插入拿主键；NamedParameterJdbcTemplate 用 :名字 当参数。
- 异常根 **DataAccessException**（运行时异常）；主键重复 DuplicateKeyException；翻译器 SQLErrorCodeSQLExceptionTranslator；对照表 sql-error-codes.xml（可自定义覆盖）。
'''
