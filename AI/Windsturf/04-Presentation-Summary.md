# Tóm Tắt Thuyết Trình - Cascade/Windsurf

## Slide 1: Giới Thiệu (2 phút)

### Hook
> "Có bao giờ bạn ước có một senior dev ngồi cạnh, sẵn sàng giúp đọc code, refactor, debug bất cứ lúc nào?"

### What is Cascade?
- **AI Agent** trong Windsurf IDE
- Không chỉ chat → **Tương tác trực tiếp với codebase**
- **Context-aware**: Hiểu toàn bộ project, không chỉ prompt
- **Tool-augmented**: Read, edit, run commands, search

### Key Differentiators
```
AI Chat thường          Cascade Agent
─────────────────       ─────────────────
Chỉ trả lời text    →    Thực hiện actions
Session memory      →    Persistent database
Passive             →    Proactive suggestions
```

---

## Slide 2: Kiến Trúc Hệ Thống (3 phút)

### Architecture Overview

```
┌─────────────────────────────────────────┐
│           Windsurf IDE                  │
├─────────────────────────────────────────┤
│  ┌─────────┐  ┌─────────┐  ┌──────────┐ │
│  │ Editor  │  │  Chat   │  │ Explorer │ │
│  └────┬────┘  └────┬────┘  └────┬─────│ │
│       └─────────────┴────────────┘     │
│                    │                    │
│       ┌────────────┴───────────┐       │
│       │    Cascade Agent       │       │
│       ├────────────────────────┤       │
│       │ • Context Management   │       │
│       │ • Memory System        │       │
│       │ • Tool Execution       │       │
│       │ • Planning & Verify    │       │
│       └────────────────────────┘       │
└─────────────────────────────────────────┘
```

### Core Components

| Component | Chức năng |
|-----------|-----------|
| **Tool System** | Read, edit, search, run commands |
| **Memory** | Lưu conventions, preferences |
| **Context** | Workspace state, active files |
| **Agent Core** | Planning, execution, verification |

---

## Slide 3: Configuration System (4 phút)

### `.windsurf/` Directory Structure

```
.windsurf/
├── workflows/     ← Slash commands (/deploy)
├── skills/        ← Auto-detect patterns
├── agents/        ← Specialized agents (@reviewer)
└── rules.md       ← Global conventions
```

### The 4 Components

| Component | Trigger | Auto-Apply | Use Case |
|-----------|---------|------------|----------|
| **Workflows** | `/command` | ❌ | Guidelines, runbooks |
| **Skills** | Pattern detect | ✅ | Refactor auto |
| **Rules** | Always | ✅ | Project standards |
| **Agents** | `@agent` | ❌ | Complex tasks |

### Live Demo Ideas
1. **Workflow**: Gõ `/deploy-checklist` → Hiện checklist
2. **Skill**: Paste HTML với inline styles → Auto suggest MUI conversion
3. **Rule**: Luôn áp dụng "Use TypeScript strict mode"

---

## Slide 4: Best Practices (4 phút)

### Prompt Engineering

```markdown
❌ "Sửa code giùm"

✅ "Refactor hàm `processData` trong 
   @/src/utils/data.ts:1-50 
   sang async/await, thêm error handling"
```

### Context-Rich Requests

| Thông tin | Ví dụ |
|-----------|-------|
| Location | `@/src/components/Button.tsx:25` |
| Expected | "Click → loading 2s → redirect" |
| Constraint | "Bundle size < 100KB" |
| Reference | "Pattern như @/src/utils/api.ts:1-30" |

### Tool Safety Protocol

```
Read → Search → Plan → Edit → Verify
         ↑___________________|
         (Always verify sau edit)
```

---

## Slide 5: Real-World Use Cases (4 phút)

### Case 1: Refactor Legacy

```
Scenario: JSX + PropTypes → TypeScript + MUI

Cascade Actions:
1. Read files, check dependencies
2. Search for patterns to migrate
3. Convert PropTypes → TS interfaces
4. migrate makeStyles → sx prop
5. Run type check & tests
6. Verify results

Result: 15 files refactored in 30 minutes
```

### Case 2: Debug Production

```
User: "API lỗi 500, log đây"

Cascade:
1. grep_search stack trace
2. Read API layer code
3. Identify: null input + missing error handling
4. Implement fix với validation
5. Add proper error messages
6. Suggest test cases
```

### Case 3: Performance Optimization

```
Before: 2.5MB bundle, 4.2s load

Cascade:
- Implement code splitting (lazy load)
- Dynamic imports cho heavy libs
- Asset optimization

After: 850KB bundle, 1.1s load
```

---

## Slide 6: Comparison (2 phút)

### Cascade vs Alternatives

| Feature | Copilot | ChatGPT | Cascade |
|---------|---------|---------|---------|
| In-IDE | ✅ | ❌ | ✅ |
| Workspace access | ❌ | ❌ | ✅ |
| Run commands | ❌ | ❌ | ✅ |
| Persistent memory | ❌ | ❌ | ✅ |
| Configurable | ❌ | ❌ | ✅ |
| Agent behavior | ❌ | ❌ | ✅ |

### When to Use What

- **Copilot**: Inline completions, quick snippets
- **ChatGPT**: Research, explanations, brainstorming
- **Cascade**: Full workflow, complex tasks, project-wide changes

---

## Slide 7: Demo (5 phút)

### Demo Script

```
1. Setup (1 min)
   - Show .windsurf/ structure
   - Explain workflows vs skills

2. Workflow Demo (2 min)
   - Type: "/deploy-checklist"
   - Walk through checklist
   - Show how it guides the process

3. Live Coding (2 min)
   - "Refactor this component to use MUI"
   - Show Cascade reading, planning, executing
   - Show verification step
```

### Tips for Live Demo
- Chuẩn bị project sẵn
- Có backup plan nếu API slow
- Focus vào workflow/skill, không phải specific code

---

## Slide 8: Q&A Preparation

### Common Questions & Answers

**Q: Cascade có thể thay thế developer không?**
> A: Không. Cascade là **pair programmer** - giúp nhanh hơn, không thay thế thinking. Developer vẫn cần review, architect, quyết định business logic.

**Q: Làm sao đảm bảo code quality?**
> A: Cascade có **safety protocols** - luôn read trước edit, verify sau changes, và destructive actions cần approval. Plus: Configurable rules và workflows cho standards.

**Q: Memory có bảo mật không?**
> A: Memory lưu project conventions, không sensitive data. Secrets nên dùng environment variables, never hardcoded.

**Q: Học Cascade mất bao lâu?**
> A: Basic usage: 1-2 giờ. Advanced (workflows/skills): 1-2 ngày. ROI: Tiết kiệm 30-50% thời gian coding routine.

---

## Slide 9: Key Takeaways (2 phút)

### 3 Main Points

1. **Cascade = Context-Aware AI Agent**
   - Không chỉ chat, mà tương tác trực tiếp codebase
   - Persistent memory + configurable behavior

2. **Configuration System Powerful**
   - Workflows: Manual triggers (/command)
   - Skills: Auto-detect patterns
   - Rules: Always-on conventions

3. **Professional Workflow**
   - Plan → Execute → Verify
   - Safety-first với approval gates
   - Minimal, focused edits

### Call to Action

> "Hãy thử Windsurf IDE + Cascade cho project tiếp theo của bạn. Bắt đầu với workflows đơn giản, dần dần xây dựng skills cho team."

---

## Appendix: Resources

### Documentation
- Windsurf Docs: https://codeium.com/windsurf
- Cascade Guide: https://codeium.com/cascade

### Sample Workflows
- `/deploy-checklist`
- `/code-review`
- `/mui-reminder`

### Contact
- GitHub: [your-repo]
- Email: [your-email]

---

## Speaker Notes

### Timing
- Slide 1-2: 5 phút (Giới thiệu + Kiến trúc)
- Slide 3-4: 8 phút (Config + Best practices)
- Slide 5-6: 6 phút (Use cases + Comparison)
- Slide 7: 5 phút (Demo)
- Slide 8-9: 4 phút (Q&A + Takeaways)
- **Tổng: ~30 phút**

### Audience Engagement
- Pause sau mỗi section chính
- Hỏi: "Ai đã dùng Copilot/ChatGPT chưa?"
- Poll: "Thấy feature nào hữu ích nhất?"

### Backup Content
- Nếu demo fail: Show screenshots pre-capture
- Nếu hết giờ: Skip to Key Takeaways
- Nếu còn giờ: Deep dive vào skill development
