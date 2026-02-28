# Danbooru Tag 中英文对照表 

![Tag Count](https://count.getloli.com/@ffdkj_tags?name=ffdkj&theme=booru-lewd&padding=6&offset=0&align=center&scale=2&pixelated=1&darkmode=auto&num=293608) 

## ***每日更新 !***

截止03月01日 00:12 已收录并翻译 **293608**+ 条标签。

收录所有 post_count >= 10 的 tag，使用人工智能 **Gemini 3 Flash** 翻译 + 能工智人校对。如使用过程中遇到翻译错误可访问https://tagsuggest.zeabur.app 提交纠错或联系 2624696826a@gmail.com。

## 数据库结构：

| 字段名 (Column) | 类型 (Type) | 约束 (Constraint) | 描述 (Description) |
| :--- | :--- | :--- | :--- |
| **`name`** | `TEXT` | `PRIMARY KEY` | **英文标签名**。Danbooru 原始标签（单词间以下划线 `_` 分隔）。 |
| **`category`** | `INTEGER` | - | **标签分类 ID**。例如：0-常规, 1-艺术家, 3-版权/作品, 4-角色, 5-元数据。 |
| **`cn_name`** | `TEXT` | - | **中文翻译**。由 Gemini 3 Flash 翻译 + 能工智人校对的结果。 |
| **`post_count`** | `INTEGER` | - | **引用数量**。该标签在 Danbooru 上的帖子总数，反映标签的热门程度。 |

---

> **Acknowledgment:** > README 的实时计数展示由 [Moe-Counter](https://github.com/journey-ad/Moe-Counter) 提供支持。感谢作者 [@journey-ad](https://github.com/journey-ad) 开发的猫娘计数器！
