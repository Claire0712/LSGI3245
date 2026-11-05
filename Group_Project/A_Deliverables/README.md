# A 的阶段性交付（2026-11-05）

本包完成 A 可独立处理的两类数据、研究主线、来源整理和两分钟开场稿。全组 PPT 整合及最终研究结论仍等待 B、E 的成果及 C、D 的版本对齐。供 B 从本分支获取交接数据；最终合并遵循仓库的 Pull Request 审查流程。

## 交给谁、使用什么

- 给 B：`data/Facilities_A_handoff.csv`，422 行，五列顺序与 C 交接文件一致：`facility_type,facility_name,address,latitude,longitude`。
- 类型暂采用 `Badminton Court`、`Basketball Court`，与 C 的单数命名风格一致，须由 B 确认全组类型字典。D 使用 `Badminton Courts`、`Basketball Courts`，合并前必须映射。
- 给 B/C：`results/quality_issues.csv` 和两份 `data/*_cleaned.csv`。后者保留源行号、行政区、坐标差异、更新时间和来源。
- 给 A 自己：`presentation/A_Opening_and_Integration.md`，含两页英文内容、约两分钟讲稿、整合清单。
- 给报告撰写者：`docs/Research_and_Methods.md`，含研究问题、来源、清洗规则及可引用的方法段落。

## 当前检查结果

| 数据 | 输入 | 保留 | 完全重复删除 | 无效记录剔除 |
|---|---:|---:|---:|---:|
| Badminton |116|116|0|0|
| Basketball |306|306|0|0|

144 条记录的 geometry 坐标与属性经纬度差异超过 5 m，最大约 37.56 m。采用 D 相同的源 geometry 优先规则，不凭猜测修正。5 m 是审核阈值，不是精度承诺或错误判定。两条篮球记录的源行政区标签与 D 边界匹配不一致：源第 108 行为 WAN CHAI / 空间匹配 EASTERN；第 138 行为 LEI YUE MUN / 空间匹配 KWUN TONG。Lei Yue Mun 不是 18 区之一，不直接作为行政区导入。五列交接表不含行政区，B/C 应用最终 `HK_Admin` 重做空间匹配。

本包完成来源哈希、行数守恒、非空名称、有限坐标、香港范围筛查、源 ID 唯一性及 D 边界空间检查。未运行 B 的最终数据库，也未核验每一个设施入口或当前营业状态。422 是本次快照中按活动类别记录的设施地点数，不是球场片数。

## 复现

环境需要 Python 3、pyproj、shapely。本轮使用 pyproj 3.7.2、shapely 2.1.2。

```bash
python3 Group_Project/A_Deliverables/scripts/clean_a.py
```

脚本只重建本包清洗输出及审计文件，不改源 CSV。来源快照来自 D 包，SHA-256 与 D manifest 一致；不是 A 重新从官网下载的完整原始双语数据。完整来源与上游 commit 见 `data/source_manifest.json`，D 边界出处见 `data/source/district_provenance_D.json`。

## 合并前必须解决

1. B 确认五列结构和八种类型名称；由 B 生成全组 `facility_id` 与 `geom`。
2. C 的 2021 人口年份需在最终 PPT/报告中一致说明；课程 PDF 推荐 2016，C 文档称实际课程文件为 2021，本轮未独立检查课程网站。
3. D 演示快照健身室为 80 条，C 交付为 86 条。不能把 D 的 775 条八类演示数据整包追加到各人交接数据，否则重复；也不能将 D 的旧查询结果直接宣称为最终统一数据库结果。
4. B 合并 A/B/C/D 后，D/E 在同一最终数据库重跑查询，A 再更新总行数、流程与结论。
5. 两条行政区核查项须由 B/C 结合最终边界处理；坐标差异应在临界距离查询中保留局限说明。
