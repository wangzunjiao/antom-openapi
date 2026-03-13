# Yuque Operations Best Practices

Advanced tips and patterns for effective Yuque document operations.

## Content Organization

### Knowledge Base Structure

**Principle**: Organize knowledge bases by domain, project, or team.

**Good Examples:**
- `team-docs/onboarding` - Team onboarding materials
- `project-x/architecture` - Project X technical architecture
- `personal/notes` - Personal knowledge notes

**Anti-patterns:**
- Mixing unrelated content in one knowledge base
- Creating too many granular knowledge bases
- Using unclear or generic names

### Document Hierarchy

**Best Practice**: Use document titles and internal links to create logical hierarchies.

**Pattern:**
```markdown
# Main Topic

See related documents:
- [Subtopic 1](./subtopic-1)
- [Subtopic 2](./subtopic-2)

## Overview
...
```

**Tips:**
- Create index documents for complex topics
- Use consistent naming conventions
- Maintain bidirectional links when appropriate

---

## Content Formatting

### Markdown Best Practices

**Heading Structure:**
```markdown
# Document Title (H1 - use once)

## Main Section (H2)

### Subsection (H3)

#### Detail Level (H4)
```

**Code Blocks:**
```markdown
​```python
def example():
    return "Always specify language"
​```
```

**Tables:**
```markdown
| Feature | Status | Notes |
|---------|--------|-------|
| Read    | ✓      | Implemented |
| Write   | ✓      | Implemented |
```

**Lists:**
```markdown
- Use unordered lists for related items
- Each item should be concise

1. Use ordered lists for sequential steps
2. Number will auto-increment
3. Maintain logical order
```

### Visual Elements

**Images:**
- Use descriptive alt text
- Keep file sizes reasonable
- Host images in Yuque when possible
- Use relative paths for internal images

**Callouts:**
```markdown
> **Note**: Important information here

> ⚠️ **Warning**: Critical warning here

> 💡 **Tip**: Helpful suggestion here
```

---

## Workflow Optimization

### Read Operations

**Cache Frequently Accessed Documents:**
```
If document is read multiple times:
1. Read once and store in memory
2. Reuse cached content
3. Check updated_at to detect changes
4. Refresh cache if needed
```

**Selective Reading:**
```
For large knowledge bases:
1. Use search to find relevant documents
2. Read only necessary documents
3. Extract specific sections
4. Avoid loading entire knowledge base
```

### Write Operations

**Draft Then Publish:**
```
1. Create document with public: "0" (private)
2. Review and refine content
3. Update with public: "1" or "2" when ready
```

**Incremental Updates:**
```
For long documents:
1. Update sections independently
2. Read current content first
3. Modify only changed sections
4. Preserve unchanged content
```

**Batch Document Creation:**
```
When creating multiple documents:
1. Prepare all content first
2. Validate namespace exists
3. Create documents sequentially with small delays
4. Log results for each creation
5. Handle failures gracefully
```

---

## Search Strategies

### Effective Search Queries

**Specific Keywords:**
- Good: "React hooks useEffect"
- Bad: "React stuff"

**Phrase Search:**
- Use quotes for exact phrases (if supported)
- "error handling" vs error handling

**Iterative Refinement:**
```
1. Start with broad search
2. Review results
3. Refine with more specific terms
4. Combine related keywords
```

### Post-Search Processing

**Filter Results:**
```
1. Search with keyword
2. Check each result's title and snippet
3. Identify most relevant documents
4. Read only filtered subset
5. Extract and synthesize information
```

**Cross-Reference:**
```
1. Search for primary topic
2. Note related documents in results
3. Search for related topics
4. Map connections between documents
5. Create comprehensive understanding
```

---

## Security and Permissions

### Document Visibility

**Public Levels:**
- `"0"` - Private: Only visible to author and authorized users
- `"1"` - Public: Visible to anyone with link
- `"2"` - Enterprise: Visible within organization

**Guidelines:**
- Default to private for new documents
- Review content before making public
- Use enterprise visibility for internal docs
- Regularly audit public documents

### Access Control

**Best Practices:**
- Verify user has permission before operations
- Handle access denied errors gracefully
- Don't expose sensitive information in errors
- Log access attempts for audit

---

## Error Handling Strategies

### Graceful Degradation

**Pattern:**
```
try:
    result = read_document(namespace, slug)
except AccessDenied:
    inform_user("You don't have permission to access this document")
    suggest_alternatives()
except NotFound:
    inform_user("Document not found")
    offer_to_search()
except RateLimitExceeded:
    inform_user("Too many requests")
    retry_with_backoff()
```

### User Communication

**Good Error Messages:**
- "Unable to access document. You may not have permission, or it may have been deleted."
- "Document not found. Would you like me to search for similar documents?"
- "The knowledge base 'xyz' doesn't exist. Let me list your available knowledge bases."

**Poor Error Messages:**
- "Error 403"
- "API call failed"
- "Something went wrong"

---

## Performance Optimization

### Minimize API Calls

**Pattern: Batch Information Gathering**
```
Instead of:
1. Get document list
2. For each doc: read full content
3. Process each doc

Do:
1. Get document list
2. Filter by metadata (title, updated_at)
3. Read only filtered documents
4. Process in batch
```

### Context Management

**For Long Sessions:**
```
1. Keep track of loaded documents
2. Reference by title or ID instead of re-reading
3. Update only when necessary
4. Clear old references when done
```

### Pagination Efficiency

**Smart Pagination:**
```
1. Start with reasonable page size (20)
2. Check total results
3. If total > threshold, ask user to refine search
4. Otherwise, fetch remaining pages
5. Aggregate results efficiently
```

---

## Content Quality

### Writing Guidelines

**Clear Structure:**
- Start with overview/summary
- Use logical progression
- Group related information
- End with conclusions or next steps

**Actionable Content:**
- Be specific and concrete
- Provide examples
- Include code snippets when relevant
- Link to related resources

**Maintenance:**
- Add creation/update dates
- Mark deprecated information
- Update links regularly
- Archive obsolete documents

### Documentation Standards

**Technical Documents:**
```markdown
# Title

## Overview
Brief description of purpose and scope

## Prerequisites
What reader needs to know/have

## Main Content
Core information with examples

## Troubleshooting
Common issues and solutions

## References
Links to related documents
```

**Meeting Notes:**
```markdown
# Meeting Title - Date

## Attendees
- Name 1
- Name 2

## Agenda
1. Topic 1
2. Topic 2

## Discussion
Key points discussed

## Action Items
- [ ] Task 1 (@owner)
- [ ] Task 2 (@owner)

## Next Steps
What happens next
```

---

## Integration Patterns

### With External Tools

**Git + Yuque:**
```
Use case: Sync documentation
1. Store source in Git
2. On commit, trigger sync
3. Convert to markdown if needed
4. Update or create Yuque document
5. Maintain version mapping
```

**Notion + Yuque:**
```
Use case: Migrate content
1. Export from Notion
2. Convert format to Yuque markdown
3. Preserve structure and links
4. Create documents in Yuque
5. Verify migration completeness
```

### Automation Workflows

**Daily Summary:**
```
1. Search for documents updated today
2. Read each document
3. Extract key changes
4. Generate summary document
5. Create/update summary in Yuque
```

**Content Audit:**
```
1. List all documents in knowledge base
2. Check each document's updated_at
3. Identify stale documents (e.g., >6 months old)
4. Generate audit report
5. Create action items for updates
```

---

## Troubleshooting Guide

### Common Issues

**Issue: Can't find document by URL**
Solution:
1. Verify URL is complete and correct
2. Parse URL to extract namespace and slug
3. Check if user has access
4. Try searching by title instead

**Issue: Document content truncated**
Solution:
1. Check if response has pagination
2. Verify full body_md is returned
3. Handle large documents in chunks
4. Consider document size limits

**Issue: Update not reflecting**
Solution:
1. Verify update call succeeded
2. Check if parameters were correct
3. Read document again to confirm
4. Clear cache if caching is used

**Issue: Search returns too many results**
Solution:
1. Refine search terms
2. Add more specific keywords
3. Filter results by metadata
4. Limit to specific knowledge base

---

## Advanced Techniques

### Document Templates

**Create Reusable Templates:**
```markdown
# [Project Name] - Weekly Update

## Week of [Date]

### Accomplishments
-

### Challenges
-

### Next Week
-

### Blockers
-
```

**Usage:**
1. Store template in assets or as reference
2. Load template when needed
3. Fill in placeholders
4. Create document with filled content

### Content Analysis

**Extract Insights:**
```
1. Read multiple related documents
2. Extract key themes and topics
3. Identify patterns and trends
4. Generate summary or report
5. Create new document with insights
```

**Link Analysis:**
```
1. Read document
2. Extract all internal links
3. Map document relationships
4. Create knowledge graph
5. Identify gaps or orphaned documents
```

### Bulk Operations

**Mass Update:**
```
Use case: Update footer on all documents
1. List all documents in knowledge base
2. For each document:
   a. Read current content
   b. Append/update footer
   c. Update document
   d. Log result
3. Generate completion report
```

**Migration:**
```
Use case: Move documents to new knowledge base
1. List documents in source knowledge base
2. For each document:
   a. Read full content
   b. Create in target knowledge base
   c. Verify creation
   d. Optionally delete from source
3. Update cross-references
```

---

## Maintenance Checklist

### Regular Tasks

**Weekly:**
- [ ] Review recent document changes
- [ ] Check for broken links
- [ ] Update frequently accessed documents
- [ ] Archive outdated content

**Monthly:**
- [ ] Audit document permissions
- [ ] Review knowledge base organization
- [ ] Update documentation standards
- [ ] Clean up drafts and duplicates

**Quarterly:**
- [ ] Comprehensive content audit
- [ ] Update templates and guidelines
- [ ] Review and optimize workflows
- [ ] Gather feedback and improve
