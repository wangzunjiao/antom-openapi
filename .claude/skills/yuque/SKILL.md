---
name: yuque
description: 全面的语雀文档操作工具集，支持以下核心功能：1) **读取文档** - 解析URL并获取文档内容，支持图片理解与上下文提取；2) **搜索文档** - 按关键词搜索有权限访问的文档，支持分页；3) **创建文档** - 在指定知识库创建新文档，支持Markdown格式和公开性设置；4) **更新文档** - 修改文档标题、内容或可见性，支持增量更新；5) **知识库管理** - 列出个人/团队知识库、列出知识库文档、更新知识库设置；6) **URL解析** - 从yuque.com或yuque.antfin.com自动提取namespace和slug参数；7) **错误诊断** - 检测并引导解决Auth error等认证问题。触发条件：用户消息包含yuque.antfin.com、yuque.com、语雀、yuque，或请求读取/总结/分析/搜索/创建/更新/打开语雀文档或知识库。**在调用yuque-mcp工具前必须先加载此skill。** 此skill提供图片理解能力、参数自动解析和交互式询问等功能，这些是直接调用MCP工具无法获得的。
allowed-tools: Read, Bash, AskUserQuestion
---

# 语雀文档操作技能

## 概述

此技能通过 yuque-mcp MCP 服务器工具提供操作语雀文档的专业能力。它支持读取、搜索、创建、更新和管理语雀文档及知识库，包括 URL 解析、参数提取和 API 使用模式。

## 何时使用此技能

当用户进行以下操作时激活此技能：

**文档操作场景：**
- 提供语雀 URL（例如：`https://yuque.antfin.com/aimoyu/kg7h1z/mw4dpwx835mx54zn`）
- 请求阅读或总结语雀文档
- 想要搜索包含特定关键词的文档
- 需要在语雀知识库中创建新文档
- 要求更新现有文档内容或元数据
- 请求列出知识库或文档
- 想要管理知识库设置

**错误诊断场景：**
- yuque-mcp 工具执行失败（如返回 Auth error、认证错误等）
- 用户报告无法使用语雀相关功能
- 需要排查 yuque-mcp 工具的连接或权限问题

## 核心功能

### 1. URL 解析和参数提取

语雀 URL 遵循以下模式：
```
https://yuque.antfin.com/{namespace}/{slug}
或
https://yuque.com/{user}/{book_namespace}/{doc_slug}
```

**关键参数：**
- `namespace`：知识库标识符（格式：`user/book_slug` 或独立形式）
- `slug`：文档标识符（在知识库内唯一）

使用 `scripts/parse_yuque_url.py` 自动从 URL 中提取这些参数：

```bash
python scripts/parse_yuque_url.py "https://yuque.antfin.com/aimoyu/kg7h1z/mw4dpwx835mx54zn"
```

### 2. 读取文档

**工作流程：**
1. 解析 URL 以提取 `namespace` 和 `slug`
2. 使用 `mcp__yuque-mcp__skylark_user_doc_detail` 工具
3. 处理返回的 markdown 内容

**示例请求：** "阅读这篇语雀文档的内容"

**工具使用：**
```
mcp__yuque-mcp__skylark_user_doc_detail
  - namespace: "aimoyu/kg7h1z"
  - slug: "mw4dpwx835mx54zn"
```

**响应包括：** title（标题）、body_md（markdown 内容）、元数据（created_at、updated_at、word_count 等）

**图片处理：**
- 如果文档内容包含图片链接（通常为 `![](url)` 或 HTML img 标签格式），主动询问用户是否需要理解图片内容
- 如果用户确认需要理解图片，使用 `scripts/understand_image.py` 逐个分析图片
- 将图片理解结果整合到文档内容的总结中，提供更全面的信息

### 3. 搜索文档

**工作流程：**
1. 使用 `mcp__yuque-mcp__skylark_search` 搭配关键词
2. 查看搜索结果（标题、摘要、URL）
3. 可选择读取相关文档的完整内容

**示例请求：** "搜索关于AI的语雀文档"

**工具使用：**
```
mcp__yuque-mcp__skylark_search
  - q: "AI"
  - pageNo: 1 (可选，默认 1)
  - pageSize: 20 (可选，最大 20)
```

**最佳实践：** 对于多页结果，使用递增的 `pageNo` 进行顺序调用。

### 4. 列出知识库

**工作流程：**
1. 使用 `mcp__yuque-mcp__skylark_user_book_list` 获取可访问的知识库
2. 指定 user_type："User" 表示个人知识库，"Group" 表示团队知识库

**示例请求：** "列出我的所有知识库"

**工具使用：**
```
mcp__yuque-mcp__skylark_user_book_list
  - user_type: "User" 或 "Group"
```

**响应包括：** 知识库名称、namespace、描述、公开状态

### 5. 列出知识库中的文档

**工作流程：**
1. 获取知识库 namespace
2. 使用 `mcp__yuque-mcp__skylark_user_doc_list`
3. 如需要，处理分页

**示例请求：** "查看XX知识库下的所有文档"

**工具使用：**
```
mcp__yuque-mcp__skylark_user_doc_list
  - namespace: "aimoyu/kg7h1z"
  - limit: 100 (可选，默认 100，最大 100)
  - offset: 0 (可选，默认 0)
```

### 6. 创建文档

**工作流程：**
1. 确定目标知识库 namespace
2. 准备 markdown 格式的文档内容
3. 使用 `mcp__yuque-mcp__skylark_user_doc_create`

**示例请求：** "在XX知识库创建一篇关于XXX的文档"

**工具使用：**
```
mcp__yuque-mcp__skylark_user_doc_create
  - namespace: "aimoyu/kg7h1z"
  - title: "文档标题" (可选，默认为"无标题")
  - body: "# 标题\n\n正文内容..." (必需，markdown 格式)
  - public: "0" (私密), "1" (公开), "2" (企业) (可选，默认 0)
```

**最佳实践：**
- 始终使用 markdown 格式的正文内容
- 包含适当的标题结构
- 设置合适的公开可见性
- 创建前验证 namespace 是否存在

### 7. 更新文档

**工作流程：**
1. 解析 URL 或获取 namespace 和 slug
2. 可选择先读取当前内容
3. 使用 `mcp__yuque-mcp__skylark_user_doc_update`
4. 只包含需要更新的字段

**示例请求：** "更新这篇文档的内容"

**工具使用：**
```
mcp__yuque-mcp__skylark_user_doc_update
  - namespace: "aimoyu/kg7h1z"
  - slug: "mw4dpwx835mx54zn"
  - title: "新标题" (可选，仅在更改时)
  - body: "更新后的内容" (可选，仅在更改时)
  - public: "1" (可选，仅在更改可见性时)
```

**重要：** 只传递需要更新的参数。省略未更改的字段。

### 8. 更新知识库设置

**工作流程：**
1. 获取知识库 namespace
2. 使用 `mcp__yuque-mcp__skylark_user_book_update`
3. 只包含要更新的字段

**示例请求：** "更新知识库信息"

**工具使用：**
```
mcp__yuque-mcp__skylark_user_book_update
  - namespace: "aimoyu/kg7h1z"
  - name: "新名称" (可选)
  - description: "新简介" (可选)
  - public: "1" (可选，0=私密，1=公开，2=企业)
```

## 常见工作流程

### 工作流程 A：从 URL 读取并总结文档

1. 接收用户提供的语雀 URL
2. 使用 `scripts/parse_yuque_url.py` 或手动提取解析 URL
3. 使用 namespace 和 slug 调用 `mcp__yuque-mcp__skylark_user_doc_detail`
4. 从响应中提取 body_md 内容
5. 为用户分析和总结内容
6. 呈现要点、结构和见解

### 工作流程 B：搜索、审查和提取信息

1. 接收用户的搜索查询
2. 使用关键词调用 `mcp__yuque-mcp__skylark_search`
3. 查看搜索结果并识别相关文档
4. 对每个相关文档调用 `mcp__yuque-mcp__skylark_user_doc_detail`
5. 跨文档提取和综合信息
6. 向用户呈现综合发现

### 工作流程 C：创建综合文档

1. 了解用户的内容要求
2. 确定目标知识库 namespace
3. 使用适当的标题以 markdown 格式构建内容
4. 使用完整内容调用 `mcp__yuque-mcp__skylark_user_doc_create`
5. 确认创建成功并提供文档 URL
6. 如需要，提供调整建议

### 工作流程 D：更新现有文档

1. 定位文档（通过 URL 或搜索）
2. 使用 `mcp__yuque-mcp__skylark_user_doc_detail` 读取当前内容
3. 了解需要哪些更改
4. 准备更新的内容（标题、正文或可见性）
5. 仅使用更改的字段调用 `mcp__yuque-mcp__skylark_user_doc_update`
6. 确认更新成功

### 工作流程 E：理解文档中的图片

1. 读取文档内容后,检查 body_md 中是否包含图片链接
2. **提取图片上下文信息：**
   - 识别每张图片所在的章节标题（向上查找最近的 # ## ### 标题）
   - 提取图片前后的文字上下文（前后各 1-2 行）
   - 记录图片的 alt 文本（如果有）
   - 按文档顺序编号

3. **必须使用 AskUserQuestion 工具发起澄清询问：**

   **重要：不要在文本中直接输出选项让用户手动回复，必须调用 AskUserQuestion 工具创建可点击的选项表单。**

   在调用工具前，先输出图片位置信息：
   ```
   文档中含有 3 张图片：
   - 图片1：位于「系统架构」章节，描述系统组件关系
   - 图片2：位于「部署流程」章节，展示部署步骤
   - 图片3：位于「监控配置」章节，显示监控面板截图
   ```

   然后**调用 AskUserQuestion 工具**：
   ```json
   {
     "questions": [{
       "question": "文档中含有3张图片，是否需要理解图片内容？",
       "header": "图片理解",
       "options": [
         {"label": "是，需要理解所有图片", "description": "使用视觉模型分析所有图片内容"},
         {"label": "是，只理解部分图片", "description": "选择性分析特定图片"},
         {"label": "否，只看文字内容", "description": "跳过图片，仅总结文字"}
       ],
       "multiSelect": false
     }]
   }
   ```

4. 如果用户确认需要理解图片:
   - 对每个图片 URL 调用 `python scripts/understand_image.py <image_url> "请详细描述这个图片的内容"`
   - 根据图片上下文定制提示词（如架构图、流程图、截图等）
5. 收集所有图片的理解结果
6. 将图片理解结果整合到文档总结中,按图片出现顺序标注,关联对应章节
7. 向用户呈现包含图片内容描述的完整文档总结

**图片 URL 及上下文提取示例：**
```markdown
## 系统架构

我们的系统采用微服务架构：

![架构图](https://example.com/arch.png)

各服务之间通过 gRPC 通信...
```
提取结果：
- 所在章节：`系统架构`
- Alt 文本：`架构图`
- 图片 URL：`https://example.com/arch.png`
- 上下文：`我们的系统采用微服务架构` / `各服务之间通过 gRPC 通信`

**支持的图片格式：**
- Markdown 格式: `![图片说明](https://example.com/image.jpg)` → 提取 URL 和 alt 文本
- HTML 格式: `<img src="https://example.com/image.jpg" alt="说明">` → 提取 URL 和 alt 属性
- 注意处理语雀特定的图片域名（如 cdn.nlark.com、mass.alipay.com 等）

## 最佳实践

### URL 处理
- 始终准确地从 URL 中提取 namespace 和 slug
- 支持 `yuque.com` 和 `yuque.antfin.com` 两个域名
- 使用解析脚本以确保提取一致性
- 在 API 调用前验证提取的参数

### 内容格式化
- 始终使用 markdown 格式的文档正文
- 保持适当的标题层次结构（# ## ###）
- 包含带语言规范的代码块
- 适当使用表格、列表和其他 markdown 功能

### API 使用模式
- 更新前先读取以了解当前状态
- 只传递需要修改的参数
- 处理大结果集的分页
- 检查响应状态并优雅地处理错误

### 用户沟通
- 在破坏性操作前确认行动
- 提供文档内容的清晰摘要
- 在响应中包含文档 URL（如相关）
- 提供后续步骤或相关操作建议

## 错误处理

常见问题及解决方案：

**Auth error / 认证错误：**
- **症状：** yuque-mcp 工具执行时返回 "Auth error" 或认证失败相关错误
- **原因：** 用户尚未获得办公网授权访问 yuque-mcp 服务
- **解决方案：** 引导用户访问以下链接申请办公网授权：
  ```
  https://antmcp.alipay.com/mcp/detail/mcp.ant.faas.skylarkmcpserver.skylarkmcpserver
  ```
- **用户提示：** 明确告知用户需要先申请授权才能使用 yuque-mcp 功能，授权通过后即可正常使用

**无效的 namespace/slug：**
- 验证 URL 解析是否正确
- 检查用户是否有权访问文档
- 确认知识库是否存在

**访问被拒绝：**
- 用户可能没有访问/修改权限
- 检查文档/知识库是否为私密
- 验证身份验证状态

**内容过大：**
- 语雀文档有大小限制
- 考虑拆分为多个文档
- 总结或重构内容

## 资源

### scripts/
- `parse_yuque_url.py` - 从语雀 URL 中提取 namespace 和 slug
- `understand_image.py` - 使用 GLM-4.6V 模型理解和描述图片内容

### references/
- `yuque-mcp-api.md` - 所有 yuque-mcp 工具的完整 API 参考
- `best-practices.md` - 语雀操作的高级技巧和模式
- `image-understanding.md` - 图片理解功能的详细说明和使用示例

如需详细的 API 规范和高级使用模式，请在需要时使用 Read 工具参考参考文档。
