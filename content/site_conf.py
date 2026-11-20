# 站点配置：学习路线分组、模拟卷结构
TITLE = '考试冲刺 · Spring 全家桶'
BRAND = '考试冲刺'
BRAND_SUB = 'Spring 全家桶'
STORAGE_KEY = 'spring-review-v2'   # 和 Python 站同在 swt-eriri.github.io 下，键名必须不同，否则进度会互相覆盖

MODULE_ORDER = ['base', 'ds', 'jdbc', 'tx', 'jpa', 'mybatis', 'nosql', 'reactor', 'aop',
                'mvc', 'view', 'client', 'rest', 'boot', 'ops',
                'cloud', 'discovery', 'resilience', 'config', 'stream']

STAGES = [
    {'n': 1, 'name': '数据访问', 'desc': '第 1—38 讲：Spring 基础、JDBC、事务、JPA / MyBatis、Redis 与缓存、响应式、AOP', 'mods': ['base', 'ds', 'jdbc', 'tx', 'jpa', 'mybatis', 'nosql', 'reactor', 'aop']},
    {'n': 2, 'name': 'Web 开发', 'desc': '第 39—66 讲：Spring MVC、视图、HTTP 客户端、REST、WebFlux', 'mods': ['mvc', 'view', 'client', 'rest']},
    {'n': 3, 'name': 'Spring Boot', 'desc': '第 67—85 讲：自动配置、起步依赖、配置加载、Actuator、打包部署', 'mods': ['boot', 'ops']},
    {'n': 4, 'name': 'Spring Cloud', 'desc': '第 86—122 讲：微服务、注册发现、熔断限流、配置中心、消息、链路追踪', 'mods': ['cloud', 'discovery', 'resilience', 'config', 'stream']},
]

# 模拟卷：考试题型未知，按「全选择题」估计；每个模块抽 2 道单选，重点模块多抽，另加 10 道多选。
# 模拟考只抽主线题（tags 含 basic），进阶题不进模拟卷。
_SINGLE = {m: 2 for m in MODULE_ORDER}
_SINGLE.update({'tx': 3, 'mvc': 3, 'boot': 3, 'resilience': 3, 'view': 1, 'cloud': 2})
_MULTI = ['tx', 'nosql', 'mvc', 'rest', 'boot', 'ops', 'cloud', 'resilience', 'config', 'stream']
BLUEPRINT = ([{'m': m, 'type': 'single', 'tag': 'basic'} for m in MODULE_ORDER for _ in range(_SINGLE[m])]
             + [{'m': m, 'type': 'multi', 'tag': 'basic'} for m in _MULTI])
