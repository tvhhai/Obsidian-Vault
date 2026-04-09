# Multi-Agent Implementation

[[Agentic AI Architecture Với Pattern, Framework & MCP]]

---

## Multi-Agent System Design

### Core Concepts
```
┌─────────────────────────────────────────────────────────┐
│                  Multi-Agent System                        │
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
└─────────────────────────────────────────────────────────┘
```

---

## Implementation with AutoGen

### Basic Multi-Agent Setup
```python
import autogen

# Configuration
config_list = [
    {
        "model": "gpt-4",
        "api_key": "your-api-key"
    }
]

# Create agents
assistant = autogen.AssistantAgent(
    name="assistant",
    llm_config={"config_list": config_list}
)

coder = autogen.AssistantAgent(
    name="coder",
    llm_config={"config_list": config_list},
    system_message="You are a coding expert. Write clean, efficient code."
)

reviewer = autogen.AssistantAgent(
    name="reviewer",
    llm_config={"config_list": config_list},
    system_message="You review code for quality and best practices."
)

user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=10
)

# Group chat
groupchat = autogen.GroupChat(
    agents=[user_proxy, assistant, coder, reviewer],
    messages=[],
    max_round=12
)

manager = autogen.GroupChatManager(
    groupchat=groupchat,
    llm_config={"config_list": config_list}
)

# Start conversation
user_proxy.initiate_chat(
    manager,
    message="Build a Python web scraper with error handling"
)
```

### Sequential Workflow
```python
# Handoff pattern với AutoGen
from autogen import ConversableAgent

researcher = ConversableAgent(
    name="researcher",
    system_message="Research the topic thoroughly.",
    llm_config={"config_list": config_list}
)

writer = ConversableAgent(
    name="writer",
    system_message="Write based on research provided.",
    llm_config={"config_list": config_list}
)

editor = ConversableAgent(
    name="editor",
    system_message="Edit and polish the final output.",
    llm_config={"config_list": config_list}
)

# Sequential handoffs
result = researcher.initiate_chat(
    writer,
    message="Research: benefits of AI in healthcare",
    max_turns=1
)

final = writer.initiate_chat(
    editor,
    message=f"Write article based on: {result.summary}",
    max_turns=1
)
```

---

## Implementation with CrewAI

### Role-Based Multi-Agent
```python
from crewai import Agent, Task, Crew, Process

# Define agents with roles
researcher = Agent(
    role='Senior Research Analyst',
    goal='Uncover cutting-edge developments in AI',
    backstory='Expert in AI research with 10+ years experience',
    verbose=True,
    allow_delegation=True,
    tools=[search_tool, web_scraper]
)

writer = Agent(
    role='Tech Content Writer',
    goal='Craft engaging articles about AI',
    backstory='Professional writer specializing in technology',
    verbose=True,
    allow_delegation=False
)

reviewer = Agent(
    role='Editor',
    goal='Ensure quality and accuracy',
    backstory='Senior editor with technical background',
    verbose=True,
    allow_delegation=False
)

# Define tasks
task1 = Task(
    description='Research latest AI trends in 2024',
    agent=researcher,
    expected_output='Comprehensive report on AI trends'
)

task2 = Task(
    description='Write article based on research',
    agent=writer,
    expected_output='Engaging blog post',
    context=[task1]
)

task3 = Task(
    description='Review and edit the article',
    agent=reviewer,
    expected_output='Polished final article',
    context=[task2]
)

# Create crew
crew = Crew(
    agents=[researcher, writer, reviewer],
    tasks=[task1, task2, task3],
    process=Process.sequential,
    verbose=True
)

# Execute
result = crew.kickoff()
```

### Hierarchical Process
```python
from crewai import Process

# Manager agent điều phối
manager = Agent(
    role='Project Manager',
    goal='Coordinate team to deliver project',
    backstory='Experienced PM with technical expertise',
    allow_delegation=True
)

# Hierarchical execution
crew = Crew(
    agents=[researcher, writer, reviewer],
    tasks=[task1, task2, task3],
    process=Process.hierarchical,
    manager_agent=manager,
    verbose=True
)
```

---

## Implementation with LangGraph

### State Machine Multi-Agent
```python
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
import operator

# State definition
class AgentState(TypedDict):
    messages: Annotated[list, operator.add]
    next_agent: str
    results: dict

# Agent nodes
def researcher_node(state: AgentState):
    result = researcher_agent.invoke(state["messages"])
    return {
        "messages": [result],
        "results": {"research": result.content}
    }

def writer_node(state: AgentState):
    result = writer_agent.invoke(state["messages"])
    return {
        "messages": [result],
        "results": {"draft": result.content}
    }

def reviewer_node(state: AgentState):
    result = reviewer_agent.invoke(state["messages"])
    return {
        "messages": [result],
        "next_agent": "end" if "approved" in result.content else "writer"
    }

# Router function
def router(state: AgentState):
    if state["next_agent"] == "end":
        return END
    return state["next_agent"]

# Build graph
workflow = StateGraph(AgentState)

workflow.add_node("researcher", researcher_node)
workflow.add_node("writer", writer_node)
workflow.add_node("reviewer", reviewer_node)

workflow.set_entry_point("researcher")
workflow.add_edge("researcher", "writer")
workflow.add_edge("writer", "reviewer")
workflow.add_conditional_edges("reviewer", router)

app = workflow.compile()

# Execute
result = app.invoke({
    "messages": ["Write about quantum computing"],
    "next_agent": "",
    "results": {}
})
```

### Parallel Agent Execution
```python
from langgraph.graph import StateGraph, END

class ParallelState(TypedDict):
    topic: str
    research_result: str
    code_result: str
    analysis_result: str
    final_output: str

def research_agent(state: ParallelState):
    # Independent task
    return {"research_result": f"Research on {state['topic']}"}

def code_agent(state: ParallelState):
    # Independent task
    return {"code_result": f"Code for {state['topic']}"}

def analysis_agent(state: ParallelState):
    # Independent task
    return {"analysis_result": f"Analysis of {state['topic']}"}

def aggregator(state: ParallelState):
    # Combine all results
    final = f"""
    Research: {state['research_result']}
    Code: {state['code_result']}
    Analysis: {state['analysis_result']}
    """
    return {"final_output": final}

# Build parallel graph
workflow = StateGraph(ParallelState)

workflow.add_node("research", research_agent)
workflow.add_node("code", code_agent)
workflow.add_node("analysis", analysis_agent)
workflow.add_node("aggregate", aggregator)

# Parallel execution
workflow.set_entry_point("research")
workflow.add_edge("research", "aggregate")

# Multiple entry points for parallel
workflow.add_edge("code", "aggregate")
workflow.add_edge("analysis", "aggregate")

# Or use fan-out pattern
workflow.add_conditional_edges(
    "start",
    lambda _: ["research", "code", "analysis"]
)
```

---

## Custom Multi-Agent Framework

### Message Bus Architecture
```python
from dataclasses import dataclass
from typing import Dict, List, Callable, Any
from enum import Enum
import asyncio

class MessageType(Enum):
    TASK = "task"
    RESULT = "result"
    BROADCAST = "broadcast"
    DIRECT = "direct"

@dataclass
class Message:
    msg_id: str
    sender: str
    recipient: Optional[str]  # None for broadcast
    msg_type: MessageType
    content: Any
    timestamp: float

class MessageBus:
    """Central message broker for agents"""
    
    def __init__(self):
        self.subscribers: Dict[str, List[Callable]] = {}
        self.message_history: List[Message] = []
    
    def subscribe(self, agent_id: str, handler: Callable):
        if agent_id not in self.subscribers:
            self.subscribers[agent_id] = []
        self.subscribers[agent_id].append(handler)
    
    async def publish(self, message: Message):
        self.message_history.append(message)
        
        if message.recipient:
            # Direct message
            if message.recipient in self.subscribers:
                for handler in self.subscribers[message.recipient]:
                    await handler(message)
        else:
            # Broadcast
            for handlers in self.subscribers.values():
                for handler in handlers:
                    await handler(message)

class BaseAgent:
    """Base class for all agents"""
    
    def __init__(self, agent_id: str, bus: MessageBus):
        self.agent_id = agent_id
        self.bus = bus
        self.bus.subscribe(agent_id, self.receive)
    
    async def receive(self, message: Message):
        """Override in subclasses"""
        pass
    
    async def send(self, recipient: Optional[str], content: Any):
        msg = Message(
            msg_id=str(uuid.uuid4()),
            sender=self.agent_id,
            recipient=recipient,
            msg_type=MessageType.DIRECT if recipient else MessageType.BROADCAST,
            content=content,
            timestamp=time.time()
        )
        await self.bus.publish(msg)

class OrchestratorAgent(BaseAgent):
    """Coordinates multiple agents"""
    
    def __init__(self, agent_id: str, bus: MessageBus, workers: List[str]):
        super().__init__(agent_id, bus)
        self.workers = workers
        self.task_queue = asyncio.Queue()
        self.results = {}
    
    async def assign_task(self, task: Dict):
        # Round-robin or intelligent routing
        worker = self.select_worker(task)
        await self.send(worker, {
            "type": "task",
            "data": task
        })
    
    async def receive(self, message: Message):
        if message.content.get("type") == "result":
            self.results[message.msg_id] = message.content
            await self.check_completion()
    
    def select_worker(self, task: Dict) -> str:
        # Intelligent routing logic
        pass
```

---

## Communication Patterns

### 1. Request-Reply
```python
class RequestReplyPattern:
    """Synchronous request-response between agents"""
    
    async def request(self, target_agent: str, request_data: Any) -> Any:
        request_id = str(uuid.uuid4())
        future = asyncio.Future()
        
        self.pending_requests[request_id] = future
        
        await self.bus.publish(Message(
            msg_id=request_id,
            sender=self.agent_id,
            recipient=target_agent,
            msg_type=MessageType.TASK,
            content=request_data,
            timestamp=time.time()
        ))
        
        # Wait for response
        return await asyncio.wait_for(future, timeout=30)
```

### 2. Publish-Subscribe
```python
class PubSubPattern:
    """Event-driven communication"""
    
    def subscribe_to_topic(self, topic: str, handler: Callable):
        if topic not in self.topics:
            self.topics[topic] = []
        self.topics[topic].append(handler)
    
    async def publish_event(self, topic: str, event: Any):
        if topic in self.topics:
            for handler in self.topics[topic]:
                await handler(event)
```

### 3. Blackboard Pattern
```python
class BlackboardPattern:
    """Shared knowledge base for agents"""
    
    def __init__(self):
        self.knowledge: Dict[str, Any] = {}
        self.subscribers: Dict[str, List[Callable]] = {}
    
    def write(self, key: str, value: Any, agent_id: str):
        self.knowledge[key] = {
            "value": value,
            "author": agent_id,
            "timestamp": time.time()
        }
        self.notify_change(key)
    
    def read(self, key: str) -> Any:
        return self.knowledge.get(key, {}).get("value")
```

---

## Best Practices

### 1. Agent Design
```
Single Responsibility Principle
├── Each agent has one primary role
├── Clear input/output contracts
├── Minimal coupling between agents
└── Shared state through message bus only
```

### 2. Error Handling
```python
class RobustAgent(BaseAgent):
    async def execute_with_retry(self, task: Task, max_retries: int = 3):
        for attempt in range(max_retries):
            try:
                return await self.execute(task)
            except Exception as e:
                if attempt == max_retries - 1:
                    await self.escalate(task, e)
                await asyncio.sleep(2 ** attempt)  # Exponential backoff
```

### 3. Observability
```python
class ObservableAgent(BaseAgent):
    async def execute(self, task: Task):
        start_time = time.time()
        
        # Log start
        self.logger.info(f"Agent {self.agent_id} starting task {task.id}")
        
        try:
            result = await self._execute(task)
            
            # Log success
            self.logger.info(
                f"Task completed in {time.time() - start_time:.2f}s"
            )
            return result
            
        except Exception as e:
            # Log failure
            self.logger.error(f"Task failed: {e}")
            raise
```

---

## Resources

- [[Agent Testing & Evaluation]]
- [[Production Agent Deployment]]
- [AutoGen Docs](https://microsoft.github.io/autogen/)
- [CrewAI Docs](https://docs.crewai.com/)
- [LangGraph Docs](https://langchain-ai.github.io/langgraph/)
