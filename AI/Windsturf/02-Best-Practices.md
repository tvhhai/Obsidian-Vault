# Cascade - Best Practices Chuyên Nghiệp

## 1. Prompt Engineering cho Cascade

### 1.1 Nguyên Tắc Viết Prompt Hiệu Quả

```markdown
❌ Tránh:
"Sửa cái này cho tôi"
"Làm cho nó chạy được"
"Code giùm tôi"

✅ Nên dùng:
"Refactor hàm `processData` trong @/src/utils/data.ts:1-50 
sử dụng async/await thay vì callback, thêm error handling"

"Implement unit test cho `UserService` với coverage cho:
- happy path
- null input
- database error"
```

### 1.2 Context-Rich Prompts

Luôn cung cấp đủ context:

| Yếu tố | Ví dụ |
|--------|-------|
| **File location** | `@/src/components/Button.tsx:25` |
| **Expected behavior** | "Khi click, hiển thị loading state 2s rồi redirect" |
| **Constraints** | "Không dùng external library, bundle size < 100KB" |
| **Reference** | "Giống pattern trong @/src/utils/api.ts:1-30" |

---

## 2. Workflow System - Chuyên Nghiệp

### 2.1 Tạo Workflow Hiệu Quả

```yaml
---
description: Pre-deployment checklist for React projects
---

## Deployment Checklist

### 1. Build Verification
- [ ] Run `npm run build` - no errors
- [ ] Check bundle size < 500KB
- [ ] Verify no console warnings

### 2. Testing
- [ ] All unit tests pass: `npm test`
- [ ] Critical user flows tested manually
- [ ] Cross-browser check (Chrome, Firefox, Safari)

### 3. Environment
- [ ] Environment variables configured
- [ ] API endpoints point to production
- [ ] Sentry/Datadog initialized

### 4. Rollback Plan
- [ ] Previous version tagged
- [ ] Database migration tested
- [ ] Rollback procedure documented
```

### 2.2 Sử dụng Slash Commands

```
Cấu trúc hội thoại chuyên nghiệp:

User: /deploy-checklist
Cascade: [Hiển thị checklist]

User: ✅ Build xong, bundle 450KB
Cascade: [Tiếp tục verify các bước còn lại]

User: Lỗi ở bước test, log: [paste error]
Cascade: [Phân tích lỗi và suggest fix]
```

---

## 3. Skill Development

### 3.1 Auto-Detect Skill Pattern

```yaml
---
description: Auto-convert inline styles to MUI Box
---

When detecting HTML elements with inline styles in React files:

1. Check if MUI is available in the project
2. Convert pattern:
   ```jsx
   // Before
   <div style={{ display: 'flex', padding: 16 }}>
   
   // After
   <Box sx={{ display: 'flex', p: 2 }}>
   ```

3. Apply MUI spacing scale: 1 unit = 8px
4. Import Box if not already imported

Priority: Apply only when explicitly requested or in "refactor mode"
```

### 3.2 Khi Nào Dùng Skill vs Workflow

| Tình huống | Dùng | Lý do |
|------------|------|-------|
| "Luôn luôn convert div → MUI" | Skill | Auto-apply |
| "Nhắc tôi nhớ MUI pattern" | Workflow | Manual trigger |
| "Chỉ refactor khi tôi yêu cầu" | Workflow | User control |
| "Generate boilerplate khi detect new component" | Skill | Auto-apply |

---

## 4. Memory Management

### 4.1 Lưu Trữ Thông Tin Hiệu Quả

```markdown
## Nên lưu vào Memory:

✅ Technical Stack
"Project dùng React 18, MUI v5, React Query, React Router v6"

✅ Coding Conventions  
"API calls luôn dùng axios instance từ @/src/lib/api.ts"
"Naming: components PascalCase, utils camelCase"

✅ Project-Specific Knowledge
"Auth flow: login → set cookie → redirect /dashboard"
"Database: User table có soft delete, check `deleted_at`"

❌ Không nên lưu:
- Temporary debugging info
- Code snippets dùng 1 lần
- Task-specific instructions
```

### 4.2 Memory Maintenance

| Action | When | How |
|--------|------|-----|
| Create | New project conventions established | Explicit request |
| Update | Stack/Convention thay đổi | `create_memory` with same ID |
| Delete | Outdated or incorrect info | `create_memory` with Action: delete |

---

## 5. Tool Usage Patterns

### 5.1 Exploration Strategy

```
Complex Task: "Thêm feature X vào hệ thống"

Step 1: Khám phá
└── code_search: "Find where feature X related code exists"
    └── grep_search: "Find specific patterns"
        └── read_file: "Understand current implementation"

Step 2: Plan
└── Analyze: Dependencies, side effects, test strategy

Step 3: Implement
└── multi_edit: "Apply changes across files"
    └── run_command: "Verify build/test"

Step 4: Verify
└── Check results, run tests
```

### 5.2 Command Safety Protocol

```markdown
## Trước khi run command:

1. Kiểm tra destructive potential
   - Delete files? → Confirm explicitly
   - Modify system? → Warn user
   - Network requests? → Note in response

2. Verify working directory
   - Có phải project root?
   - Có file lock (package-lock, yarn.lock)?

3. Check for alternatives
   - Có tool API thay thế command?
   - Cần user confirmation?
```

---

## 6. Code Quality Standards

### 6.1 Edit Discipline

```markdown
## Nguyên tắc khi edit code:

1. Minimal Changes
   - Một edit = một logical change
   - Không mix refactor + feature trong một PR

2. Preserving Style
   - Match existing code style
   - Không thêm comments không cần thiết
   - Không đổi tên variable nếu không liên quan

3. Verification
   - Luôn đọc lại sau khi edit
   - Check syntax errors
   - Verify no unintended changes
```

### 6.2 Citation Format

Luôn dùng format chuẩn khi reference code:

```markdown
Inline: `@/src/utils/file.ts:30`

Block:
```@/src/utils/file.ts:1-3
import React from 'react';
import { Box } from '@mui/material';
```

Không dùng:
- Plain text paths
- Bulleted lists
- Relative paths
```

---

## 7. Error Handling

### 7.1 When Cascade Gets Stuck

```markdown
## Scenario: Cascade không hiểu context

User: Hãy sửa lỗi này
[Không cung cấp context]

✅ Response:
"Tôi cần thêm thông tin:
1. File nào đang bị lỗi?
2. Error message cụ thể?
3. Expected behavior là gì?"

## Scenario: Tool call fail

Cascade: [Attempt edit nhưng file đã thay đổi]

✅ Response:
"File đã được modify bên ngoài. Đọc lại và retry..."
```

### 7.2 Communication Guidelines

| Tình huống | Response Pattern |
|------------|------------------|
| Unclear request | Ask 1-2 clarifying questions |
| Missing context | Request specific file/info |
| Ambiguous intent | Propose 2-3 approaches, ask preference |
| Tool failure | Explain, then retry or escalate |

---

## 8. Advanced Patterns

### 8.1 Multi-Session Projects

```markdown
## Cho dự án dài hạn:

1. Tạo progress.md ghi lại:
   - Completed features
   - Pending decisions
   - Known issues

2. Session handoff:
   - "Tiếp tục từ task X"
   - Reference progress.md

3. Memory updates:
   - Lưu architectural decisions
   - Update conventions khi evolve
```

### 8.2 Team Collaboration

```markdown
## Khi làm việc nhóm:

1. Consistent Conventions
   - Shared `.windsurf/rules.md`
   - Common workflows cho team

2. Code Review Integration
   - Workflow cho review checklist
   - Skill cho auto-detect common issues

3. Knowledge Transfer
   - Document domain knowledge trong memory
   - Onboarding workflows cho new members
```

---

## 9. Quick Reference

### 9.1 Decision Matrix

| Bạn muốn... | Dùng... | Ví dụ |
|-------------|---------|-------|
| Manual trigger | Workflow | `/deploy-checklist` |
| Auto-apply | Skill | Auto-convert patterns |
| Always apply | Rule | `.windsurf/rules.md` |
| Complex task | Agent | `@code-reviewer` |
| Remember info | Memory | Store conventions |

### 9.2 Command Cheat Sheet

```markdown
Navigation:
- `@/path/to/file.ts:10` - Reference line 10
- `code_search` - Explore codebase
- `grep_search` - Find patterns

Editing:
- `edit` - Single change
- `multi_edit` - Multiple changes
- `write_to_file` - New file

Execution:
- `run_command` - Terminal command
- `blocking: true` - Wait for completion

Management:
- `todo_list` - Track tasks
- `create_memory` - Store info
```
