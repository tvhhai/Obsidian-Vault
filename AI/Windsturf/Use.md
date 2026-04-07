**Folder structure hiện tại của Cascade:**

|Location|Mục đích|Khi nào dùng|
|---|---|---|
|`.windsurf/workflows/*.md`|**Slash commands** - Gõ `/command` để gọi|Khi cần trigger thủ công|
|`.windsurf/skills/*.md`|**Auto-detect skills** - Cascade tự nhận diện|Khi muốn auto-apply|
|`SKILL.md` (root)|Legacy skill format|Ít dùng, đang deprecated|

**Tôi chọn workflows vì:**

- MUI reminder là **guideline** cần gõ `/mui-reminder` để xem, không phải skill Cascade tự động áp dụng
    
- Skills folder dành cho skills có thể **auto-invoke** khi detect pattern
    
- Ví dụ: Nếu để trong skills, Cascade có thể tự động refactor HTML→MUI mỗi khi thấy `<div style=` mà không hỏi ý kiến
    

---

## 2. Giải thích chi tiết các khái niệm trong Cascade:

### **A. Workflows** (`.windsurf/workflows/*.md`)

yaml

---

description: Mô tả ngắn gọn

---

Nội dung hướng dẫn cụ thể

- **Cách dùng**: Gõ `/workflow-name` trong chat
    
- **Khi nào dùng**:
    
    - Cần nhắc nhở developer về best practices
        
    - Runbook cho deployment, testing
        
    - Template cho code review
        
- **Không auto-apply** - Phải gõ slash command thủ công
    

### **B. Skills** (`.windsurf/skills/*.md`)

yaml

---

description: Mô tả skill

---

Instruction cho Cascade khi detect pattern

- **Cách dùng**: Cascade **tự động** invoke khi phù hợp
    
- **Khi nào dùng**:
    
    - Refactor pattern cụ thể (e.g., HTML→MUI)
        
    - Generate boilerplate code
        
    - Fix common issues
        
- **Auto-apply**: Yes - Cascade đọc và tự quyết định áp dụng
    

### **C. Memory** (Database)

Lưu trữ thông tin dài hạn:

- **Global rules**: Luôn áp dụng (ví dụ: React best practices)
    
- **User-provided**: User tự thêm
    
- **System-retrieved**: Từ conversation trước
    

**Khi nào dùng:**

- Remember user preferences
    
- Project-specific conventions
    
- Technical stack info
    

### **D. Rules** (`.windsurf/rules.md` hoặc trong memory)

- Áp dụng **toàn workspace**
    
- Giống như "system prompt" cho project
    
- **Auto-apply**: Luôn luôn
    

### **E. Agents** (`.windsurf/agents/*.md`)

yaml

---

description: Agent persona

tools: [tool1, tool2]

---

Behavior và capabilities của agent

- **Khi nào dùng**: Cần specialized agent (e.g., "Code Review Agent", "Testing Agent")
    
- **Cách dùng**: Gọi qua `@agent-name` hoặc trong workflow
    

---

## 3. So sánh: Khi nào dùng cái nào?

|Tình huống|Dùng gì|Ví dụ|
|---|---|---|
|Nhắc developer check guidelines|**Workflow**|`/mui-reminder`|
|Tự động refactor khi thấy pattern|**Skill**|Auto convert `div` → `Box`|
|Luật áp dụng mọi lúc|**Rule**|"Always use TypeScript strict mode"|
|Lưu thông tin dự án|**Memory**|"Dùng MUI, không dùng Bootstrap"|
|Task phức tạp cần nhiều steps|**Agent**|"Review this PR thoroughly"|

---

## 4. `reuseMaps` option

tsx

<MapGL reuseMaps ... />

**Ý nghĩa:**

- Khi component unmount/remount (e.g., chuyển tab, conditional render), **giữ lại** Mapbox GL instance thay vì destroy & recreate
    
- Map chỉ được tạo 1 lần, tái sử dụng cho các lần render sau
    

**Lợi ích:**

- ⚡ **Performance**: Không phải tải lại tiles, style, sources
    
- 💾 **Memory**: Tránh leak memory từ việc tạo nhiều map instances
    
- 🔄 **State preservation**: Giữ viewport, layers, markers khi remount
    

**Trade-off:**

- Nếu cần **hoàn toàn fresh map** (khác style, khác token), không nên dùng
    
- Có thể gây issue nếu props thay đổi nhưng map không reset
    

**Khi nào nên dùng:**

- Map ở trong tab/component có thể hide/show
    
- Mobile app với navigation giữa screens
    
- Dashboard có nhiều widget, map không phải lúc nào cũng visible
    

---

**Tóm lại:**

- Workflow = Gõ `/command` thủ công
    
- Skill = Auto-apply khi detect pattern
    
- `reuseMaps` = Tái sử dụng map instance cho performance