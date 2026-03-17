# Antom OpenAPI 规范项目

## 项目概述

本项目存储 Antom 支付服务的 OpenAPI 接口规范文件，所有接口定义以 JSON 和 YAML 两种格式维护，用于 API 文档生成、SDK 生成和契约测试。

## 目录结构

```
antom-openapi/
├── json/          # OpenAPI 3.1.0 JSON 格式规范文件
├── yaml/          # OpenAPI 3.1.0 YAML 格式规范文件
├── .claude/
│   ├── skills/    # Claude Code 技能定义
│   └── agents/    # Subagent 配置
└── CLAUDE.md      # 本文件
```

## OpenAPI 文件命名规范

格式：`{ApiName}-v1.{json|yaml}`

示例：
- `PayRequest-v1.json` / `PayRequest-v1.yaml`
- `RefundRequest-v1.json` / `RefundRequest-v1.yaml`

## 依赖管理

### OpenAPI 验证工具（可选）

```bash
# 安装 Spectral CLI 用于高级验证
npm install -g @stoplight/spectral-cli
```

### YAML 处理工具

```bash
# Python 环境
pip install pyyaml

# 或使用 JS 工具
npm install -g js-yaml
```

## 自动化工作流程

### 从语雀文档同步新接口

用户提供语雀文档 URL，自动完成以下流程：

1. **读取语雀文档** (`yuque-reader` agent)
   - 解析 URL 并获取文档内容
   - 提取接口定义、参数、响应结构

2. **生成 OpenAPI 规范** (`openapi-updater` agent)
   - 创建/更新对应的 JSON 和 YAML 文件
   - 遵循 OpenAPI 3.1.0 规范

3. **同步 Schema 模型** (`schema-sync` agent)
   - 确保所有文件中的 `components.schemas` 保持一致
   - 同一个 Schema 在所有文件中定义相同

4. **验证规范正确性** (`openapi-validator` agent)
   - 检查语法、结构、引用完整性
   - 确认 JSON 和 YAML 文件一致

5. **提交到 Git** (`git-commit` agent)
   - 生成规范的提交信息
   - 创建 commit 并等待确认后推送

### 使用示例

```
# 从语雀文档同步新接口
/sync-openapi https://yuque.antfin.com/namespace/slug

# 同步所有 Schema 模型
/sync-schemas

# 验证所有 OpenAPI 文件
/validate-openapi
```

## Schema 同步规则

所有 OpenAPI 文件共享同一个 Schema 定义空间：

1. **基础类型必须一致**：如 `Amount`、`Currency`、`Merchant` 等在所有文件中定义必须完全相同
2. **引用路径统一**：使用 `#/components/schemas/{SchemaName}` 格式
3. **版本化规范**：所有文件版本为 `1.0.0`
4. **双格式同步**：JSON 和 YAML 文件内容保持一致

## Agents 概览

| Agent | 职责 |
|-------|------|
| `yuque-reader` | 从语雀读取接口文档，提取 API 定义 |
| `openapi-updater` | 根据接口定义生成/更新 OpenAPI 文件 |
| `schema-sync` | 同步所有文件中的 Schema 定义 |
| `openapi-validator` | 验证 OpenAPI 规范的正确性 |
| `git-commit` | 提交变更到 Git 仓库 |

## 开发规范

1. 所有接口文件必须同时生成 JSON 和 YAML 两种格式
2. Schema 定义遵循命名规范：大驼峰（PascalCase）
3. 必须包含示例数据（example）用于文档生成
4. 所有 `$ref` 引用必须指向文件内存在的 Schema
5. 提交前必须通过验证检查

## Git 工作流

遵循 Conventional Commits 规范：

```
<type>(<scope>): <subject>

<body>

<footer>
```

Types:
- `add`: 新增接口
- `update`: 更新接口
- `fix`: 修复接口规范
- `sync`: Schema 同步
- `refactor`: 重构/格式调整