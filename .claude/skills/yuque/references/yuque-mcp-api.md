# Yuque MCP API Reference

Complete reference for all yuque-mcp MCP server tools.

## Document Operations

### mcp__yuque-mcp__skylark_user_doc_detail

Retrieve full document content including metadata and markdown body.

**Parameters:**
- `namespace` (string, required): Knowledge base identifier (format: "user/book")
- `slug` (string, required): Document identifier

**Returns:**
```json
{
  "id": 466161970,
  "type": "Doc",
  "title": "Document Title",
  "slug": "doc-slug",
  "word_count": 886,
  "read_count": 0,
  "created_at": "2025-07-25T03:42:09.000Z",
  "updated_at": "2025-07-29T03:41:58.000Z",
  "body_md": "# Title\n\nContent in markdown format...",
  "user": { ... },
  "book": { ... },
  "url": "/go/doc/466161970"
}
```

**Example:**
```
namespace: "aimoyu/kg7h1z"
slug: "mw4dpwx835mx54zn"
```

---

### mcp__yuque-mcp__skylark_user_doc_list

List all documents in a knowledge base with pagination support.

**Parameters:**
- `namespace` (string, required): Knowledge base identifier
- `limit` (number, optional): Items per page (default: 100, max: 100)
- `offset` (number, optional): Pagination offset (default: 0)

**Returns:**
Array of document objects with metadata (without full body content).

**Example:**
```
namespace: "aimoyu/kg7h1z"
limit: 50
offset: 0
```

---

### mcp__yuque-mcp__skylark_user_doc_create

Create a new document in a knowledge base.

**Parameters:**
- `namespace` (string, required): Target knowledge base identifier
- `body` (string, required): Document content in markdown format
- `title` (string, optional): Document title (default: "无标题")
- `public` (string, optional): Visibility - "0" (private), "1" (public), "2" (enterprise) (default: "0")

**Returns:**
Created document object with full details.

**Example:**
```
namespace: "aimoyu/kg7h1z"
title: "New Document"
body: "# Introduction\n\nThis is the content..."
public: "0"
```

**Best Practices:**
- Always use markdown format for body
- Structure content with proper headings
- Set appropriate visibility level
- Verify namespace exists before creating

---

### mcp__yuque-mcp__skylark_user_doc_update

Update existing document content or metadata.

**Parameters:**
- `namespace` (string, required): Knowledge base identifier
- `slug` (string, required): Document identifier
- `title` (string, optional): New title (only if changing)
- `body` (string, optional): New content in markdown (only if changing)
- `public` (string, optional): New visibility setting (only if changing)

**Returns:**
Updated document object.

**Example:**
```
namespace: "aimoyu/kg7h1z"
slug: "mw4dpwx835mx54zn"
title: "Updated Title"
body: "# Updated Content\n\nNew content here..."
```

**Important:** Only include parameters that need to be changed. Omitting a parameter leaves it unchanged.

---

## Knowledge Base Operations

### mcp__yuque-mcp__skylark_user_book_list

List all accessible knowledge bases.

**Parameters:**
- `user_type` (string, required): "User" for personal, "Group" for team knowledge bases

**Returns:**
Array of knowledge base objects with metadata.

**Example:**
```
user_type: "User"
```

---

### mcp__yuque-mcp__skylark_user_book_update

Update knowledge base metadata.

**Parameters:**
- `namespace` (string, required): Knowledge base identifier
- `name` (string, optional): New name (only if changing)
- `description` (string, optional): New description (only if changing)
- `public` (string, optional): New visibility - "0", "1", or "2" (only if changing)

**Returns:**
Updated knowledge base object.

**Example:**
```
namespace: "aimoyu/kg7h1z"
name: "Updated Knowledge Base Name"
description: "Updated description"
```

---

## Search Operations

### mcp__yuque-mcp__skylark_search

Search for documents across accessible knowledge bases.

**Parameters:**
- `q` (string, required): Search keyword
- `pageNo` (number, optional): Page number (default: 1, min: 1)
- `pageSize` (number, optional): Results per page (default: 20, max: 20)

**Returns:**
```json
{
  "results": [
    {
      "title": "Document Title",
      "snippet": "...matching content snippet...",
      "url": "/user/book/doc-slug",
      "book": { ... },
      "updated_at": "2025-07-29T03:41:58.000Z"
    }
  ],
  "total": 45,
  "page": 1
}
```

**Example:**
```
q: "AI摸鱼"
pageNo: 1
pageSize: 20
```

**Pagination Example:**
To get all results when total > pageSize:
1. Call with pageNo: 1
2. Check total in response
3. Calculate pages: Math.ceil(total / pageSize)
4. Make additional calls with pageNo: 2, 3, etc.

---

## Common Patterns

### Pattern: URL to API Parameters

```python
# URL: https://yuque.antfin.com/aimoyu/kg7h1z/mw4dpwx835mx54zn
# Extract:
namespace = "aimoyu/kg7h1z"  # user/book
slug = "mw4dpwx835mx54zn"    # document
```

### Pattern: Read Then Update

```
1. Call skylark_user_doc_detail to get current content
2. Modify the content as needed
3. Call skylark_user_doc_update with only changed fields
```

### Pattern: Search and Read

```
1. Call skylark_search with keyword
2. Review results and identify relevant documents
3. For each relevant doc, call skylark_user_doc_detail
4. Process and synthesize information
```

### Pattern: Check Before Create

```
1. Call skylark_user_book_list to verify namespace exists
2. Optionally call skylark_user_doc_list to check for duplicates
3. Call skylark_user_doc_create with new content
```

---

## Error Handling

### Common Errors

**Authentication Errors:**
- User not logged in to Yuque
- MCP server not configured correctly
- Token expired or invalid

**Access Errors:**
- User lacks permission for requested resource
- Document or knowledge base is private
- Invalid namespace or slug

**Validation Errors:**
- Missing required parameters
- Invalid parameter format
- Content exceeds size limits

### Error Response Format

```json
{
  "error": {
    "message": "Error description",
    "code": "ERROR_CODE"
  }
}
```

---

## Rate Limits and Best Practices

### Rate Limits
- Yuque API has rate limits per user
- Avoid making rapid successive calls
- Implement retry logic with exponential backoff

### Best Practices
1. **Cache results**: Store document content locally when possible
2. **Batch operations**: Group related operations together
3. **Validate inputs**: Check parameters before API calls
4. **Handle errors gracefully**: Provide meaningful feedback to users
5. **Respect permissions**: Don't attempt unauthorized operations
6. **Use pagination**: Handle large result sets properly
7. **Read before write**: Always fetch current state before updates

---

## Advanced Usage

### Working with Large Documents

For documents exceeding context limits:
1. Read full document
2. Chunk content into manageable sections
3. Process sections independently
4. Synthesize results

### Bulk Operations

When operating on multiple documents:
1. Get document list first
2. Filter and prioritize
3. Process sequentially with delays
4. Track progress and failures
5. Provide summary of operations

### Content Transformation

When converting external content to Yuque:
1. Convert to markdown format
2. Clean and validate markdown
3. Structure with proper headings
4. Add metadata in frontmatter if needed
5. Create document with formatted content

---

## Integration Examples

### Example 1: Sync External Content

```
1. Fetch content from external source
2. Convert to markdown format
3. Search Yuque for existing document
4. If exists: update with skylark_user_doc_update
5. If not: create with skylark_user_doc_create
```

### Example 2: Knowledge Base Report

```
1. List all documents with skylark_user_doc_list
2. For each document, read content with skylark_user_doc_detail
3. Extract metadata and statistics
4. Aggregate and generate report
5. Optionally create summary document in Yuque
```

### Example 3: Cross-Document Search

```
1. Search with keyword using skylark_search
2. Read top N results with skylark_user_doc_detail
3. Extract relevant sections from each
4. Synthesize information across documents
5. Present consolidated findings
```
