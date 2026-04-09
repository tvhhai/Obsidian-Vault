# Production Agent Deployment

[[Agentic AI Architecture Với Pattern, Framework & MCP]]

---

## Production Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Load Balancer                         │
│                   (Nginx / ALB)                        │
└─────────────────────────────────────────────────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        ▼                  ▼                  ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Agent     │    │   Agent     │    │   Agent     │
│   Pod 1     │    │   Pod 2     │    │   Pod N     │
│             │    │             │    │             │
│ ┌─────────┐ │    │ ┌─────────┐ │    │ ┌─────────┐ │
│ │ FastAPI │ │    │ │ FastAPI │ │    │ │ FastAPI │ │
│ │  App    │ │    │ │  App    │ │    │ │  App    │ │
│ └────┬────┘ │    │ └────┬────┘ │    │ └────┬────┘ │
│      │      │    │      │      │    │      │      │
│ ┌────▼────┐ │    │ ┌────▼────┐ │    │ ┌────▼────┐ │
│ │  Agent  │ │    │ │  Agent  │ │    │ │  Agent  │ │
│ │ Engine  │ │    │ │ Engine  │ │    │ │ Engine  │ │
│ └─────────┘ │    │ └─────────┘ │    │ └─────────┘ │
└─────────────┘    └─────────────┘    └─────────────┘
        │                  │                  │
        └──────────────────┼──────────────────┘
                           ▼
┌─────────────────────────────────────────────────────────┐
│                   Redis Cluster                          │
│         (Session Store / Cache / PubSub)                │
└─────────────────────────────────────────────────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        ▼                  ▼                  ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  Vector DB  │    │  OLAP DB    │    │  Message    │
│  (Pinecone) │    │  (ClickHouse)│   │  Queue      │
└─────────────┘    └─────────────┘    │  (RabbitMQ) │
                                      └─────────────┘
```

---

## Deployment Options

### 1. Container Orchestration (Kubernetes)

```yaml
# k8s-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: agent-service
spec:
  replicas: 3
  selector:
    matchLabels:
      app: agent-service
  template:
    metadata:
      labels:
        app: agent-service
    spec:
      containers:
      - name: agent
        image: agent-service:latest
        ports:
        - containerPort: 8000
        env:
        - name: OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: agent-secrets
              key: openai-key
        - name: REDIS_URL
          value: "redis://redis-cluster:6379"
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "2000m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: agent-service
spec:
  selector:
    app: agent-service
  ports:
  - port: 80
    targetPort: 8000
  type: ClusterIP
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: agent-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: agent-service
  minReplicas: 3
  maxReplicas: 20
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

### 2. Serverless (AWS Lambda)

```python
# lambda_handler.py
import json
from agent import Agent

agent = Agent()  # Initialize once for container reuse

def lambda_handler(event, context):
    try:
        body = json.loads(event.get('body', '{}'))
        query = body.get('query')
        
        if not query:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Missing query'})
            }
        
        # Execute with timeout handling
        result = agent.execute(query, timeout=25)
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'response': result.output,
                'tokens_used': result.tokens,
                'cost': result.cost
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
```

```yaml
# serverless.yml
service: agent-service

provider:
  name: aws
  runtime: python3.11
  memorySize: 2048
  timeout: 30
  environment:
    OPENAI_API_KEY: ${env:OPENAI_API_KEY}
    
functions:
  agent:
    handler: lambda_handler.lambda_handler
    events:
      - http:
          path: /agent
          method: post
          cors: true
      
  agent_async:
    handler: lambda_handler.async_handler
    events:
      - sqs: arn:aws:sqs:region:account:agent-queue
```

### 3. Docker Compose (On-Premise)

```yaml
# docker-compose.yml
version: '3.8'

services:
  agent-api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - REDIS_URL=redis://redis:6379
      - POSTGRES_URL=postgresql://postgres:password@db:5432/agent
    depends_on:
      - redis
      - db
      - vector-db
    deploy:
      replicas: 2
      resources:
        limits:
          cpus: '2'
          memory: 4G
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    command: redis-server --appendonly yes

  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=agent
    volumes:
      - postgres_data:/var/lib/postgresql/data

  vector-db:
    image: qdrant/qdrant:latest
    ports:
      - "6333:6333"
    volumes:
      - qdrant_data:/qdrant/storage

  monitoring:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml

volumes:
  redis_data:
  postgres_data:
  qdrant_data:
```

---

## API Implementation

### FastAPI Application
```python
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
import asyncio
import uuid

app = FastAPI(title="Agent Service", version="1.0.0")

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response models
class AgentRequest(BaseModel):
    query: str
    session_id: Optional[str] = None
    context: Optional[Dict[str, Any]] = None
    timeout: Optional[int] = 60

class AgentResponse(BaseModel):
    response: str
    session_id: str
    tokens_used: int
    cost: float
    execution_time: float
    tools_used: list[str]

class AsyncJobResponse(BaseModel):
    job_id: str
    status: str
    estimated_completion: Optional[int] = None

# Health checks
@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.0"}

@app.get("/ready")
async def readiness_check():
    # Check dependencies
    checks = {
        "llm": await check_llm_connection(),
        "redis": await check_redis(),
        "vector_db": await check_vector_db()
    }
    
    all_ready = all(checks.values())
    status_code = 200 if all_ready else 503
    
    return {
        "ready": all_ready,
        "checks": checks
    }

# Sync endpoint
@app.post("/agent/execute", response_model=AgentResponse)
async def execute_agent(request: AgentRequest):
    try:
        session_id = request.session_id or str(uuid.uuid4())
        
        # Load or create session
        session = await session_store.get(session_id)
        
        # Execute agent
        start_time = asyncio.get_event_loop().time()
        result = await agent.execute(
            query=request.query,
            context=request.context,
            session=session,
            timeout=request.timeout
        )
        execution_time = asyncio.get_event_loop().time() - start_time
        
        # Store updated session
        await session_store.save(session_id, result.updated_session)
        
        return AgentResponse(
            response=result.output,
            session_id=session_id,
            tokens_used=result.tokens,
            cost=result.cost,
            execution_time=execution_time,
            tools_used=result.tools_used
        )
        
    except Exception as e:
        logger.error(f"Agent execution failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Async endpoint with job queue
@app.post("/agent/execute/async", response_model=AsyncJobResponse)
async def execute_agent_async(
    request: AgentRequest,
    background_tasks: BackgroundTasks
):
    job_id = str(uuid.uuid4())
    
    # Add to job queue
    await job_queue.add_job(
        job_id=job_id,
        request=request,
        status="queued"
    )
    
    # Process in background
    background_tasks.add_task(process_agent_job, job_id, request)
    
    return AsyncJobResponse(
        job_id=job_id,
        status="queued",
        estimated_completion=30
    )

@app.get("/agent/job/{job_id}")
async def get_job_status(job_id: str):
    job = await job_queue.get_job(job_id)
    
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return {
        "job_id": job_id,
        "status": job.status,
        "result": job.result if job.status == "completed" else None,
        "error": job.error if job.status == "failed" else None
    }

# Streaming endpoint for real-time responses
@app.post("/agent/execute/stream")
async def execute_agent_stream(request: AgentRequest):
    from fastapi.responses import StreamingResponse
    
    async def event_generator():
        async for chunk in agent.execute_stream(request.query):
            yield f"data: {json.dumps({'chunk': chunk})}\n\n"
        yield "data: [DONE]\n\n"
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream"
    )
```

---

## Configuration Management

### Environment-Based Config
```python
from pydantic_settings import BaseSettings
from typing import List, Optional

class Settings(BaseSettings):
    """Production settings"""
    
    # API
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    DEBUG: bool = False
    
    # LLM
    OPENAI_API_KEY: str
    OPENAI_MODEL: str = "gpt-4"
    OPENAI_BASE_URL: Optional[str] = None
    LLM_TIMEOUT: int = 60
    LLM_MAX_RETRIES: int = 3
    
    # Rate Limiting
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_WINDOW: int = 60
    
    # Session
    SESSION_TTL: int = 3600  # 1 hour
    REDIS_URL: str = "redis://localhost:6379"
    
    # Vector DB
    VECTOR_DB_URL: str = "http://localhost:6333"
    VECTOR_DB_API_KEY: Optional[str] = None
    
    # Monitoring
    SENTRY_DSN: Optional[str] = None
    LOG_LEVEL: str = "INFO"
    METRICS_ENABLED: bool = True
    
    # Security
    API_KEY_HEADER: str = "X-API-Key"
    ALLOWED_ORIGINS: List[str] = ["*"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
```

---

## Monitoring & Observability

### Structured Logging
```python
import structlog
import logging

# Configure structlog
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()

# Usage in agent
class MonitoredAgent:
    def execute(self, query: str):
        log = logger.bind(
            session_id=self.session_id,
            query_hash=hash(query),
            agent_version="1.0.0"
        )
        
        log.info("agent_request_started")
        
        try:
            result = self._execute(query)
            log.info(
                "agent_request_completed",
                tokens_used=result.tokens,
                cost=result.cost,
                execution_time=result.duration,
                tools_used=result.tools
            )
            return result
            
        except Exception as e:
            log.error(
                "agent_request_failed",
                error=str(e),
                error_type=type(e).__name__
            )
            raise
```

### Metrics with Prometheus
```python
from prometheus_client import Counter, Histogram, Gauge, Info

# Define metrics
AGENT_REQUESTS = Counter(
    'agent_requests_total',
    'Total agent requests',
    ['status', 'model']
)

AGENT_LATENCY = Histogram(
    'agent_request_duration_seconds',
    'Request latency',
    buckets=[0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 30.0]
)

AGENT_TOKENS = Counter(
    'agent_tokens_total',
    'Total tokens used',
    ['model', 'type']  # type: prompt/completion
)

AGENT_COST = Counter(
    'agent_cost_dollars_total',
    'Total cost in dollars',
    ['model']
)

ACTIVE_SESSIONS = Gauge(
    'agent_active_sessions',
    'Number of active sessions'
)

# Integration
@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start_time = time.time()
    
    response = await call_next(request)
    
    duration = time.time() - start_time
    AGENT_LATENCY.observe(duration)
    
    return response

# Expose metrics endpoint
@app.get("/metrics")
async def metrics():
    from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
    return Response(
        generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )
```

### Distributed Tracing
```python
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.redis import RedisInstrumentor

# Setup tracing
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)

otlp_exporter = OTLPSpanExporter(endpoint="http://jaeger:4317")
span_processor = BatchSpanProcessor(otlp_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

# Instrument FastAPI
FastAPIInstrumentor.instrument_app(app)
RedisInstrumentor().instrument()

# Custom spans in agent
class TracedAgent:
    async def execute(self, query: str):
        with tracer.start_as_current_span("agent_execution") as span:
            span.set_attribute("query.length", len(query))
            span.set_attribute("session.id", self.session_id)
            
            # Tool execution span
            with tracer.start_as_current_span("tool_execution"):
                result = await self.tool.execute(query)
                span.set_attribute("tool.name", self.tool.name)
            
            # LLM call span
            with tracer.start_as_current_span("llm_call"):
                llm_result = await self.llm.generate(query)
                span.set_attribute("llm.tokens", llm_result.tokens)
            
            return result
```

---

## Security

### API Authentication
```python
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException, status

security = HTTPBearer()

async def verify_api_key(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    
    # Verify against database or cache
    is_valid = await api_key_store.verify(token)
    
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key"
        )
    
    # Check rate limits
    usage = await rate_limiter.check_usage(token)
    if usage.exceeded:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded"
        )
    
    return token

# Protect endpoints
@app.post("/agent/execute", dependencies=[Depends(verify_api_key)])
async def execute_agent(request: AgentRequest):
    # ...
```

### Input Sanitization
```python
import bleach
from pydantic import validator

class SafeRequest(BaseModel):
    query: str
    
    @validator('query')
    def sanitize_input(cls, v):
        # Remove potentially harmful content
        v = bleach.clean(v, tags=[], strip=True)
        
        # Check for injection patterns
        injection_patterns = [
            r'(?i)(ignore|override).*(instruction|prompt)',
            r'(?i)(system|developer).*(prompt|message)',
        ]
        
        for pattern in injection_patterns:
            if re.search(pattern, v):
                raise ValueError("Potentially harmful input detected")
        
        return v
```

---

## Resources

- [[MCP Protocol Chi tiết]]
- [[Multi-Agent Implementation]]
- [[Agent Testing & Evaluation]]
- [FastAPI Best Practices](https://fastapi.tiangolo.com/deployment/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Prometheus Monitoring](https://prometheus.io/docs/)
- [OpenTelemetry](https://opentelemetry.io/docs/)
