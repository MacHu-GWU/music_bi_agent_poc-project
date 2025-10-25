# Music BI Agent - Product Design Document

## Executive Summary

Music BI Agent is an intelligent multi-agent system designed to answer business intelligence questions about the music industry market. The system demonstrates advanced agent orchestration patterns by routing natural language queries to specialized agents, aggregating their results, and generating comprehensive analytical reports.

**Primary Use Case:** Enable business stakeholders to ask complex questions about music market trends, sales performance, and industry dynamics in natural language and receive data-driven insights combining historical metrics, detailed transactional data, and industry knowledge.

**Example Query:** *"How is Rock music performing compared to last quarter? What factors might explain the trend?"*

## Problem Statement

Traditional business intelligence tools require users to:
- Know specific query syntax (SQL, visualization tools)
- Understand data schema and location
- Manually correlate information from multiple sources
- Interpret raw data without contextual industry knowledge

Business stakeholders need a system that can:
- Accept natural language questions
- Intelligently route queries to appropriate data sources
- Combine quantitative data with qualitative insights
- Provide actionable recommendations with complete reasoning trace

## System Architecture

### Architecture Pattern: Agent-as-Tool

The system implements a hierarchical multi-agent architecture where specialized agents act as tools for higher-level orchestration agents. This pattern provides clear separation of concerns while enabling sophisticated workflow composition.

```
User Query
    ↓
[Routing Agent] ──→ Analyzes intent and determines required tools
    ↓
    ├──→ [Metrics Agent] ──→ Historical KPI data (JSON store)
    ├──→ [SQL Agent] ──→ Transactional data (Chinook SQLite)
    └──→ [Knowledge Agent] ──→ Industry insights (RAG/S3 Vector)
    ↓
[Report Generation Agent] ──→ Aggregates results and generates answer
    ↓
Final Answer + Execution Trace
```

### Core Agents

#### 1. Routing Agent (Intent Classification & Orchestration)

**Responsibility:** Analyze user queries and determine which specialized agents to invoke.

**Capabilities:**
- Intent classification into categories:
  - `metrics_lookup`: Queries about KPIs, trends, growth rates
  - `data_analysis`: Questions requiring detailed transactional data
  - `knowledge_inquiry`: Questions about industry context, best practices
  - `comprehensive`: Complex queries requiring multiple data sources
- Tool selection logic
- Parallel or sequential agent invocation planning

**Example Decisions:**
- *"What was Q3 revenue?"* → Metrics Agent only
- *"Which artist sold the most albums?"* → SQL Agent only
- *"Why is Metal genre growing?"* → All three agents
- *"Should we discount Rock albums?"* → SQL + Knowledge agents

**Implementation:** Uses Anthropic's Claude Sonnet 4 with structured output for intent classification.

#### 2. Metrics Agent (Historical KPI Access)

**Responsibility:** Retrieve pre-aggregated business metrics and KPIs.

**Data Source:** In-memory JSON store containing quarterly aggregated metrics:
```json
{
  "revenue": {
    "2024_q3": 125000,
    "2024_q2": 118000,
    "trend": "growing"
  },
  "top_genre_revenue": {
    "2024_q3": {"Rock": 45000, "Metal": 28000, "Jazz": 22000}
  },
  "avg_track_price": {"2024_q3": 1.05},
  "sales_growth_rate": {"2024_q3": 0.059}
}
```

**Tool Interface:**
```python
def query_metrics(metric_name: str, time_period: str) -> dict:
    """
    Query aggregated business metrics.
    
    Args:
        metric_name: revenue, growth_rate, top_genre_revenue, etc.
        time_period: 2024_q3, 2024_q2, etc.
    
    Returns:
        Dict containing metric value and metadata
    """
```

**Use Cases:**
- Dashboard-style questions
- Trend analysis
- Performance comparisons
- Quick factual lookups

#### 3. SQL Agent (Transactional Data Analysis)

**Responsibility:** Execute analytical queries against detailed transactional data.

**Data Source:** Chinook SQLite database containing:
- `Invoice` and `InvoiceLine`: Sales transactions
- `Track`, `Album`, `Artist`: Music catalog
- `Genre`: Music categories
- `Customer`: Customer information

**Technology:** MCP (Model Context Protocol) with `mcp_ohmy_sql` library for SQL execution.

**Tool Interface:**
```python
def query_sales_data(natural_language_query: str) -> dict:
    """
    Execute analytical SQL queries based on natural language.
    
    The agent translates NL to SQL, executes against Chinook DB,
    and returns structured results.
    
    Args:
        natural_language_query: "Which artist has highest sales?"
    
    Returns:
        Query results with metadata
    """
```

**Capabilities:**
- Artist/album sales rankings
- Genre performance drill-downs
- Customer behavior analysis
- Price sensitivity analysis
- Geographic sales patterns

#### 4. Knowledge Agent (Industry Insights via RAG)

**Responsibility:** Retrieve relevant industry knowledge, trends, and best practices.

**Data Source:** Document collection stored in AWS S3 with vector embeddings:
- `music_industry_trends_2024.md`: Market dynamics and forecasts
- `genre_popularity_analysis.md`: Genre-specific characteristics
- `pricing_strategy_guide.md`: Pricing recommendations and elasticity
- `seasonal_sales_patterns.md`: Cyclical trends and explanations

**Technology:** 
- AWS S3 for document storage
- `s3vectorm` library for vector similarity search
- Embeddings: Amazon Titan or OpenAI embeddings

**Tool Interface:**
```python
def search_knowledge(query: str, top_k: int = 3) -> List[Document]:
    """
    Semantic search over industry knowledge base.
    
    Args:
        query: Natural language search query
        top_k: Number of relevant documents to return
    
    Returns:
        List of relevant document chunks with similarity scores
    """
```

**Knowledge Coverage:**
- Industry benchmarks and standards
- Seasonal patterns and explanations
- Genre-specific market characteristics
- Pricing psychology and strategies
- Competitive landscape insights

#### 5. Report Generation Agent (Result Aggregation & Synthesis)

**Responsibility:** Synthesize outputs from specialized agents into coherent, actionable reports.

**Capabilities:**
- Multi-source data aggregation
- Inference and reasoning (e.g., "Is performance above/below expectations?")
- Confidence assessment
- Feedback loop triggering (request additional data if needed)
- Execution trace generation

**Inference Examples:**
- Detect anomalies: "Revenue dropped 15% - is this within seasonal norms?"
- Assess confidence: "Only metrics available, missing transaction details"
- Compare sources: "Metrics show growth, but SQL shows fewer transactions - investigate"

**Output Format:**
```markdown
## [Question]

### Key Findings
[Bullet points with main insights]

### Detailed Analysis
[Prose combining all data sources]

### Recommendations
[Actionable next steps]

---
**Execution Trace:**
- Intent: [comprehensive]
- Agents Called: [Metrics, SQL, Knowledge]
- Confidence: [High/Medium/Low]
- Feedback Loops: [None/Requested additional data]
```

## Workflow Orchestration

### Node Composition

The system implements a 4-node workflow:

1. **Understand Node** (Routing Agent)
   - Input: Raw user query
   - Process: Intent classification, tool selection
   - Output: Execution plan with agent list

2. **Fetch Node** (Specialized Agents - Parallel Execution)
   - Input: Execution plan
   - Process: Invoke Metrics/SQL/Knowledge agents
   - Output: Raw results from each agent

3. **Aggregate Node** (Report Generation Agent - Part 1)
   - Input: Raw results from all agents
   - Process: Combine data, detect inconsistencies
   - Output: Merged dataset + confidence score

4. **Answer Node** (Report Generation Agent - Part 2)
   - Input: Merged dataset + confidence
   - Process: Inference, formatting, trace generation
   - Output: Final answer with execution trace

### Feedback Loop Mechanism

**Trigger Conditions:**
- Low confidence score (< 0.7)
- Missing critical data
- Contradictory results from different sources
- Ambiguous user query

**Feedback Actions:**

**Option A: Re-query with refined parameters**
```python
# Example: Initial query returned sparse results
if confidence < 0.7:
    # Expand time range
    additional_data = metrics_agent.query(
        metric="revenue",
        time_period="2024_q1:2024_q3"  # Broader range
    )
```

**Option B: Query alternative agent**
```python
# Example: Metrics show anomaly, need transaction details
if detect_anomaly(metrics_result):
    drill_down = sql_agent.query(
        "Show daily sales breakdown for Rock genre in Q3"
    )
```

**Option C: Request user clarification**
```python
# Example: Ambiguous query
if intent_confidence < 0.5:
    return {
        "status": "needs_clarification",
        "question": "Are you asking about revenue or unit sales?",
        "options": ["Total revenue", "Number of tracks sold"]
    }
```

## Technology Stack

### Core Framework
- **Anthropic Strands**: Primary agent framework for workflow orchestration
- **Claude Sonnet 4**: LLM for all agent reasoning and natural language processing

### Data Layer
- **Chinook SQLite**: Transactional database (pre-populated with music sales data)
- **JSON Store**: In-memory metrics repository
- **AWS S3**: Document storage for knowledge base

### Specialized Libraries
- **mcp_ohmy_sql**: SQL query execution via Model Context Protocol
- **s3vectorm**: Vector similarity search over S3-stored documents
- **boto3**: AWS S3 integration

### Development Tools
- **Python 3.11+**: Primary language
- **pytest**: Testing framework
- **FastAPI** (optional): REST API wrapper for production deployment

## Data Schema

### Metrics Store Schema
```json
{
  "revenue": {
    "<period>": <float>,
    "trend": "growing|stable|declining"
  },
  "sales_growth_rate": {
    "<period>": <float>
  },
  "top_genre_revenue": {
    "<period>": {
      "<genre>": <float>
    }
  },
  "avg_track_price": {
    "<period>": <float>
  },
  "top_artists": {
    "<period>": [
      {"name": str, "revenue": float, "tracks_sold": int}
    ]
  }
}
```

### Chinook Database (Relevant Tables)
```sql
-- Core sales data
Invoice(InvoiceId, CustomerId, InvoiceDate, Total)
InvoiceLine(InvoiceLineId, InvoiceId, TrackId, Quantity, UnitPrice)

-- Catalog
Track(TrackId, Name, AlbumId, GenreId, Milliseconds, UnitPrice)
Album(AlbumId, Title, ArtistId)
Artist(ArtistId, Name)
Genre(GenreId, Name)

-- Customers
Customer(CustomerId, FirstName, LastName, Country, Email)
```

### Knowledge Base Document Structure
```markdown
# [Document Title]

## Overview
[High-level summary]

## Key Insights
- [Bullet point findings]

## Data Points
- [Specific metrics and benchmarks]

## Recommendations
- [Actionable guidance]

## Sources
[Citations if applicable]
```

## Example User Journeys

### Journey 1: Simple Metrics Query

**User Query:** *"What was our Q3 revenue?"*

**System Flow:**
1. Routing Agent classifies intent: `metrics_lookup`
2. Invokes Metrics Agent only
3. Metrics Agent queries JSON store: `revenue.2024_q3`
4. Report Generation Agent formats simple answer
5. Returns: "$125,000 in Q3 2024"

**Execution Trace:**
```
Intent: metrics_lookup
Agents: [Metrics]
Confidence: High
Duration: 0.8s
```

### Journey 2: Analytical Deep Dive

**User Query:** *"Why is Metal music revenue growing faster than other genres?"*

**System Flow:**
1. Routing Agent classifies: `comprehensive` (requires all agents)
2. **Parallel Fetch:**
   - Metrics Agent: Metal revenue trend (Q1→Q3)
   - SQL Agent: Metal transaction details (avg price, customer segments)
   - Knowledge Agent: "Metal genre market characteristics"
3. **Aggregation:**
   - Metrics show 12% growth
   - SQL reveals higher average price ($1.35 vs $1.05 overall)
   - Knowledge explains: "Metal fans exhibit high loyalty, premium willingness"
4. **Inference:**
   - Confidence: High (all data sources agree)
   - Pattern: Premium pricing + loyal fanbase = revenue growth
5. **Report Generation:**
   - Synthesizes findings
   - Provides genre-specific recommendations

**Output:**
```markdown
## Metal Genre Revenue Growth Analysis

### Key Findings
- Q3 Metal revenue: $28,000 (+12% vs Q2)
- Average track price: $1.35 (29% premium vs overall avg)
- Customer repeat rate: 68% (vs 45% overall)

### Analysis
Metal genre demonstrates "small but valuable" market characteristics.
Revenue growth driven by:

1. **Premium Pricing Power**: Fans willing to pay 29% more per track
2. **High Customer Loyalty**: 68% repeat purchase rate indicates 
   strong engagement
3. **Album Bundle Sales**: 45% of Metal sales are full albums vs 
   28% overall

According to industry research, Metal represents a mature niche with
stable demand and low price sensitivity - ideal for premium positioning.

### Recommendations
✅ Maintain premium pricing strategy
✅ Focus on complete album releases
✅ Develop exclusive content for existing fans
❌ Avoid mass-market discount promotions

---
**Execution Trace:**
- Intent: comprehensive
- Agents: [Metrics, SQL, Knowledge]
- Queries: 3 parallel
- Confidence: High (cross-validated)
- Duration: 2.3s
```

### Journey 3: Feedback Loop Activation

**User Query:** *"Should we change our pricing strategy?"*

**System Flow:**
1. Routing Agent detects ambiguous query (low confidence: 0.4)
2. **Feedback Loop Triggered → Request Clarification:**
   ```
   "I can help with pricing analysis. Could you clarify:
   - Are you asking about overall pricing or specific genres?
   - Considering increase, decrease, or dynamic pricing?
   
   Or would you like a general pricing strategy review?"
   ```
3. **User Clarifies:** *"General review across all genres"*
4. **Re-route with Clear Intent:**
   - SQL Agent: Current price distribution by genre
   - Metrics Agent: Revenue elasticity data
   - Knowledge Agent: "Pricing strategy best practices"
5. Generate comprehensive pricing analysis report

**Execution Trace:**
```
Intent: knowledge_inquiry (initial: ambiguous)
Feedback Loop: Clarification requested
Follow-up Intent: comprehensive
Agents: [SQL, Metrics, Knowledge]
Confidence: High (after clarification)
Duration: 3.1s (including user interaction)
```

## Implementation Phases

### Phase 1: Foundation (Week 1)
- Set up Chinook SQLite database
- Create metrics JSON store with sample data
- Prepare knowledge base documents
- Configure AWS S3 and vector embeddings

### Phase 2: Core Agents (Week 1-2)
- Implement Metrics Agent with JSON query tool
- Implement SQL Agent with mcp_ohmy_sql integration
- Implement Knowledge Agent with s3vectorm RAG
- Unit tests for each agent

### Phase 3: Orchestration (Week 2)
- Build Routing Agent with intent classification
- Build Report Generation Agent with aggregation logic
- Implement feedback loop mechanisms
- Integration tests

### Phase 4: Polish & Documentation (Week 2-3)
- Execution trace formatting
- Error handling and edge cases
- Performance optimization
- Comprehensive documentation and examples

## Success Metrics

### Functional Metrics
- **Intent Classification Accuracy**: >90% on test queries
- **Query Success Rate**: >95% for well-formed questions
- **Multi-Agent Coordination**: 100% successful aggregation

### Performance Metrics
- **Simple Query Latency**: <2 seconds (single agent)
- **Complex Query Latency**: <5 seconds (all agents)
- **Feedback Loop Response**: <1 second (clarification prompt)

### Quality Metrics
- **Answer Completeness**: All questions answered with data + context
- **Trace Clarity**: 100% of answers include readable execution trace
- **Recommendation Accuracy**: Validated against industry best practices

## Design Decisions & Rationale

### Why Agent-as-Tool Pattern?
- **Modularity**: Each agent can be developed, tested, and improved independently
- **Reusability**: Agents can be composed into different workflows
- **Scalability**: Easy to add new specialized agents (e.g., Competitor Analysis Agent)
- **Clear Interfaces**: Well-defined input/output contracts

### Why Not LangChain/LangGraph?
- **Strands Framework Advantages:**
  - Native integration with Anthropic Claude models
  - Simpler agent composition patterns
  - Better control over prompt engineering
  - Lower dependency overhead
- **Interview Context:** Demonstrates architectural decision-making and framework evaluation skills

### Why Three Data Sources?
- **Metrics (JSON)**: Fast access to pre-computed KPIs - mirrors real-world data warehouses
- **SQL (Chinook)**: Demonstrates ability to query relational data - essential for most enterprises
- **Knowledge (RAG)**: Shows understanding of unstructured data and semantic search - increasingly critical for AI systems

### Feedback Loop Design Choices
**Automated Re-querying** (preferred for):
- Missing data that's likely available from another agent
- Anomalies requiring drill-down

**User Clarification** (preferred for):
- Ambiguous intent
- Multiple valid interpretations
- Subjective questions requiring user preferences

## Risk Mitigation

### Technical Risks
| Risk | Mitigation |
|------|-----------|
| SQLite query performance | Index critical columns; limit result sets |
| RAG retrieval quality | Curate high-quality documents; tune embedding models |
| Agent coordination failures | Comprehensive error handling; graceful degradation |
| Token cost escalation | Cache common queries; optimize prompts |

### Data Quality Risks
| Risk | Mitigation |
|------|-----------|
| Metrics store inconsistency | Validation scripts; automated tests |
| Chinook DB schema changes | Version pinning; schema migration plan |
| Knowledge base outdated | Regular content review cycle |

## Future Enhancements

### Short-term (Post-Demo)
1. **Streaming Responses**: Real-time agent progress updates
2. **Conversation Memory**: Multi-turn dialogues with context retention
3. **Export Capabilities**: PDF/Excel report generation
4. **API Wrapper**: REST API for programmatic access

### Long-term (Production Evolution)
1. **Real-time Metrics**: Connect to live data warehouses (Snowflake, BigQuery)
2. **Additional Agents**: Competitor Analysis, Customer Sentiment, Forecasting
3. **Human-in-the-Loop**: Approval workflows for high-stakes decisions
4. **A/B Testing**: Compare agent routing strategies
5. **Multi-tenancy**: Support multiple music companies with isolated data

## Conclusion

Music BI Agent demonstrates a production-ready multi-agent architecture that addresses the core requirements of intent-driven query routing, multi-source data aggregation, intelligent inference, and feedback loop mechanisms. By grounding the system in a realistic business intelligence use case with the familiar Chinook database, it provides both technical depth and practical applicability.

The agent-as-tool pattern with Strands framework showcases modern AI system design principles while maintaining simplicity and clarity - essential qualities for both demonstration and production deployment.

---

**Document Version:** 1.0  
**Last Updated:** 2025-10-25  
**Author:** Sanhe Hu  
**Status:** Ready for Implementation