# Agentic AI Architecture: Pattern, Framework & MCP

---

## Mục Lục
1. [AI Agent là gì?](#1-ai-agent-là-gì)
2. [AI Agent vs. Agentic AI](#2-ai-agent-vs-agentic-ai)
3. [Các Component của AI Agent](#3-các-component-của-ai-agent)
4. [Agentic AI là gì? Kiến trúc Multi-Agent](#4-agentic-ai-là-gì)
5. [Cách thức hoạt động của Agentic AI](#5-cách-thức-hoạt-động-của-agentic-ai)
6. [Agentic Workflow](#6-agentic-workflow)
7. [Agentic Loop: PRAL](#7-agentic-loop-pral)
8. [AI Agent Framework](#8-ai-agent-framework)
9. [AI Agentic Design Patterns](#9-ai-agentic-design-patterns)
10. [Agentic Orchestration Patterns](#10-agentic-orchestration-patterns)
11. [Agentic RAG](#11-agentic-rag)
12. [Agent Communication & Protocol](#12-agent-communication--protocol)
13. [Context Engineering](#13-context-engineering)
14. [Agent Development Lifecycle](#14-agent-development-lifecycle)
15. [E-Shop Agentic Layer](#15-e-shop-agentic-layer)
16. [AI Agent & Generative AI](#16-ai-agent--generative-ai)
17. [Khi nào nên sử dụng AI Agent](#17-khi-nào-nên-sử-dụng-ai-agent)

---

## 1. AI Agent là gì?

### Định nghĩa
**AI Agent** là một hệ thống phần mềm tự chủ có khả năng **perceive** (nhận thức), **reason** (suy luận), **act** (hành động) và **learn** (học hỏi) trong một môi trường cụ thể để đạt được các mục tiêu được định nghĩa trước.

### Đặc điểm cốt lõi
| Đặc điểm | Mô tả |
|----------|-------|
| **Autonomy** | Hoạt động độc lập không cần giám sát liên tục |
| **Reactivity** | Phản hồi kịp thời với thay đổi môi trường |
| **Pro-activeness** | Chủ động theo đuổi mục tiêu |
| **Social Ability** | Tương tác với agents/systems khác |
| **Learning** | Cải thiện hiệu suất qua kinh nghiệm |

### Phân loại AI Agent
```
AI Agents
├── Simple Reflex Agents
├── Model-Based Reflex Agents  
├── Goal-Based Agents
├── Utility-Based Agents
└── Learning Agents (ML/DL-based)
```

---

## 2. AI Agent vs. Agentic AI

### Sự khác biệt then chốt

| Tiêu chí | AI Agent | Agentic AI |
|----------|----------|------------|
| **Scope** | Đơn lẻ, độc lập | Hệ thống nhiều agents phối hợp |
| **Complexity** | Tác vụ cụ thể | Workflow phức tạp, đa bước |
| **Decision Making** | Reactive/Rule-based | Proactive, lập kế hoạch, reasoning |
| **Collaboration** | Ít hoặc không | Multi-agent coordination |
| **Adaptability** | Hạn chế | Cao, tự điều chỉnh |

### So sánh trực quan
```
AI Agent                    Agentic AI
    |                           |
    ▼                           ▼
┌─────────┐              ┌─────────────────┐
│  LLM    │              │  Orchestrator   │
│ + Tools │              │  + Multi-Agent  │
│ + Memory│              │  + Planning     │
└─────────┘              │  + Reasoning    │
   Single                │  + Reflection   │
   Agent                 └─────────────────┘
                              System
```

---

## 3. Các Component của AI Agent

### Kiến trúc tổng quan
```
┌─────────────────────────────────────────────────────────┐
│                    AI Agent Architecture                │
├─────────────────────────────────────────────────────────┤
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐     │
│  │Perception│ | Reasoning│ │  Action │  │ Learning│     │
│  │  Layer  │  │  Engine │  │  Layer  │  │  Engine │     │
│  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘     │
│       └─────────────┴─────────────┴─────────────┘       │
│                         │                               │
│              ┌──────────┴──────────┐                    │
│              │     Memory/Core     │                    │
│              │  ┌───────────────┐  │                    │
│              │  │  Working Mem  │  │                    │
│              │  │  Long-term Mem│  │                    │
│              │  │  Episodic Mem │  │                    │
│              │  └───────────────┘  │                    │
│              └─────────────────────┘                    │
└─────────────────────────────────────────────────────────┘
```

### Chi tiết các Component

#### 3.1 Perception Layer
- **Input Processing**: Nhận dữ liệu từ môi trường (text, image, audio, sensor data)
- **Context Extraction**: Trích xuất thông tin có ý nghĩa
- **State Representation**: Biểu diễn trạng thái hiện tại

#### 3.2 Reasoning Engine
- **LLM Core**: GPT-4, Claude, Llama, etc.
- **Prompt Engineering**: System prompts, few-shot examples
- **Chain of Thought**: Suy luận đa bước

#### 3.3 Action Layer
- **Tool Registry**: Các công cụ có sẵn (API, functions)
- **Action Selection**: Chọn hành động phù hợp
- **Execution**: Thực thi và xử lý kết quả

#### 3.4 Memory System
```python
# Cấu trúc Memory
type Memory = {
  working_memory: Context;      # Ngắn hạn, session hiện tại
  short_term: RecentContext;   # Vài phút/giờ gần đây
  long_term: KnowledgeBase;    # Kiến thức lâu dài
  episodic: PastExperiences;    # Kinh nghiệm cụ thể
}
```

#### 3.5 Learning Engine
- **Feedback Integration**: Học từ kết quả hành động
- **Model Fine-tuning**: Cải thiện reasoning
- **Skill Acquisition**: Học tool usage mới

### Cách xây dựng một AI Agent

```python
from dataclasses import dataclass
from typing import List, Callable, Any

@dataclass
class AIAgent:
    name: str
    llm: Any  # Language Model
    tools: List[Callable]
    memory: MemoryStore
    system_prompt: str
    
    def perceive(self, input_data: Any) -> Perception:
        """Nhận thức môi trường"""
        return self.llm.process_input(input_data)
    
    def reason(self, perception: Perception) -> Plan:
        """Suy luận và lập kế hoạch"""
        context = self.memory.retrieve(perception)
        return self.llm.generate_plan(context, self.system_prompt)
    
    def act(self, plan: Plan) -> ActionResult:
        """Thực thi hành động"""
        for step in plan.steps:
            if step.requires_tool:
                tool = self.get_tool(step.tool_name)
                result = tool(**step.params)
            else:
                result = self.llm.generate(step.prompt)
            self.memory.store(result)
        return ActionResult(success=True)
    
    def learn(self, result: ActionResult, feedback: Feedback):
        """Cập nhật từ phản hồi"""
        self.memory.update_episodic(result, feedback)
        # Optional: fine-tune hoặc update prompts
```

---

## 4. Agentic AI là gì? Kiến trúc Multi-Agent

### Định nghĩa
**Agentic AI** là paradigma AI nơi nhiều AI Agents **phối hợp** với nhau trong một hệ thống để giải quyết các vấn đề phức tạp, có thể tự động lập kế hoạch, reasoning, và thực thi workflows đa bước.

### Kiến trúc Multi-Agent

```
┌─────────────────────────────────────────────────────────┐
│                  Multi-Agent System                      │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐ │
│  │   Agent A   │◄──►│   Agent B   │◄──►│   Agent C   │ │
│  │ (Researcher)│    │  (Planner)  │    │ (Executor)  │ │
│  └──────┬──────┘    └──────┬──────┘    └──────┬──────┘ │
│         │                  │                  │        │
│         └──────────────────┼──────────────────┘        │
│                            │                           │
│                   ┌────────▼────────┐                  │
│                   │  Orchestrator   │                  │
│                   │   / Director    │                  │
│                   └────────┬────────┘                  │
│                            │                           │
│                   ┌────────▼────────┐                  │
│                   │  Shared Memory  │                  │
│                   │   Message Bus   │                  │
│                   └─────────────────┘                  │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### Các kiểu Multi-Agent Architecture

#### 4.1 Hierarchical (Phân cấp)
```
        ┌─────────┐
        │Director │
        └────┬────┘
             │
    ┌────────┼────────┐
    ▼        ▼        ▼
┌───────┐┌───────┐┌───────┐
│Agent 1││Agent 2││Agent 3│
└───────┘└───────┘└───────┘
```
- **Ưu điểm**: Clear chain of command, dễ quản lý
- **Nhược điểm**: Single point of failure

#### 4.2 Flat/Peer-to-Peer
```
    ┌───────┐
    │Agent 1│◄────►┌───────┐
    └───┬───┘      │Agent 2│
        │          └───┬───┘
        ▼              │
    ┌───────┐          ▼
    │Agent 3│◄────►┌───────┐
    └───────┘      │Agent 4│
                   └───────┘
```
- **Ưu điểm**: Flexible, resilient
- **Nhược điểm**: Coordination phức tạp

#### 4.3 Hub-and-Spoke
```
         ┌─────────┐
    ┌───►│Mediator │◄───┐
    │    └────┬────┘    │
    │         │         │
    ▼         ▼         ▼
┌───────┐ ┌───────┐ ┌───────┐
│Agent 1│ │Agent 2│ │Agent 3│
└───────┘ └───────┘ └───────┘
```

---

## 5. Cách thức hoạt động của Agentic AI

### System-Level Architecture

#### 5.1 Orchestration Pattern
```
┌────────────────────────────────────────┐
│          Orchestrator Agent            │
│  ┌────────┐ ┌────────┐ ┌────────┐   │
│  │ Plan   │ │Assign  │ │Monitor │   │
│  │        │ │Task    │ │Progress│   │
│  └────────┘ └────────┘ └────────┘   │
└────────────┬───────────────────────────┘
             │
    ┌────────┼────────┬────────┐
    ▼        ▼        ▼        ▼
┌───────┐┌───────┐┌───────┐┌───────┐
│Task 1 ││Task 2 ││Task 3 ││Task 4 │
└───────┘└───────┘└───────┘└───────┘
```
- **Central Controller**: Một agent điều phối toàn bộ workflow
- **Task Assignment**: Phân chia và gán tasks cho các specialist agents
- **Monitoring**: Theo dõi tiến độ và xử lý lỗi

#### 5.2 Choreography Pattern
```
┌───────┐    Event Bus /    ┌───────┐
│Agent 1│◄───Message Queue──►│Agent 2│
└───────┘                     └───────┘
    ▲                            ▲
    │    ┌───────┐    ┌───────┐   │
    └────►│Agent 3│◄──►│Agent 4│◄──┘
         └───────┘    └───────┘
```
- **Decentralized**: Không có controller trung tâm
- **Event-Driven**: Agents phản hồi events từ message bus
- **Flexible**: Dễ dàng thêm/bớt agents

### Workflow Execution Models

| Model | Mô tả | Use Case |
|-------|-------|----------|
| **Sequential** | Tasks thực thi tuần tự | Data pipeline |
| **Parallel** | Tasks chạy đồng thời | Independent tasks |
| **Conditional** | Branching logic | Decision trees |
| **Iterative** | Lặp cho đến khi đạt yêu cầu | Refinement tasks |

---

## 6. Agentic Workflow

### Định nghĩa
**Agentic Workflow** là quy trình làm việc tự động nơi AI Agents thực hiện chuỗi các hành động, quyết định, và phối hợp để hoàn thành một mục tiêu phức tạp.

### Ví dụ: Customer Support Workflow
```
┌─────────┐   ┌──────────┐   ┌─────────┐   ┌──────────┐
│  Intent │──►│ Knowledge│──►│ Solution│──►│ Response│
│  Classifier  │   │  Search  │   │ Generator   │   │ Formatter│
└─────────┘   └──────────┘   └─────────┘   └──────────┘
     │             │             │             │
     ▼             ▼             ▼             ▼
┌─────────────────────────────────────────────────────┐
│  Escalation Agent (nếu confidence < threshold)      │
└─────────────────────────────────────────────────────┘
```

### Components của Agentic Workflow
1. **Triggers**: Điều kiện khởi động workflow
2. **Stages**: Các giai đoạn xử lý
3. **Agents**: Thực thể thực hiện tasks
4. **Transitions**: Luồng chuyển tiếp giữa stages
5. **Conditions**: Logic branching
6. **Termination**: Điều kiện kết thúc

---

## 7. Agentic Loop: PRAL

### Định nghĩa
**PRAL Loop** (Perception, Reasoning, Action, Learning) là chu trình cốt lõi của autonomous agents.

```
        ┌─────────────┐
        │  Perception │
        │  (Nhận thức)│
        └──────┬──────┘
               │
               ▼
        ┌─────────────┐
        │  Reasoning  │◄──────┐
        │  (Suy luận) │       │
        └──────┬──────┘       │
               │              │
               ▼              │
        ┌─────────────┐       │
        │    Action   │       │
        │  (Hành động)│       │
        └──────┬──────┘       │
               │              │
               ▼              │
        ┌─────────────┐       │
        │   Learning  │──────┘
        │  (Học hỏi)  │
        └─────────────┘
```

### Chi tiết từng giai đoạn

#### 7.1 Perception (Nhận thức)
- **Input Collection**: Thu thập dữ liệu từ môi trường
- **Feature Extraction**: Trích xuất đặc trưng quan trọng
- **Context Building**: Xây dựng ngữ cảnh hiện tại

#### 7.2 Reasoning (Suy luận)
- **Goal Analysis**: Phân tích mục tiêu
- **Planning**: Lập kế hoạch hành động
- **Prediction**: Dự đoán kết quả

#### 7.3 Action (Hành động)
- **Tool Selection**: Chọn công cụ phù hợp
- **Execution**: Thực thi hành động
- **Observation**: Quan sát kết quả

#### 7.4 Learning (Học hỏi)
- **Outcome Evaluation**: Đánh giá kết quả
- **Memory Update**: Cập nhật kinh nghiệm
- **Strategy Refinement**: Cải thiện chiến lược

---

## 8. AI Agent Framework

### Các Framework phổ biến

#### 8.1 LangChain
```python
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_openai import ChatOpenAI
from langchain.tools import tool

@tool
def search(query: str) -> str:
    """Search tool"""
    return f"Results for: {query}"

llm = ChatOpenAI(model="gpt-4")
tools = [search]
agent = create_openai_tools_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools)
```

#### 8.2 LangGraph
- **State Machines**: Workflow dạng graph
- **Persistence**: Lưu trạng thái giữa các runs
- **Streaming**: Real-time updates

#### 8.3 AutoGen (Microsoft)
```python
import autogen

assistant = autogen.AssistantAgent(
    name="assistant",
    llm_config={"config_list": config_list}
)

user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="NEVER"
)

user_proxy.initiate_chat(
    assistant, 
    message="Tìm thông tin về AI Agents"
)
```

#### 8.4 CrewAI
```python
from crewai import Agent, Task, Crew

researcher = Agent(
    role='Researcher',
    goal='Tìm kiếm thông tin',
    backstory='Chuyên gia nghiên cứu',
    tools=[search_tool]
)

task = Task(
    description='Nghiên cứu chủ đề X',
    agent=researcher
)

crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, write_task]
)
```

#### 8.5 LlamaIndex
- **RAG-focused**: Retrieval-Augmented Generation
- **Data Connectors**: 100+ data sources
- **Query Engines**: Complex question answering

#### 8.6 Semantic Kernel (Microsoft)
- **Planners**: Automatic task decomposition
- **Plugins**: Modular skill system
- **Memory**: Long-term context

### So sánh Framework

| Framework | Strengths | Best For |
|-----------|-----------|----------|
| **LangChain** | Ecosystem, flexibility | General purpose |
| **LangGraph** | Complex workflows, persistence | Stateful apps |
| **AutoGen** | Multi-agent conversation | Collaborative tasks |
| **CrewAI** | Role-based, simple API | Team simulations |
| **LlamaIndex** | Data integration, RAG | Knowledge bases |
| **Semantic Kernel** | Enterprise, planners | Business apps |

---

## 9. AI Agentic Design Patterns

### Tổng quan các Pattern
```
Agentic Design Patterns
├── Single Agent Patterns
│   ├── Tool Use
│   ├── Planning
│   ├── Reflection
│   └── ReAct
└── Multi-Agent Patterns
    ├── Router & Specialist
    ├── Handoff
    ├── Group Chat / Debate
    └── Swarm
```

---

## 10. "Tool Use" Pattern

### Định nghĩa
Agent có khả năng **gọi external functions/tools** để mở rộng capabilities vượt ra ngoài kiến thức base của LLM.

### Cấu trúc
```python
class ToolUsePattern:
    """
    ┌─────────────────┐
    │   User Query    │
    └────────┬────────┘
             ▼
    ┌─────────────────┐
    │   LLM decides   │
    │   if tool needed│
    └────────┬────────┘
             │
    ┌────────┴────────┐
    ▼                 ▼
┌─────────┐    ┌─────────────┐
│Direct   │    │ Select Tool │
│Response │    │ + Parameters│
└─────────┘    └──────┬──────┘
                      ▼
              ┌───────────────┐
              │ Execute Tool  │
              └───────┬───────┘
                      ▼
              ┌───────────────┐
              │  LLM with     │
              │  Tool Result    │
              └───────────────┘
    """
    
    def __init__(self, llm, tools: List[Tool]):
        self.llm = llm
        self.tools = {t.name: t for t in tools}
    
    def execute(self, query: str) -> str:
        # Step 1: LLM phân tích query
        analysis = self.llm.analyze(query, available_tools=self.tools)
        
        # Step 2: Nếu cần tool
        if analysis.requires_tool:
            tool = self.tools[analysis.tool_name]
            result = tool.execute(**analysis.parameters)
            
            # Step 3: LLM tổng hợp với kết quả tool
            return self.llm.synthesize(query, result)
        
        return self.llm.generate(query)
```

### Tool Definition Example
```python
@tool
def calculator(expression: str) -> float:
    """Evaluate mathematical expression"""
    return eval(expression)

@tool
def search_database(query: str, table: str) -> List[Dict]:
    """Search database table"""
    return db.query(f"SELECT * FROM {table} WHERE {query}")

@tool
def send_email(to: str, subject: str, body: str) -> bool:
    """Send email to recipient"""
    return email_service.send(to, subject, body)
```

---

## 11. "Planning" Pattern

### Định nghĩa
Agent **phân rã task phức tạp** thành chuỗi các sub-tasks có thể quản lý được.

### Cấu trúc
```python
class PlanningPattern:
    """
    ┌─────────────────┐
    │  Complex Task   │
    │  "Book a trip"  │
    └────────┬────────┘
             ▼
    ┌─────────────────┐
    │  Task Breakdown │
    │  (Planning LLM) │
    └────────┬────────┘
             ▼
    ┌─────────────────┐
    │  Sub-task List  │
    │  1. Search flights
    │  2. Compare prices  
    │  3. Book hotel
    │  4. Confirm booking
    └────────┬────────┘
             ▼
    ┌─────────────────┐
    │  Sequential     │
    │  Execution      │
    └─────────────────┘
    """
    
    def plan(self, task: str) -> Plan:
        """Generate step-by-step plan"""
        prompt = f"""
        Break down this task into specific steps:
        Task: {task}
        
        For each step, specify:
        - Action description
        - Required tools (if any)
        - Dependencies on previous steps
        - Success criteria
        """
        return self.llm.generate_plan(prompt)
    
    def execute_plan(self, plan: Plan) -> Result:
        """Execute plan with monitoring"""
        results = []
        for step in plan.steps:
            # Execute step
            result = self.execute_step(step)
            results.append(result)
            
            # Validate result
            if not self.validate(step, result):
                # Re-plan if needed
                plan = self.replan(plan, step, result)
        
        return self.synthesize(results)
```

### Planning Strategies

| Strategy | Mô tả | Use Case |
|----------|-------|----------|
| **Hierarchical** | Task → Sub-tasks → Actions | Complex projects |
| **Conditional** | Plan with if-then branches | Uncertain environments |
| **Iterative** | Plan → Execute → Refine | Creative tasks |
| **Multi-agent** | Different agents for sub-tasks | Specialized domains |

---

## 12. "Reflection" Pattern (Metacognition)

### Định nghĩa
Agent **tự đánh giá** output của chính mình để cải thiện chất lượng trước khi hoàn thành.

### Cấu trúc
```python
class ReflectionPattern:
    """
    ┌─────────────────┐
    │  Initial Output │
    │  (Generation)   │
    └────────┬────────┘
             ▼
    ┌─────────────────┐
    │   Reflection    │
    │  (Self-Critique)│
    └────────┬────────┘
             │
    ┌────────┴────────┐
    ▼                 ▼
┌─────────┐    ┌─────────────┐
│ Pass    │    │  Identify   │
│ Quality │    │  Issues     │
│ Check   │    │             │
└────┬────┘    └──────┬──────┘
     │                 │
     ▼                 ▼
┌─────────┐    ┌─────────────┐
│ Return  │    │  Refinement │
│ Output  │    │  (Revision) │
└─────────┘    └──────┬──────┘
                      │
            (Loop back to Reflection)
    """
    
    def generate_with_reflection(self, prompt: str, max_iterations: int = 3) -> str:
        output = self.llm.generate(prompt)
        
        for _ in range(max_iterations):
            # Self-critique
            critique = self.reflect(output, prompt)
            
            if critique.is_satisfactory:
                break
            
            # Refine based on critique
            output = self.refine(output, critique.feedback)
        
        return output
    
    def reflect(self, output: str, original_prompt: str) -> Critique:
        reflection_prompt = f"""
        Review this output:
        {output}
        
        Original request: {original_prompt}
        
        Evaluate:
        1. Accuracy - Is information correct?
        2. Completeness - Are all aspects covered?
        3. Clarity - Is it easy to understand?
        4. Relevance - Does it address the request?
        
        If issues found, specify what needs improvement.
        """
        return self.llm.generate_critique(reflection_prompt)
```

### Reflection Types
1. **Self-Correction**: Detect và sửa lỗi factual
2. **Style Improvement**: Cải thiện tone, clarity
3. **Consistency Check**: Đảm bảo tính nhất quán
4. **Completeness Verification**: Kiểm tra độ đầy đủ

---

## 13. "ReAct" Compound Pattern

### Định nghĩa
**ReAct** (Reasoning + Acting) là pattern kết hợp **suy luận** (reasoning) và **hành động** (acting) trong một chuỗi thought-action-thought.

### Cấu trúc
```python
class ReActPattern:
    """
    Thought → Action → Observation → Thought → ...
    
    ┌───────────┐
    │  Thought  │ "I need to find the population of Paris"
    └─────┬─────┘
          ▼
    ┌───────────┐
    │   Action  │ search("population of Paris")
    └─────┬─────┘
          ▼
    ┌───────────┐
    │Observation│ "Population: 2.16 million (2023)"
    └─────┬─────┘
          ▼
    ┌───────────┐
    │  Thought  │ "Now I can answer the question"
    └─────┬─────┘
          ▼
    ┌───────────┐
    │   Answer  │ "The population of Paris is 2.16 million"
    └───────────┘
    """
    
    def react_loop(self, query: str, max_steps: int = 10) -> str:
        context = f"Question: {query}\n"
        
        for step in range(max_steps):
            # Thought
            thought = self.llm.generate(f"{context}\nThought:")
            context += f"Thought: {thought}\n"
            
            # Check if can answer
            if self.is_final_answer(thought):
                return self.extract_answer(thought)
            
            # Action
            action = self.parse_action(thought)
            context += f"Action: {action}\n"
            
            # Execute
            observation = self.execute_action(action)
            context += f"Observation: {observation}\n"
        
        return "Max steps reached"
```

### ReAct Prompt Example
```
You are an AI assistant. Solve the problem by alternating between Thought and Action.

Thought: Analyze what you need to do
Action: Take one of [search, calculate, lookup, answer]
Observation: Result of the action
(Followed by next Thought)

Question: What is the current weather in London and should I bring an umbrella?
Thought: I need to check the current weather in London
Action: search("current weather London")
Observation: Cloudy with 60% chance of rain, 18°C
Thought: There's a good chance of rain, so I should recommend bringing an umbrella
Action: answer("Yes, bring an umbrella. There's a 60% chance of rain in London today.")
```

---

## 14. "Router & Specialist" Pattern

### Định nghĩa
Một **Router Agent** phân loại requests và chuyển tiếp đến **Specialist Agents** phù hợp.

### Cấu trúc
```python
class RouterSpecialistPattern:
    """
         ┌─────────┐
         │  Query  │
         └────┬────┘
              ▼
    ┌─────────────────┐
    │  Router Agent   │
    │  (Classification)│
    │                 │
    │  ┌───────────┐  │
    │  │ Intent    │  │ ──► ┌─────────────┐
    │  │ Detection │  │     │ Billing     │
    │  └───────────┘  │     │ Specialist  │
    │  ┌───────────┐  │     └─────────────┘
    │  │ Domain    │  │ ──► ┌─────────────┐
    │  │ Routing   │  │     │ Technical   │
    │  └───────────┘  │     │ Specialist  │
    └─────────────────┘     └─────────────┘
              │             ┌─────────────┐
              └────────────►│ Sales       │
                            │ Specialist  │
                            └─────────────┘
    """
    
    def __init__(self):
        self.router = RouterAgent()
        self.specialists = {
            "billing": BillingAgent(),
            "technical": TechnicalAgent(),
            "sales": SalesAgent(),
            "general": GeneralAgent()
        }
    
    def route(self, query: str) -> Response:
        # Route quyết định specialist phù hợp
        category = self.router.classify(query)
        
        # Chuyển đến specialist
        specialist = self.specialists.get(category, self.specialists["general"])
        
        # Specialist xử lý
        return specialist.handle(query)
```

### Routing Strategies

| Strategy | Mô tả |
|----------|-------|
| **Intent Classification** | Phân loại theo ý định người dùng |
| **Domain Routing** | Chuyển theo lĩnh vực chuyên môn |
| **Load Balancing** | Phân phối đều giữa specialists |
| **Skill Matching** | So khớp kỹ năng với yêu cầu |

---

## 15. "Handoff" Pattern (Sequential Workflow)

### Định nghĩa
Chuyển giao trách nhiệm từ agent này sang agent khác theo chuỗi tuần tự.

### Cấu trúc
```python
class HandoffPattern:
    """
    ┌─────────┐   Handoff   ┌─────────┐   Handoff   ┌─────────┐
    │ Agent 1 │────────────►│ Agent 2 │────────────►│ Agent 3 │
    │(Intake) │   (context) │ (Process)│  (context) │(Finalize)│
    └─────────┘             └─────────┘             └─────────┘
         │                      │                      │
         ▼                      ▼                      ▼
    ┌─────────┐            ┌─────────┐            ┌─────────┐
    │Collect  │            │Analyze  │            │Deliver  │
    │Info     │            │& Process│            │Result   │
    └─────────┘            └─────────┘            └─────────┘
    """
    
    def execute_handoff_chain(self, initial_input: Any) -> Result:
        # Khởi tạo context
        context = {"input": initial_input, "history": []}
        
        # Agent 1: Intake
        result1 = self.intake_agent.process(context)
        context["history"].append({"agent": "intake", "result": result1})
        context["intake_result"] = result1
        
        # Handoff to Agent 2
        result2 = self.process_agent.process(context)
        context["history"].append({"agent": "process", "result": result2})
        context["process_result"] = result2
        
        # Handoff to Agent 3
        result3 = self.finalize_agent.process(context)
        
        return result3
```

### Context Passing
```python
@dataclass
class HandoffContext:
    """Thông tin chuyển giao giữa agents"""
    original_query: str
    accumulated_results: Dict[str, Any]
    intermediate_outputs: List[Any]
    metadata: Dict[str, Any]
    priority: int
    deadline: Optional[datetime]
```

---

## 16. "Group Chat / Debate" Pattern

### Định nghĩa
Nhiều agents **thảo luận** với nhau để đạt được consensus hoặc tổng hợp quan điểm.

### Cấu trúc
```python
class GroupChatPattern:
    """
         ┌─────────┐
         │ Facilitator│
         │  Agent    │
         └────┬────┘
              │
    ┌─────────┼─────────┐
    ▼         ▼         ▼
┌───────┐ ┌───────┐ ┌───────┐
│Agent 1│ │Agent 2│ │Agent 3│
│  (Pro)│ │(Con)  │ │(Neutral)│
└───┬───┘ └───┬───┘ └───┬───┘
    │         │         │
    └─────────┼─────────┘
              │
    ┌─────────┴─────────┐
    ▼                   ▼
┌───────┐         ┌───────┐
│Discuss│◄───────►│Discuss│
└───────┘         └───────┘
    │
    ▼
┌───────┐
│Consensus│
│  Vote  │
└───────┘
    """
    
    def debate(self, topic: str, agents: List[Agent], rounds: int = 3) -> Consensus:
        discussion_history = []
        
        for round_num in range(rounds):
            round_responses = []
            
            for agent in agents:
                # Agent phản hồi dựa trên history
                response = agent.respond(topic, discussion_history)
                round_responses.append({
                    "agent": agent.name,
                    "stance": agent.stance,
                    "response": response
                })
            
            discussion_history.append({
                "round": round_num,
                "responses": round_responses
            })
        
        # Facilitator tổng hợp
        return self.facilitator.synthesize_consensus(discussion_history)
```

### Use Cases
- **Policy Debate**: Thảo luận chính sách với nhiều perspectives
- **Design Review**: Đánh giá thiết kế từ nhiều angles
- **Creative Brainstorming**: Tạo ý tưởng qua tương tác
- **Fact Verification**: Xác minh thông tin qua cross-reference

---

## 17. "Swarm" Pattern (Parallelization)

### Định nghĩa
Nhiều agents **thực thi song song** trên cùng một task hoặc phần khác nhau của task.

### Cấu trúc
```python
class SwarmPattern:
    """
         ┌─────────┐
         │  Task   │
         └────┬────┘
              │
    ┌─────────┼─────────┐
    ▼         ▼         ▼
┌───────┐ ┌───────┐ ┌───────┐
│Agent 1│ │Agent 2│ │Agent 3│
│(Chunk1)│ │(Chunk2)│ │(Chunk3)│
└───┬───┘ └───┬───┘ └───┬───┘
    │         │         │
    └─────────┼─────────┘
              ▼
    ┌─────────────────┐
    │    Aggregator   │
    │  (Reduce/Merge) │
    └────────┬────────┘
             ▼
    ┌─────────────────┐
    │   Final Result  │
    └─────────────────┘
    """
    
    async def execute_swarm(self, task: Task, num_agents: int = 5) -> Result:
        # Chia task thành sub-tasks
        sub_tasks = self.split_task(task, num_agents)
        
        # Chạy song song
        tasks = [
            self.create_agent(i).execute(sub_task)
            for i, sub_task in enumerate(sub_tasks)
        ]
        
        results = await asyncio.gather(*tasks)
        
        # Tổng hợp kết quả
        return self.aggregator.merge(results)
```

### Swarm Strategies

| Strategy | Mô tả | Use Case |
|----------|-------|----------|
| **Divide & Conquer** | Chia task thành phần nhỏ | Large document processing |
| **Voting** | Nhiều agents vote kết quả | Accuracy-critical tasks |
| **Ensemble** | Kết hợp outputs khác nhau | Creative generation |
| **Competitive** | Chọn best result | Optimization tasks |

---

## 18. "Human-in-the-Loop" (HITL) Pattern

### Định nghĩa
Tích hợp **sự can thiệp của con người** vào workflow của agent.

### Cấu trúc
```python
class HumanInTheLoopPattern:
    """
    ┌─────────┐
    │  Agent  │
    │ Execute │
    └────┬────┘
         │
         ▼
    ┌─────────┐  Yes   ┌─────────┐
    │ Need Human?│────►│ Request │
    └────┬────┘       │ Approval│
         │ No         └────┬────┘
         │                 │
         ▼                 ▼
    ┌─────────┐      ┌─────────────┐
    │ Continue│      │ Human       │
    │ Autonomous    │ Decision    │
    └─────────┘      └──────┬──────┘
                            │
                   ┌────────┴────────┐
                   ▼                 ▼
              ┌─────────┐      ┌─────────┐
              │ Approve │      │ Reject/ │
              │         │      │ Modify  │
              └────┬────┘      └────┬────┘
                   │                │
                   ▼                ▼
              ┌─────────┐      ┌─────────┐
              │ Continue│      │  Agent  │
              │         │      │ Retry   │
              └─────────┘      └─────────┘
    """
    
    def execute_with_hitl(self, task: Task) -> Result:
        while not task.is_complete():
            # Agent thực thi
            result = self.agent.step(task)
            
            # Kiểm tra cần human input
            if self.requires_human_approval(result):
                human_input = self.request_human_input(
                    context=result,
                    options=["approve", "reject", "modify"]
                )
                
                if human_input.decision == "reject":
                    task.add_feedback(human_input.feedback)
                    continue
                elif human_input.decision == "modify":
                    result = human_input.modified_result
            
            task.update(result)
        
        return task.final_result()
```

### HITL Trigger Conditions
```python
trigger_conditions = {
    "high_risk": lambda result: result.risk_score > 0.8,
    "high_value": lambda result: result.financial_impact > 10000,
    "low_confidence": lambda result: result.confidence < 0.6,
    "novel_situation": lambda result: result.novelty_score > 0.9,
    "compliance_required": lambda result: result.requires_audit,
}
```

---

## 19. Agentic Orchestration Patterns

### 19.1 Sequential
```
A ──► B ──► C ──► D
```
Tasks thực thi tuần tự, output của A là input của B.

### 19.2 Concurrent (Parallel)
```
    ┌─► B ─┐
A ──┼─► C ─┼──► E
    └─► D ─┘
```
B, C, D chạy song song, E chờ tất cả hoàn thành.

### 19.3 Group Chat
```
    ┌───┐
A ──┤   ├── B
    │ G │
C ──┤   ├── D
    └───┘
```
Agents A, B, C, D thảo luận trong group G.

### 19.4 Handoff
```
A ──► B (A chuyển giao cho B)
```
Chuyển quyền điều khiển hoàn toàn.

### 19.5 Magentic-One (Microsoft)
```
    ┌─────────────────────┐
    │     Orchestrator    │
    │  (Planning & Tracking)│
    └──────────┬──────────┘
               │
    ┌──────────┼──────────┐
    ▼          ▼          ▼
┌───────┐  ┌───────┐  ┌───────┐
│WebSurfer│  │FileSurfer│ │Coder   │
└───────┘  └───────┘  └───────┘
```

---

## 20. Agentic RAG

### Định nghĩa
**Agentic RAG** mở rộng RAG (Retrieval-Augmented Generation) với **reasoning agents** có thể đưa ra quyết định retrieval thông minh.

### Cấu trúc
```python
class AgenticRAG:
    """
    ┌─────────────────┐
    │  User Query     │
    └────────┬────────┘
             ▼
    ┌─────────────────┐
    │  Query Analysis │
    │  Agent          │
    │                 │
    │  - Decompose?   │
    │  - Direct RAG?  │
    │  - Web Search?  │
    └────────┬────────┘
             │
    ┌────────┴────────┐
    ▼                 ▼
┌─────────┐     ┌─────────────┐
│Simple   │     │ Complex     │
│Query    │     │ Query       │
└────┬────┘     └──────┬──────┘
     │                  │
     ▼                  ▼
┌─────────┐     ┌─────────────┐
│Vector DB│     │ Multi-Step  │
│Search   │     │ Retrieval   │
│         │     │ Strategy    │
└────┬────┘     └──────┬──────┘
     │                  │
     └────────┬─────────┘
              ▼
    ┌─────────────────┐
    │  Synthesize     │
    │  & Generate     │
    └─────────────────┘
    """
    
    def process(self, query: str) -> str:
        # Step 1: Analyze query complexity
        analysis = self.analyze_query(query)
        
        if analysis.is_simple:
            # Simple: Direct vector search
            docs = self.vector_store.search(query)
            return self.llm.generate(query, context=docs)
        
        # Complex: Multi-step retrieval
        retrieval_plan = self.create_retrieval_plan(analysis)
        
        retrieved_docs = []
        for step in retrieval_plan.steps:
            if step.type == "vector_search":
                docs = self.vector_store.search(step.query)
            elif step.type == "web_search":
                docs = self.web_search(step.query)
            elif step.type == "sql_query":
                docs = self.database.query(step.query)
            
            retrieved_docs.extend(docs)
            
            # Re-plan nếu cần
            if self.needs_more_info(docs, step):
                retrieval_plan = self.adjust_plan(retrieval_plan, docs)
        
        return self.synthesize(query, retrieved_docs)
```

### Agentic RAG vs Traditional RAG

| Aspect | Traditional RAG | Agentic RAG |
|--------|----------------|-------------|
| **Query Processing** | Direct embedding | Intelligent analysis |
| **Retrieval** | Single-step | Multi-hop, adaptive |
| **Source Selection** | Fixed | Dynamic routing |
| **Reasoning** | Post-retrieval only | Throughout process |
| **Self-Correction** | None | Re-plan, re-retrieve |

---

## 21. Agent Communication & Protocol

### Các Protocol chính

#### 21.1 MCP (Model Context Protocol)
```
┌─────────────┐         ┌─────────────┐
│   Client    │◄───────►│   Server    │
│  (AI Agent) │  MCP    │  (Tool/Resource│
└─────────────┘ Protocol │  Provider)   │
                       └─────────────┘
```
- **Purpose**: Standardized tool/resource context sharing
- **Transport**: stdio, SSE, HTTP
- **Features**: Tools, Resources, Prompts, Sampling

#### 21.2 A2A (Agent-to-Agent Protocol - Google)
```
┌─────────────┐         ┌─────────────┐
│   Agent A   │◄───────►│   Agent B   │
│  (Client)   │   A2A   │  (Remote)   │
└─────────────┘ Protocol └─────────────┘
```
- **Purpose**: Direct agent communication
- **Format**: JSON-RPC + HTTP
- **Capabilities**: Task delegation, status updates

#### 21.3 ACP (Agent Communication Protocol)
- **Purpose**: Enterprise-grade agent coordination
- **Features**: Security, governance, audit

### Comparison

| Protocol | Scope | Use Case | Status |
|----------|-------|----------|--------|
| **MCP** | Tool/Resource access | Universal tool integration | Open standard |
| **A2A** | Agent-to-agent | Multi-agent collaboration | Google proposal |
| **ACP** | Enterprise | Secure B2B agent comms | Emerging |

---

## 22. Model Context Protocol (MCP) trong Action Design

### MCP Architecture
```
┌─────────────────────────────────────────────────────────┐
│                      MCP Host                            │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐                 │
│  │Client 1 │  │Client 2 │  │Client 3 │                 │
│  └────┬────┘  └────┬────┘  └────┬────┘                 │
│       └─────────────┴─────────────┘                    │
│                    │                                     │
│              MCP Protocol Layer                          │
│                    │                                     │
│       ┌─────────────┼─────────────┐                     │
│       ▼             ▼             ▼                     │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐                │
│  │Server 1 │  │Server 2 │  │Server 3 │                │
│  │ (Files) │  │ (DB)    │  │ (APIs)  │                │
│  └─────────┘  └─────────┘  └─────────┘                │
└─────────────────────────────────────────────────────────┘
```

### MCP trong Action Design

```python
from mcp import ClientSession, StdioServerParameters

class MCPActionDesigner:
    """Sử dụng MCP để thiết kế actions"""
    
    def __init__(self):
        self.mcp_session = None
        self.available_tools = {}
    
    async def connect_to_server(self, server_params: StdioServerParameters):
        """Kết nối đến MCP server"""
        self.mcp_session = await ClientSession.create(server_params)
        
        # Khám phá available tools
        tools = await self.mcp_session.list_tools()
        for tool in tools:
            self.available_tools[tool.name] = tool
    
    async def design_action(self, intent: str) -> Action:
        """Thiết kế action dựa trên intent"""
        
        # 1. Chọn tools phù hợp từ MCP registry
        relevant_tools = self.select_tools(intent)
        
        # 2. Tạo action plan
        action = Action(
            intent=intent,
            steps=[
                ActionStep(
                    tool=tool,
                    parameters=self.infer_parameters(intent, tool)
                )
                for tool in relevant_tools
            ]
        )
        
        return action
    
    async def execute_action(self, action: Action) -> Result:
        """Thực thi action qua MCP"""
        results = []
        
        for step in action.steps:
            # Gọi tool qua MCP
            result = await self.mcp_session.call_tool(
                step.tool.name,
                step.parameters
            )
            results.append(result)
        
        return self.aggregate_results(results)
```

### MCP Server Types
- **FileSystem Server**: Access local/remote files
- **Database Server**: SQL/NoSQL query access
- **API Server**: REST/GraphQL integration
- **Browser Server**: Web automation
- **Custom Servers**: Domain-specific tools

---

## 23. Context Engineering cho AI Agent

### Định nghĩa
**Context Engineering** là nghệ thuật thiết kế và quản lý context để tối ưu hóa hiệu suất agent.

### Context Components
```python
@dataclass
class AgentContext:
    """Đầy đủ context cho agent"""
    
    # System context
    system_prompt: str
    available_tools: List[Tool]
    constraints: List[Constraint]
    
    # Session context  
    conversation_history: List[Message]
    current_state: Dict[str, Any]
    
    # Domain context
    knowledge_base: KnowledgeBase
    relevant_documents: List[Document]
    
    # Runtime context
    user_preferences: Dict[str, Any]
    environmental_factors: Dict[str, Any]
```

### Context Engineering Techniques

#### 23.1 Context Compression
```python
def compress_context(messages: List[Message], max_tokens: int) -> List[Message]:
    """Nén context để fit trong token limit"""
    
    # 1. Summarize older messages
    if len(messages) > 10:
        older = messages[:-10]
        recent = messages[-10:]
        
        summary = llm.summarize(older)
        return [Message(role="system", content=summary)] + recent
    
    # 2. Remove redundant information
    messages = remove_duplicates(messages)
    
    # 3. Semantic pruning
    messages = keep_relevant(messages, current_query)
    
    return messages
```

#### 23.2 Dynamic Context Injection
```python
def inject_relevant_context(query: str, knowledge_base: KnowledgeBase) -> str:
    """Inject relevant context based on query"""
    
    # Retrieve relevant documents
    docs = knowledge_base.similarity_search(query, k=5)
    
    # Format context
    context_str = "\n\n".join([
        f"Document {i+1}:\n{doc.content}"
        for i, doc in enumerate(docs)
    ])
    
    return f"""
    Relevant context:
    {context_str}
    
    User query: {query}
    """
```

#### 23.3 Structured Context Format
```
[SYSTEM PROMPT]
You are an expert assistant. You have access to these tools: {tools}

[GLOBAL CONTEXT]
User: {user_profile}
Session ID: {session_id}
Current Time: {timestamp}

[WORKING MEMORY]
{recent_conversation}

[RETRIEVED KNOWLEDGE]
{relevant_docs}

[CURRENT TASK]
{user_input}
```

---

## 24. Agent Development Lifecycle (ADLC)

### Vòng đời phát triển Agent

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Design    │───►│ Development │───►│   Testing   │
│             │    │             │    │             │
│ • Requirements    │ • Prompt      │    │ • Unit tests│
│ • Architecture    │   engineering │    │ • Integration│
│ • Agent roles     │ • Tool dev    │    │ • Evaluation│
└─────────────┘    └─────────────┘    └──────┬──────┘
      ▲                                       │
      │                                       ▼
┌─────┴───────┐                         ┌─────────────┐
│  Monitoring │                         │ Deployment  │
│  & Improvement                        │             │
│             │                         │ • Staging   │
│ • Metrics   │                         │ • Production│
│ • Feedback  │                         │ • Scaling   │
│ • Iteration │                         └─────────────┘
└─────────────┘
```

### Enterprise Agent Development

#### 24.1 Requirements Phase
```
┌─────────────────────────────────────┐
│ 1. Business Requirements              │
│    - Use case identification          │
│    - ROI analysis                     │
│    - Risk assessment                  │
├─────────────────────────────────────┤
│ 2. Technical Requirements             │
│    - Model selection                  │
│    - Infrastructure needs             │
│    - Integration points               │
├─────────────────────────────────────┤
│ 3. Compliance Requirements            │
│    - Data privacy                     │
│    - Audit trails                     │
│    - Human oversight                  │
└─────────────────────────────────────┘
```

#### 24.2 Architecture Patterns cho Enterprise
```
┌─────────────────────────────────────────────────────────┐
│              Enterprise Agent Platform                   │
├─────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │   Agent     │  │   Agent     │  │   Agent     │     │
│  │   Layer     │  │   Layer     │  │   Layer     │     │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘     │
│         └─────────────────┴─────────────────┘          │
│                    │                                     │
│         ┌──────────┴──────────┐                         │
│         │   Orchestration     │                         │
│         │   Engine            │                         │
│         └──────────┬──────────┘                         │
│                    │                                     │
│  ┌─────────────────┼─────────────────┐                │
│  ▼                 ▼                 ▼                │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐                │
│  │  LLM    │  │  Tools  │  │  Memory │                │
│  │ Gateway │  │ Registry│  │  Store  │                │
│  └─────────┘  └─────────┘  └─────────┘                │
│                                                         │
│  ┌─────────────────────────────────────────┐           │
│  │     Governance & Monitoring Layer       │           │
│  │  - Access Control  - Audit Logs          │           │
│  │  - Rate Limiting   - Cost Tracking       │           │
│  └─────────────────────────────────────────┘           │
└─────────────────────────────────────────────────────────┘
```

### Testing Strategies

| Test Type | Purpose | Tools |
|-----------|---------|-------|
| **Unit** | Test individual components | pytest, jest |
| **Integration** | Agent-tool interaction | custom fixtures |
| **End-to-End** | Full workflow testing | Playwright |
| **Evaluation** | LLM output quality | LLM-as-judge, metrics |
| **Safety** | Harmful output detection | Guardrails, eval datasets |

---

## 25. Xây dựng E-Shop Agentic Layer

### Kiến trúc E-Shop với Agents

```
┌─────────────────────────────────────────────────────────┐
│              E-Commerce Agentic System                     │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌─────────────────────────────────────────────────────┐ │
│  │            Customer-Facing Layer                    │ │
│  │  ┌───────────┐ ┌───────────┐ ┌───────────┐          │ │
│  │  │ Shopping  │ │ Support   │ │Recommend │          │ │
│  │  │ Assistant │ │   Agent   │ │   Agent  │          │ │
│  │  └───────────┘ └───────────┘ └───────────┘          │ │
│  └─────────────────────────────────────────────────────┘ │
│                         │                                │
│  ┌──────────────────────┼─────────────────────────────┐ │
│  │         Orchestration Layer (Router)              │ │
│  └──────────────────────┼─────────────────────────────┘ │
│                         │                                │
│  ┌─────────────────────────────────────────────────────┐ │
│  │            Backend Service Layer                    │ │
│  │  ┌───────────┐ ┌───────────┐ ┌───────────┐          │ │
│  │  │ Inventory │ │  Pricing  │ │  Order    │          │ │
│  │  │   Agent   │ │   Agent   │ │  Agent    │          │ │
│  │  └───────────┘ └───────────┘ └───────────┘          │ │
│  └─────────────────────────────────────────────────────┘ │
│                         │                                │
│  ┌─────────────────────────────────────────────────────┐ │
│  │            Integration Layer                        │ │
│  │  ┌───────────┐ ┌───────────┐ ┌───────────┐          │ │
│  │  │  ERP      │ │  CRM      │ │ Payment   │         │ │
│  │  │Connector │ │Connector │ │ Gateway   │         │ │
│  │  └───────────┘ └───────────┘ └───────────┘          │ │
│  └─────────────────────────────────────────────────────┘ │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### Use Cases

#### 25.1 Shopping Assistant
```python
class ShoppingAssistant:
    """Agent hỗ trợ mua sắm"""
    
    def assist(self, customer_query: str) -> Response:
        # 1. Intent classification
        intent = self.classify_intent(customer_query)
        
        if intent == "product_search":
            return self.handle_product_search(customer_query)
        elif intent == "comparison":
            return self.handle_comparison(customer_query)
        elif intent == "recommendation":
            return self.handle_recommendation(customer_query)
        elif intent == "order_status":
            return self.handoff_to_order_agent(customer_query)
    
    def handle_product_search(self, query: str) -> ProductList:
        # RAG từ product catalog
        products = self.product_retriever.search(query)
        
        # Personalize dựa trên user history
        if self.user_profile:
            products = self.personalizer.rank(products, self.user_profile)
        
        return ProductList(products=products, explanation=self.generate_explanation())
```

#### 25.2 Dynamic Pricing Agent
```python
class PricingAgent:
    """Agent điều chỉnh giá động"""
    
    def adjust_prices(self):
        # Collect market data
        competitor_prices = self.scrape_competitors()
        inventory_levels = self.get_inventory()
        demand_signals = self.analyze_demand()
        
        # Pricing strategy
        for product in self.products:
            optimal_price = self.optimize_price(
                product=product,
                competitors=competitor_prices,
                inventory=inventory_levels,
                demand=demand_signals
            )
            
            if self.validate_price_change(product, optimal_price):
                self.update_price(product, optimal_price)
```

---

## 26. AI Agent sử dụng Generative AI

### Tích hợp GenAI vào Agents

```
┌─────────────────────────────────────────────────────────┐
│           Generative AI in Agent Systems                 │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌─────────────────────────────────────────────────────┐│
│  │           Foundation Models                           ││
│  │  ┌───────────┐ ┌───────────┐ ┌───────────┐          ││
│  │  │   Text    │ │  Vision   │ │  Audio    │          ││
│  │  │  (LLM)    │ │  (VLM)    │ │  (TTS/STT)│          ││
│  │  └─────┬─────┘ └─────┬─────┘ └─────┬─────┘          ││
│  └────────┼─────────────┼─────────────┼────────────────┘│
│           │             │             │                  │
│  ┌────────┴─────────────┴─────────────┴────────────────┐│
│  │              Agent Capabilities                      ││
│  │                                                    ││
│  │  ┌───────────┐  ┌───────────┐  ┌───────────┐     ││
│  │  │ Content   │  │ Code      │  │ Analysis  │     ││
│  │  │ Generation│  │ Generation│  │ & Synthesis     ││
│  │  └───────────┘  └───────────┘  └───────────┘     ││
│  │                                                    ││
│  │  ┌───────────┐  ┌───────────┐  ┌───────────┐     ││
│  │  │ Reasoning │  │ Planning  │  │ Summarization    ││
│  │  │ & Logic   │  │ & Strategy│  │             │     ││
│  │  └───────────┘  └───────────┘  └───────────┘     ││
│  └─────────────────────────────────────────────────────┘│
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### GenAI Use Cases trong Agents

| Capability | Application | Example |
|------------|-------------|---------|
| **Text Generation** | Response crafting | Customer service replies |
| **Code Generation** | Tool creation | Dynamic API clients |
| **Image Analysis** | Visual understanding | Product identification |
| **Summarization** | Information condensation | Meeting notes |
| **Translation** | Multi-language support | Global customer service |
| **Personalization** | Tailored content | Marketing emails |

### Implementation Pattern
```python
class GenAIAgent:
    """Agent sử dụng Generative AI"""
    
    def __init__(self):
        self.text_model = ChatOpenAI(model="gpt-4")
        self.vision_model = ChatOpenAI(model="gpt-4-vision")
        self.code_model = ChatOpenAI(model="gpt-4-code")
    
    def multimodal_understand(self, text: str, image: Image) -> Understanding:
        """Hiểu cả text và image"""
        return self.vision_model.invoke([
            SystemMessage("Analyze the image and text together"),
            HumanMessage(content=[
                {"type": "text", "text": text},
                {"type": "image_url", "image_url": image.url}
            ])
        ])
    
    def generate_tool(self, description: str) -> Callable:
        """Generate custom tool từ description"""
        code = self.code_model.invoke(f"""
        Write a Python function that: {description}
        Include docstring and type hints.
        """)
        return self.compile_tool(code)
```

---

## 27. Khi nào nên sử dụng AI Agent (và khi nào không nên)

### Nên sử dụng khi:

#### ✅ Complex Multi-Step Tasks
- Workflow có nhiều bước dependencies
- Cần reasoning và planning
- Cần tích hợp nhiều data sources

#### ✅ Dynamic Environments
- Context thay đổi liên tục
- Cần adapt và learn
- Rule-based không đủ linh hoạt

#### ✅ Collaboration Needs
- Multi-domain expertise required
- Cần phối hợp giữa teams/functions
- Consensus building cần thiết

#### ✅ Autonomous Operation
- 24/7 operation requirement
- Scale beyond human capacity
- Real-time response needs

### KHÔNG nên sử dụng khi:

#### ❌ Simple, Deterministic Tasks
- Rule-based đủ hiệu quả
- Clear if-then logic
- High precision required

#### ❌ High-Stakes Decisions
- Legal/liability concerns
- Life-critical applications
- Regulatory strict requirements

#### ❌ Limited Training Data
- Domain quá mới/niche
- Data quality issues
- Edge cases không rõ ràng

#### ❌ Budget Constraints
- Compute costs cao
- Maintenance overhead
- ROI không rõ ràng

### Decision Framework
```
┌─────────────────────────────────────────────────────────┐
│              AI Agent Decision Tree                      │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌─────────┐                                            │
│  │ Task phức│──Yes──► ┌─────────┐                       │
│  │ tạp?    │          │ Cần     │──Yes──► USE AGENT    │
│  └────┬────┘          │ reason  │                       │
│       │ No            │ ing?    │──No───► Simple Tool  │
│       ▼               └────┬────┘                       │
│  ┌─────────┐               │ No                          │
│  │ Rule    │◄─────────────┘                             │
│  │ based   │                                            │
│  │ đủ?    │──Yes──► Use Rules/Script                   │
│  └────┬────┘                                            │
│       │ No                                              │
│       ▼                                                 │
│  ┌─────────┐                                            │
│  │ High    │──Yes──► Human-in-the-Loop                 │
│  │ stakes? │                                            │
│  └────┬────┘                                            │
│       │ No                                              │
│       ▼                                                 │
│  USE AGENT với monitoring                               │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

---

## Tài liệu tham khảo

- [LangChain Documentation](https://python.langchain.com/)
- [AutoGen (Microsoft)](https://github.com/microsoft/autogen)
- [CrewAI](https://docs.crewai.com/)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [A2A Protocol (Google)](https://github.com/google/A2A)
- [Anthropic: Building Effective Agents](https://www.anthropic.com/research/building-effective-agents)
- [ReAct Paper](https://arxiv.org/abs/2210.03629)

---

## Related Notes
- [[MCP Protocol Chi tiết]]
- [[Multi-Agent Implementation]]
- [[Agent Testing & Evaluation]]
- [[Production Agent Deployment]]
