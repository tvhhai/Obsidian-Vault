# Cascade/Windsurf - Tổng Quan Kiến Trúc

## 1. Cascade Là Gì?

Cascade là AI agent được tích hợp trong Windsurf IDE, hoạt động như một **pair programmer** đồng hành cùng developer trong suốt quá trình coding.

### Khác biệt so với AI coding thông thường:

| Feature | AI Chat thông thường | Cascade Agent |
|---------|---------------------|---------------|
| Context | Chỉ dựa trên prompt | Toàn bộ workspace + tools |
| Action | Chỉ trả lời text | Read, edit, run commands, search |
| Initiative | Passive (chờ hỏi) | Proactive (đề xuất, detect issues) |
| Memory | Session-based | Persistent database |

---

## 2. Kiến Trúc Hệ Thống

```
┌─────────────────────────────────────────────────────────┐
│                     Windsurf IDE                        │
├─────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────┐  │
│  │   Editor    │  │   Chat      │  │  File Explorer  │  │
│  │  (Monaco)   │  │  (Cascade)  │  │                 │  │
│  └──────┬──────┘  └──────┬──────┘  └────────┬────────┘  │
│         └─────────────────┴──────────────────┘           │
│                           │                             │
│         ┌─────────────────┴──────────────────┐         │
│         │         Cascade Agent Core          │         │
│         ├─────────────────────────────────────┤         │
│         │  • Tool System (Read/Edit/Search) │         │
│         │  • Context Management               │         │
│         │  • Memory System                    │         │
│         │  • Planning & Execution             │         │
│         └─────────────────────────────────────┘         │
└─────────────────────────────────────────────────────────┘
```

---

## 3. Core Components

### 3.1 Tool System

Cascade có quyền truy cập các tool để tương tác với codebase:

| Tool | Chức năng | Use Case |
|------|-----------|----------|
| `read_file` | Đọc nội dung file | Hiểu code hiện tại |
| `edit` / `multi_edit` | Sửa code | Implement changes |
| `write_to_file` | Tạo file mới | Generate boilerplate |
| `grep_search` | Tìm kiếm trong codebase | Locate functions, patterns |
| `find_by_name` | Tìm file theo tên | Navigation |
| `run_command` | Chạy terminal commands | Build, test, deploy |
| `code_search` | Semantic search | Complex exploration |

### 3.2 Memory System

Lưu trữ thông tin dài hạn qua 3 loại:

```
Memory Hierarchy:
├── Global Rules (Luôn áp dụng)
│   └── "Always use TypeScript strict mode"
│
├── User-Provided Memories
│   └── "Project dùng MUI, không dùng Bootstrap"
│
└── System-Retrieved Memories
    └── Từ conversation trước (auto-detect relevance)
```

### 3.3 Context Management

Cascade tự động quản lý context window:
- **Active Document**: File đang mở trong IDE
- **Mentioned Files**: `@file` trong chat
- **Workspace State**: Toàn bộ project structure
- **Search Results**: Kết quả tìm kiếm

---

## 4. Configuration System (`.windsurf/`)

### 4.1 Folder Structure

```
.windsurf/
├── workflows/          # Slash commands (manual trigger)
│   ├── mui-reminder.md
│   ├── deploy-checklist.md
│   └── code-review.md
│
├── skills/             # Auto-detect skills
│   ├── convert-html-to-mui.md
│   ├── generate-tests.md
│   └── refactor-patterns.md
│
├── agents/             # Specialized agents
│   ├── code-reviewer.md
│   ├── testing-agent.md
│   └── docs-agent.md
│
└── rules.md            # Workspace-wide rules
```

### 4.2 So sánh Components

| Component | Trigger | Use Case | Auto-Apply? |
|-----------|---------|----------|-------------|
| **Workflows** | `/command` | Guidelines, runbooks, templates | ❌ Manual |
| **Skills** | Pattern detect | Refactor, boilerplate generation | ✅ Yes |
| **Rules** | Always | Project conventions, standards | ✅ Yes |
| **Agents** | `@agent` or workflow | Specialized tasks | ❌ Manual |

---

## 5. Communication Flow

```
User Request
     ↓
[Cascade Agent]
     ↓
┌────────────────────────────────────┐
│ 1. Parse Intent                    │
│ 2. Retrieve Relevant Memories      │
│ 3. Plan Actions (if needed)        │
│ 4. Execute with Tools              │
│ 5. Verify Results                  │
└────────────────────────────────────┘
     ↓
Response + Actions
```

---

## 6. Key Principles

### 6.1 Agent Behavior

- **Proactive**: Đề xuất improvements, detect issues
- **Minimal**: Prefer single-line edits over large changes
- **Verifiable**: Luôn kiểm tra kết quả trước khi xác nhận
- **Transparent**: Giải thích lý do đằng sau actions

### 6.2 Tool Usage Discipline

1. **Read trước khi Edit**: Luôn đọc file trước khi sửa
2. **Search để Explore**: Dùng code_search cho complex tasks
3. **Batch Independent Actions**: Chạy parallel khi không dependent
4. **Verify Commands**: Kiểm tra status sau run_command

### 6.3 Safety Protocols

| Action | Safety Level | Auto-Run? |
|--------|--------------|-----------|
| Read files | ✅ Safe | Yes |
| Edit files | ⚠️ Destructive | No (needs approval) |
| Run commands | ⚠️ Context-dependent | Judgment call |
| Delete files | ❌ Unsafe | Never auto |

---

## 7. Tóm Tắt

Cascade = **Context-Aware AI Agent** với:
- ✅ Full workspace access
- ✅ Persistent memory
- ✅ Tool-augmented capabilities
- ✅ Configurable behavior via `.windsurf/`
- ✅ Safety-first execution

> **Mental Model**: Think of Cascade as a senior developer pair programming with you - they can read, write, run commands, and remember your preferences, but always ask before making destructive changes.
