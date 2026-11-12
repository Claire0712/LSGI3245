# Integrated rehearsal notes

15 main slides + 2 backup slides. Planned allocation: A 2 min, B 3 min, C 3 min, D 3 min, E 4 min. Timing includes explanation and transitions; rehearse with a timer.

## Slide 1

A — 20 seconds. Good morning. Our project examines sports and outdoor facilities in Hong Kong. We use a spatial database to connect local proximity questions with comparisons between administrative districts. Today we will explain the data, database design and four required queries, followed by the main findings and limitations.
中文提示：开场只介绍研究目的，不在封面解释数据异常。

## Slide 2

We ask four questions. For a given location, which facility is nearest? Within a specified distance, how many distinct facility types are available? For a selected facility type, how do districts rank by the number of records? Finally, how does that ranking change after accounting for population? These questions connect individual locations with district-level provision. We treat public health as the motivation, but our database does not estimate a causal effect on health or life expectancy. 中文提示：四个问题分为地点查询与行政区比较。

Source: Claire0712/LSGI3245, main f0081c9, B_Deliverables.zip (12 November 2026 inspection). Results are supplied reference outputs; final team PostGIS execution confirmation remains pending.

## Slide 3

Our consolidated table contains 781 facility records across eight activity categories. We combine these points with 18 district polygons and the 2021 census data supplied in C’s package. Members A to D cleaned their allocated categories, and B standardized the handoffs into one Facilities table. C prepared the boundary and population tables. Spatial and attribute queries then support the results. One record describes an activity at a facility location. A sports centre may therefore appear in more than one category, and these counts are not counts of individual courts. 中文提示：说明781、8类、18区及2021人口，随后交给B。

Source: Claire0712/LSGI3245, main f0081c9, B_Deliverables.zip (12 November 2026 inspection). Results are supplied reference outputs; final team PostGIS execution confirmation remains pending.

## Slide 4

We consolidated A’s 422 records, B’s 99, C’s 111 and D’s 149, giving 781 records. The handoff structure contains type, name, address, latitude and longitude. We normalized text and category names and handled WGS84 coordinates, Hong Kong Grid coordinates and degrees-minutes-seconds representations. We kept an audit trail for coordinate discrepancies rather than deleting valid venues automatically. The common type vocabulary is important because singular and plural labels would otherwise inflate the distinct-type query. 中文提示：不要逐条念八类数据，重点讲统一格式为何必要。

Source: Claire0712/LSGI3245, main f0081c9, B_Deliverables.zip (12 November 2026 inspection). Results are supplied reference outputs; final team PostGIS execution confirmation remains pending.

## Slide 5

The reference spatial audit matches 779 of the 781 points to a district polygon using ST_Covers. Two waterfront park points fall just outside the supplied boundaries, at about 0.38 metres and 10.95 metres from the closest polygon. We retain their source coordinates so that proximity queries remain unchanged. We distinguish strict district matches from a 15-metre tolerance estimate. For the main district comparisons we use strict matching, with the tolerance results reserved for sensitivity discussion. Four provider district labels also differ from polygon assignments. These differences require explanation, not undocumented coordinate changes. 中文提示：781是完整主表，779是严格空间归属数，并不矛盾。

Source: Claire0712/LSGI3245, main f0081c9, B_Deliverables.zip (12 November 2026 inspection). Results are supplied reference outputs; final team PostGIS execution confirmation remains pending.

## Slide 6

Each facility has a primary key and a Point geometry in EPSG 4326. Geometry construction puts longitude first and latitude second. We constrain facility_type to the eight agreed names. Geometry indexes support district joins, while a geography expression index supports metre-based distance queries. The load script inserts records when the table is empty. If the table already contains data, it verifies the expected records and stops on discrepancies. This is a verified load, not an upsert that overwrites conflicting data. 中文提示：用一个点说明经纬度顺序；避免把加载方式叫upsert。

Source: Claire0712/LSGI3245, main f0081c9, B_Deliverables.zip (12 November 2026 inspection). Results are supplied reference outputs; final team PostGIS execution confirmation remains pending.

## Slide 7

Facilities stores the point locations and descriptive attributes. HK_Admin stores district identifiers, standardized district names and polygon geometries. Census stores population, population percentage and census year without a geometry column. The primary key in Facilities identifies facility records, while the district name connects Census to HK_Admin. Facility-to-district membership is computed with a spatial predicate. This spatial relationship is distinct from a conventional foreign-key link. Keeping population outside the facility table avoids repeating district population on every facility row. 中文提示：这是逻辑结构；最终主键和外键以组内执行的DDL为准。

Source: Claire0712/LSGI3245, main f0081c9, B_Deliverables.zip (12 November 2026 inspection). Results are supplied reference outputs; final team PostGIS execution confirmation remains pending.

## Slide 8

For district comparisons we start with all 18 administrative districts and left join facilities using ST_Covers. Starting with the districts preserves areas with zero facilities of a selected type. We then join Census on the standardized district name. Population-adjusted provision equals the count divided by the district population, multiplied by one hundred thousand. We use COUNT of the facility identifier rather than COUNT star so that empty matches do not become one facility. The category filter must preserve the left join. 中文提示：解释零值区保留和COUNT(facility_id)，不用逐字读SQL。

Source: Claire0712/LSGI3245, main f0081c9, B_Deliverables.zip (12 November 2026 inspection). Results are supplied reference outputs; final team PostGIS execution confirmation remains pending.

## Slide 9

The integrated design needs three checks before interpretation. First, all facility geometries must use the same coordinate reference system and the same type vocabulary. Second, all 18 census districts must match the administrative table. Third, district totals must account for the two points outside the strict polygons. The census reference year is 2021, whereas facility sources have different update dates. These data describe a mixed-date snapshot, so we should not present the ratios as perfectly simultaneous measurements. 中文提示：讲检查逻辑；本汇报中的结果来自B交付的参考输出，正式演讲前确认数据库实测。

Source: Claire0712/LSGI3245, main f0081c9, B_Deliverables.zip (12 November 2026 inspection). Results are supplied reference outputs; final team PostGIS execution confirmation remains pending.

## Slide 10

We calculate spheroidal distances in metres using WGS84 geography and order facilities by distance. The table reports four deliberately selected study coordinates. In Hung Hom the closest record is Hong Tat Path Garden, categorized as basketball, about 433 metres away. In Central the closest record in the 781-record table is the badminton activity at Hong Kong Park Sports Centre, about 509.5 metres away. Sha Tin Park and Tung Chung Swimming Pool are closest to the other two points. Central differs from D’s preliminary 775-record snapshot because the consolidated fitness-room source uses different coordinates. Therefore we use the updated reference result here. These study points are not verified entrances, and the distances do not follow walking routes. 中文提示：中环必须用509.5米，不再用旧稿504.7米。

Source: Claire0712/LSGI3245, main f0081c9, B_Deliverables.zip (12 November 2026 inspection). Results are supplied reference outputs; final team PostGIS execution confirmation remains pending.

## Slide 11

The second query counts distinct activity categories within 500 metres, rather than just the number of facility records. Hung Hom has one record of one type. Central has none within this radius. Sha Tin and Tung Chung each have five records covering four types. We also check 400 and 800 metres because conclusions depend on the radius. At Central, increasing the radius to 800 metres includes ten records across four types. Zero within 500 metres therefore does not mean the wider area has no facilities. A straight-line radius is a simple proximity indicator and does not account for road access, barriers or opening hours. 中文提示：区分设施条数与种类数，解释半径敏感性。

Source: Claire0712/LSGI3245, main f0081c9, B_Deliverables.zip (12 November 2026 inspection). Results are supplied reference outputs; final team PostGIS execution confirmation remains pending.

## Slide 12

For the district comparison we select basketball so that one consistent category illustrates both required rankings. The chart includes all 18 districts, ordered by the number of records. Kowloon City has the most, with 30, followed by Yuen Long with 27 and North with 25. Southern has six. Across all districts there are 306 basketball records. Every basketball point has a strict polygon match, so the two coastal park exceptions do not change this example. Counts describe the scale of recorded provision, but districts differ in population and facility capacity. We therefore use the population-adjusted comparison on the next slide. 中文提示：这是用B参考表准备的E部分，需E审核接手。

Source: Claire0712/LSGI3245, main f0081c9, B_Deliverables.zip (12 November 2026 inspection). Results are supplied reference outputs; final team PostGIS execution confirmation remains pending.

## Slide 13

After dividing by 2021 district population, North ranks first at about 8.07 basketball records per one hundred thousand residents. Kowloon City ranks second at 7.31 and Islands third at 6.48. Yuen Long, second by count, moves to eleventh in the supplied per-capita ranking at 4.04. This is why total counts and population-adjusted measures answer different questions. The rate remains a simple provision indicator. It does not measure the number of courts inside each venue, utilisation, quality or access across district boundaries. 中文提示：重点对比九龙城、北区、元朗的排序变化。

Source: Claire0712/LSGI3245, main f0081c9, B_Deliverables.zip (12 November 2026 inspection). Results are supplied reference outputs; final team PostGIS execution confirmation remains pending.

## Slide 14

The location queries show different nearby facility variety at the four study points. This difference also changes when we alter the radius, as the Central example demonstrates. The district comparison shows that the highest count does not necessarily produce the highest population-adjusted rate. Kowloon City leads the basketball count, while North leads the per-capita rate. We should avoid treating these rankings as a complete measure of fairness or actual access. A district boundary does not prevent residents from visiting neighbouring facilities, and our data do not contain facility capacity, affordability or travel-network information. 中文提示：每个结论对应前面一张图，不扩大为健康因果结论。

Source: Claire0712/LSGI3245, main f0081c9, B_Deliverables.zip (12 November 2026 inspection). Results are supplied reference outputs; final team PostGIS execution confirmation remains pending.

## Slide 15

Our database combines 781 records from eight facility categories with district boundaries and population data. It supports the four required queries using a common schema and explicit spatial rules. The results distinguish local proximity, district counts and population-adjusted provision. Retaining source records and documenting boundary exceptions makes the comparisons easier to reproduce and interpret. Thank you. We welcome your questions. 中文提示：简短总结后进入Q&A，不再新增数字或研究问题。

Source: Claire0712/LSGI3245, main f0081c9, B_Deliverables.zip (12 November 2026 inspection). Results are supplied reference outputs; final team PostGIS execution confirmation remains pending.

## Slide 16

Only the Parks, Zoos and Gardens category changes under the supplied 15-metre tolerance estimate. The estimate assigns two points to the nearest districts without moving their coordinates. This does not independently establish their legal district membership. The main basketball charts are identical under both approaches.

Source: Claire0712/LSGI3245, main f0081c9, B_Deliverables.zip (12 November 2026 inspection). Results are supplied reference outputs; final team PostGIS execution confirmation remains pending.

## Slide 17

Counts from the consolidated 781-record master. These count activity-category facility records, not individual playing courts or unique buildings. All categories appear in the location queries. The two main district charts use basketball as the specified facility type.

Source: Claire0712/LSGI3245, main f0081c9, B_Deliverables.zip (12 November 2026 inspection). Results are supplied reference outputs; final team PostGIS execution confirmation remains pending.