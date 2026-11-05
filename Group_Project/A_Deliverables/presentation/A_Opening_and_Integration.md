# A 的开场与整合稿

状态：2026-11-05 草稿；以下是可直接放入 PPT 的两页文字，不是已整合完成的全组 PPT。开场采用研究目标表述，避免把尚未合并的数据库称作已完成。

## Slide 1 — Sports and outdoor facilities in Hong Kong

**Research focus:** Spatial distribution, local availability and population-adjusted provision.

- Where is the nearest facility to a given location?
- How many facility types are available within a specified distance?
- How do districts compare in facility counts and facilities per capita?

**Scope:** Eight facility categories; Hong Kong administrative districts.

## Slide 2 — Data and workflow

**Inputs:** Facility locations + district boundaries + district population.

**Workflow:** Source checks → standardized cleaning → Facilities / HK_Admin / census → spatial and non-spatial queries → maps and district comparisons.

- A–D clean their allocated facility categories; B consolidates Facilities.
- C prepares district and population tables; D/E run the queries.
- A integrates the presentation; E coordinates figures, rehearsal and Q&A.

**Interpretation:** Facility records by activity type; straight-line proximity is a walking-access proxy.

制作时可用简单横向流程箭头。最终数据总数留待合并验证，不填写 D 演示库的 775。

## English script — approximately two minutes

Good morning. Our project examines the distribution of sports and outdoor facilities in Hong Kong. These facilities provide opportunities for physical activity, but their availability can vary between locations and districts. Our aim is to use a geospatial database to describe those differences in a consistent and reproducible way.

We focus on four questions. First, which facility is nearest to a given location? Second, how many different facility types are available within a specified distance? Third, how do districts rank by the number of a selected facility type? Finally, how does that ranking change when we account for district population?

Our data cover eight categories, including badminton and basketball courts, fitness rooms, swimming pools and outdoor parks. We combine facility locations with administrative boundaries and district population data. Each facility record represents an activity at a location, so our counts should not be interpreted as the number of individual courts.

The workflow begins with source checks and data cleaning. We standardize names, categories and coordinates, while keeping an audit trail for records that need review. The database design then organizes the information into three linked tables: Facilities, HK_Admin and census. Spatial queries support the location-based questions, and district-level queries support the population comparisons.

We interpret distance-based results as proximity indicators, rather than exact walking routes. We also distinguish the dates of the facility snapshots from the census year. These choices help us explain both the findings and their limitations. Next, our second speaker will introduce the cleaning process and the Facilities table.

讲稿约 260 个英文词；实际是否两分钟须自行计时排练。A 清洗细节交给 B 的清洗部分展示，开场不逐条讲异常。

## 全组整合顺序与检查清单

| 环节 | 时间 | 当前材料/待补事项 |
|---|---|---|
| A 研究问题、数据、流程 |2 min|本稿；最终人口年份和设施总数待对齐|
| B 数据清洗、Facilities |3 min|等待 B；可引用 A 422 条与审核清单|
| C schema 与关联 |3 min|C 分支已有 schema 图；合并后确认最终字段|
| D 最近设施、距离范围 |3 min|D 包已有稿与结果；统一设施表后需重跑|
| E 区域比较、发现、结论 |4 min|等待 E；结论须由最终输出支持|

整合时逐项确认：

- 八类类型名称完全一致；A/C 的单数与 D 的复数经过显式映射。
- B 只合并每人负责的记录，不重复导入 D 的全类型演示快照。
- C 的人口年份、人口覆盖范围、18 区名称与 E 使用的一致。
- D 所用半径、距离算法及展示单位一致；地图标注为研究点/参考点，不默认是真实入口。
- D/E 对同一版本最终数据库运行；图表记录运行版本或日期。
- 数量图保留零设施行政区；每万人指标注明分母和公式。
- C/D 来源不一致及 A 坐标审核项处理结果记录在报告中。
- 一页一个主要信息；全组计时 15 分钟。额外问题如展示，纳入 E 原有时间，另一题可留备用页。
- 每个人的报告、SQL 和额外问题提交要求另行检查，不能用本次小组开场稿替代。

## A 可回答的 Q&A

**Did you count individual courts?** No. We counted source facility records by activity category; a venue can contain multiple courts.

**Did you delete uncertain coordinates?** Not automatically. We retained source geometry, checked alternative coordinate attributes, and documented discrepancies for review.

**Are these actual walking distances?** No. The current D implementation uses geodesic straight-line distances as a proximity proxy.

**Which population year did you use?** C's current package uses 2021 and reports that this is the course-supplied census file. We will keep that year explicit in the final integrated database and presentation.

**Can you conclude that facilities improve longevity?** This project describes spatial provision and accessibility proxies; it does not estimate a causal health effect.
