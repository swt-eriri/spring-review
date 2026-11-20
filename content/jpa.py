# 模块：Spring Data JPA（第 15—19、23 讲）。深度：认得出。
from qhelp import Q, TF

MODULE = {
    'id': 'jpa', 'title': 'Spring Data JPA：实体、Repository 和按方法名查询', 'short': 'JPA',
    'group': '第三章 O/R Mapping 实践', 'exam': '第 15—19、23 讲',
    'refs': [{'label': 'Spring Data JPA 文档 · 按方法名查询', 'url': 'https://docs.spring.io/spring-data/jpa/docs/2.1.x/reference/html/#jpa.query-methods'}],
    'lessons': [
        {'title': 'ORM、JPA、Hibernate、Spring Data JPA 是什么关系', 'cards': [
'''### 一句话

Java 里是「对象」，数据库里是「表」，两者结构不一样。**ORM（对象关系映射）就是把对象和表自动对应起来**，你操作对象，它帮你生成 SQL。

| 名字 | 是什么 | 打个比方 |
|---|---|---|
| **JPA** | 一套**规范**（只定规则，不干活） | 驾照考试标准 |
| **Hibernate** | JPA 的一种**实现**（真正干活的） | 一个具体的司机 |
| **Spring Data JPA** | Spring 在 JPA 之上再简化一层，提供 **Repository** | 给司机配了自动驾驶 |

> 📌 认准：**JPA 是规范，Hibernate 是实现，Spring Data JPA 用 Repository 再简化。**''',
'''### 实体注解：对号入座（第 16 讲）

「实体」就是和一张表对应的 Java 类。

| 看到题目说…… | 就选 |
|---|---|
| 这个类对应数据库里的一张表 | **@Entity** |
| 指定表名 | **@Table** |
| 这个字段是主键 | **@Id** |
| 主键自动生成 | **@GeneratedValue** |
| 指定列名等 | **@Column** |
| 多对多关系（如一个订单多杯咖啡，一种咖啡在多个订单里） | **@ManyToMany** |
| 一对多 / 多对一 | **@OneToMany / @ManyToOne** |
| 自动记录创建时间 / 更新时间 | **@CreationTimestamp / @UpdateTimestamp** |
| 枚举存进数据库 | **@Enumerated** |
| 多个实体的公共字段（如 id、创建时间）放到父类 | **@MappedSuperclass** |'''
        ]},
        {'title': 'Lombok：少写样板代码', 'cards': [
'''### 一句话

**Lombok 用注解自动生成那些又长又无聊的代码**（取值、赋值、构造方法等），课程里大量使用。

| 看到题目说…… | 就选 |
|---|---|
| 自动生成 getter / setter / toString 等一大堆 | **@Data** |
| 只生成 getter / setter | **@Getter / @Setter** |
| 生成无参构造方法 | **@NoArgsConstructor** |
| 生成全参构造方法 | **@AllArgsConstructor** |
| 用「链式写法」创建对象 | **@Builder** |
| 自动生成一个日志对象 log | **@Slf4j** |
| 生成 toString 方法 | **@ToString** |

### SpringBucks 建模要点（第 17 讲）

- 金额不能用小数类型（会有精度问题），课程用 **Joda Money** 库表示金额；
- 订单状态用**枚举**表示（如 INIT、PAID、BREWING、BREWED、TAKEN、CANCELLED）。'''
        ]},
        {'title': 'Repository：只写接口就能查数据库', 'cards': [
'''### 一句话

**在 Spring Data JPA 里，你只需要写一个接口，不用写实现，Spring 自动帮你生成。**

三个常见的父接口，一个比一个功能多：

| 接口 | 提供 |
|---|---|
| **CrudRepository** | 基本的增删改查（Crud = Create Read Update Delete） |
| **PagingAndSortingRepository** | 再加上**分页和排序** |
| **JpaRepository** | 再加上 JPA 特有的功能（如批量） |

- 开启 Repository 扫描：**@EnableJpaRepositories**（Boot 自动开启）；
- 不想让 Spring 为某个接口生成实现（比如它只是公共父接口）：**@NoRepositoryBean**。''',
'''### 按方法名查询：方法名就是查询条件（第 18 讲）

只要按规则起方法名，Spring 就能「读懂」并生成 SQL：

| 方法名 | Spring 理解为 |
|---|---|
| `findByName(name)` | 按名字查 |
| `findByNameAndPrice(...)` | 按名字**和**价格查 |
| `findByCustomerOrderById(...)` | 按顾客查，**按 id 排序** |
| `findTop3ByOrderByUpdateTimeDesc()` | 按更新时间倒序，取**前 3 个** |
| `countByStatus(...)` | 按状态**计数** |

- 开头：**find…By / read…By / query…By / get…By**（查询），**count…By**（计数）；
- 中间：And、Or、OrderBy、Top / First；
- 分页参数 **Pageable**，排序参数 **Sort**。

### Repository 是怎么变成 Bean 的（第 19 讲，认关键词）

Spring 为你的接口生成**代理对象**。基础的增删改查交给默认实现 **SimpleJpaRepository**；按方法名的查询，由框架**解析方法名**后执行。

### Query by Example（第 23 讲）

拿一个「样例对象」当查询条件：样例里填了什么字段，就按什么字段查。'''
        ]},
    ],
    'questions': [
        Q('jpa-p1', 'JPA、Hibernate 的关系是？', ['JPA 是规范，Hibernate 是它的一种实现', 'Hibernate 是规范，JPA 是实现', '两者完全无关', '两者是同一个东西'], 0,
          ['对', '说反了', '有关', '不同'], 'JPA 规范，Hibernate 实现。', lesson=0),
        Q('jpa-p2', '标记一个类对应数据库中的一张表，用？', ['@Entity', '@Id', '@Column', '@Service'], 0,
          ['Entity = 实体', '主键', '列', '业务层'], '实体 → @Entity。', lesson=0),
        Q('jpa-p3', 'Lombok 中，自动生成 getter、setter、toString 等的注解是？', ['@Data', '@Builder', '@Slf4j', '@Entity'], 0,
          ['一个顶一堆', '链式创建对象', '日志', 'JPA 注解'], '@Data。', lesson=1),
        Q('jpa-p4', '在 Spring Data JPA 中，方法 `findByName(String name)` 的作用是？', ['按名字查询', '删除名字', '修改名字', '统计名字数量'], 0,
          ['find…By + 条件', '删除是 delete', '修改用 save', '计数是 count'], '方法名就是查询条件。', lesson=2),

        Q('jpa-1', 'Spring Data JPA 在 JPA 之上提供的核心抽象是？', ['Repository', 'JdbcTemplate', 'DataSource', 'DispatcherServlet'], 0,
          ['对', '那是 Spring JDBC 的', '数据源', 'Web 的入口'], 'Spring Data 的核心：Repository。'),
        Q('jpa-2', 'ORM 的作用是？', ['把 Java 对象和数据库表对应起来', '把网页和数据库对应起来', '把多个数据库合并', '加速网络请求'], 0,
          ['对象关系映射', '无关', '无关', '无关'], 'ORM = 对象 ↔ 表。'),
        Q('jpa-3', '标记实体的**主键**字段，用？', ['@Id', '@GeneratedValue', '@Column', '@Table'], 0,
          ['Id = 主键', '它是主键生成策略', '列', '表名'], '@Id 主键，@GeneratedValue 自动生成。'),
        Q('jpa-4', '让主键**自动生成**，用？', ['@GeneratedValue', '@Id', '@Entity', '@Column'], 0,
          ['Generated = 生成的', '只标记主键', '实体', '列'], '@GeneratedValue。'),
        Q('jpa-5', '订单和咖啡（一个订单多种咖啡，一种咖啡在多个订单里）的关系用？', ['@ManyToMany', '@OneToOne', '@Id', '@Table'], 0,
          ['多对多', '一对一', '主键', '表名'], '多对多。'),
        Q('jpa-6', '多个实体共有的字段（id、创建时间）提取到父类，父类上贴？', ['@MappedSuperclass', '@Entity', '@Table', '@Data'], 0,
          ['Mapped Superclass = 映射的父类', '实体', '表名', 'Lombok'], '公共父类 → @MappedSuperclass。'),
        Q('jpa-7', '自动记录**创建时间**，用？', ['@CreationTimestamp', '@UpdateTimestamp', '@GeneratedValue', '@Column'], 0,
          ['Creation = 创建', '更新时间', '主键生成', '列'], '创建 Creation，更新 Update。'),
        Q('jpa-8', 'Lombok 中，用「链式写法」创建对象的注解是？', ['@Builder', '@Data', '@AllArgsConstructor', '@Getter'], 0,
          ['Builder = 建造者', '一大堆方法', '全参构造', '取值'], '@Builder。'),
        Q('jpa-9', 'Lombok 中，自动生成日志对象 log 的注解是？', ['@Slf4j', '@Data', '@ToString', '@Builder'], 0,
          ['Slf4j 是日志框架名', '无关', '无关', '无关'], '@Slf4j。'),
        Q('jpa-10', '在 Repository 父接口中，提供**分页和排序**的是？', ['PagingAndSortingRepository', 'CrudRepository', 'JdbcTemplate', 'MongoRepository'], 0,
          ['名字就是意思', '只有基本增删改查', '不是 Repository', 'MongoDB 用的'], 'Paging = 分页，Sorting = 排序。'),
        Q('jpa-11', 'CrudRepository 中的 CRUD 指？', ['增、查、改、删', '缓存、路由、更新、删除', '创建、运行、上传、下载', '连接、读取、更新、断开'], 0,
          ['Create Read Update Delete', '不是', '不是', '不是'], '基本增删改查。'),
        Q('jpa-12', '不想让 Spring 为某个公共父接口生成实现，在它上面贴？', ['@NoRepositoryBean', '@Repository', '@EnableJpaRepositories', '@Entity'], 0,
          ['名字就是意思：不是 Repository Bean', '那是标记数据层', '那是开启扫描', '实体'], '@NoRepositoryBean。'),
        Q('jpa-13', '开启 JPA Repository 扫描的注解是？', ['@EnableJpaRepositories', '@EnableCaching', '@EnableTransactionManagement', '@NoRepositoryBean'], 0,
          ['对（Boot 自动开启）', '缓存', '事务', '相反'], 'Enable + JpaRepositories。'),
        Q('jpa-14', '方法名 `findTop3ByOrderByUpdateTimeDesc()` 的意思是？', ['按更新时间倒序，取前 3 个', '按更新时间正序，取前 3 个', '删除前 3 个', '统计 3 次'], 0,
          ['Top3 前三，Desc 倒序', 'Desc 是倒序', '不是删除', '不是计数'], '读方法名就行。'),
        Q('jpa-15', 'Spring Data JPA 中，分页查询的参数类型是？', ['Pageable', 'Sort', 'RowMapper', 'Example'], 0,
          ['Page = 页', '排序', 'JDBC 的', '按样例查询'], '分页 Pageable，排序 Sort。'),
        Q('jpa-16', 'Repository 接口中基础增删改查的默认实现类是？', ['SimpleJpaRepository', 'JdbcTemplate', 'HibernateTemplate', 'JpaTransactionManager'], 0,
          ['对', '不是', '不是', '那是事务管理器'], '第 19 讲：代理 + SimpleJpaRepository。'),
        Q('jpa-17', '用一个「样例对象」当查询条件的查询方式叫？', ['Query by Example', '按方法名查询', '原生 SQL', '分页查询'], 0,
          ['对', '那是读方法名', '不是', '不是'], 'Query by Example。'),
        TF('jpa-18', '使用 Spring Data JPA 时，必须为 Repository 接口手写实现类', False, '错', '对：只写接口，Spring 自动生成代理', '只写接口。'),
        Q('jpa-19', '课程中表示金额用的是？', ['Joda Money', 'double', 'float', 'String'], 0,
          ['对', '小数类型有精度问题', '小数类型有精度问题', '不合适'], '金额别用小数类型。'),
    ],
}

CHEATSHEET = '''### JPA（第 15—19、23 讲）

- ORM 对象 ↔ 表；**JPA 规范，Hibernate 实现，Spring Data JPA 提供 Repository**。
- @Entity 实体，@Table 表名，@Id 主键，@GeneratedValue 自动生成，@Column 列，@ManyToMany 多对多，@CreationTimestamp / @UpdateTimestamp，@Enumerated 枚举，@MappedSuperclass 公共父类。
- Lombok：@Data 一大堆，@Builder 链式，@Slf4j 日志，@NoArgsConstructor / @AllArgsConstructor。金额用 Joda Money。
- CrudRepository（增删改查）→ PagingAndSortingRepository（+分页排序）→ JpaRepository；@EnableJpaRepositories；@NoRepositoryBean。
- 方法名查询：findBy… And / OrderBy / Top3 / Desc；countBy…；Pageable 分页、Sort 排序。
- 接口 → 代理 → 默认实现 SimpleJpaRepository。Query by Example = 样例对象当条件。
'''
