# 研究设计、来源与清洗方法

## 汇报主线

研究主题：香港运动与户外设施的空间分布、邻近可获得性及人口标准化供给。

通过八类设施点、行政区边界及人口数据建立 PostgreSQL/PostGIS 数据库，连接“某个地点周围有哪些设施”与“不同区的设施供给如何比较”。公共健康是研究背景；本项目不识别设施供给对健康或寿命的因果作用。

必做问题与负责人：

| 问题 | 查询输出 | 负责人 |
|---|---|---|
| 指定坐标最近的设施是什么？ |名称、类型、距离、相关信息|D|
| 指定坐标合理距离内有多少种设施？ |不同类型数及明细|D|
| 某类设施各区数量如何排名？ |包括零设施区的区级计数|E|
| 某类设施各区人均数量如何排名？ |设施数 / 人口；建议展示每万人数量|E|

D 当前使用 500 m 椭球面直线距离，并考察 400/800 m。它是邻近性的近似，不是沿道路的实际步行距离。全组最终采用的半径由 D/B 确认。额外问题可选“哪些区缺少某类设施”，但尚未列为完成结果，也不能替代个人额外问题及 SQL 的提交要求。

## 数据来源台账

本轮阅读的仓库版本：main `4eec86309bfb3358764ed715fc6f380c46668ba6`；C 分支 `d38ae67b90bbd368e622a7c8f842ff91ac0273b4`。

| 数据 | 当前可用来源 | 本轮使用及限制 |
|---|---|---|
| 羽毛球场 |D 包 LCSD/CSDI 英文字段快照；dataset `lcsd_rcd_1629267205214_38344`|A 清洗 116 条；D 记录下载日期 2026-11-03|
| 篮球场 |D 包 LCSD/CSDI 英文字段快照；dataset `lcsd_rcd_1629267205215_38105`|A 清洗 306 条；D 记录下载日期 2026-11-03|
| 网球场、游泳池 |D 有演示快照，正式交接由 B 提供|最终版本待 B 确认|
| 健身室、运动场 |C 分支 JSON 源数据及清洗包|C 报告 86/25 条；与 D 演示版本不同|
| 郊野公园、公园/动物园/花园 |D 正式负责的数据与清洗包|D 报告 25/124 条；本轮未独立重跑 D 全套查询|
| 行政区 |C 的 HKDistrict18 shapefile；D 另带 GeoJSON 参考边界|A 暂用 D 边界审核；最终用 C/B 的 HK_Admin|
| 人口 |C 的 census_cleaned 文件与来源说明|C 标记 2021 年、18 区；最终统计口径由 C 确认|

官方元数据链接与版本下载链接保留在 `../data/source_manifest.json`。源记录 LASTUPDATE、D 的下载日期及 A 的处理日期是不同概念，不能互相替代。不把 2026 下载的数据统称为“2026 年调查数据”。

## A 的清洗规则及理由

1. 不改源 CSV。验证 D manifest 的英文字段快照哈希，保留来源信息。
2. 清理英文名称、地址中的 HTML、实体与重复空格；不编造缺失地址。
3. 源数据每行视为某活动类别的一条设施记录。同场馆不同活动保留各自记录，不能跨类型去重。
4. 仅移除整行完全相同的源记录。同名同类型同坐标但其他字段不同的记录只标记，不自动合并。本次无此类候选重复。
5. 采用源 GeometryLongitude / GeometryLatitude，保留 WGS84 经纬度；检查数值有限性及宽松香港范围。无效记录隔离并写出原因；本次为零。
6. 比较属性坐标与 geometry 坐标，超过 5 m 标记审核，仍保留 geometry。不得因为存在坐标差异就删除记录。
7. 源行政区仅作审核，CENTRAL AND WESTERN 规范为 CENTRAL & WESTERN 以匹配 D 参考边界。空间匹配使用 covers，记录无匹配、多匹配及冲突；不凭名字猜测位置。
8. B 的五列交接表不含源 ID、行政区、geometry；审计明细另存。B 应使用 `ST_MakePoint(longitude, latitude)` 构造 EPSG:4326 点，顺序不能按 CSV 的纬度在前照搬。

这些是 A 的阶段性执行规则，兼容 C 五列结构并尽量沿用 D 坐标口径，不代表 B 或全组已经确认了最终规范。

## 可用于报告的英文方法段落

For Member A's contribution, 116 badminton and 306 basketball source records were processed from the English-column snapshots bundled with Member D's repository submission. Input SHA-256 hashes were checked against the supplied manifest. Names and addresses were normalized, and source geometry longitude and latitude were retained in WGS84. Records were screened for missing names, non-finite coordinates and coordinates outside a broad Hong Kong envelope. Only identical complete source rows were eligible for automatic removal; none were removed. All 422 records were retained. Geometry-to-attribute coordinate differences exceeding 5 m were flagged in 144 records, and two source district labels required review against the reference polygons. These flags were retained for investigation rather than treated as confirmed errors. The five-column handoff follows Member C's existing import structure; final category names, district assignment and database integration remain subject to Member B and C's validation. Counts represent facility records by activity category rather than individual courts. The snapshots and reference boundaries are version-specific and do not establish current operating status or pedestrian-network accessibility.
