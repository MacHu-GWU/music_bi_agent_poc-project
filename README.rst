
.. image:: https://readthedocs.org/projects/music-bi-agent-poc/badge/?version=latest
    :target: https://music-bi-agent-poc.readthedocs.io/en/latest/
    :alt: Documentation Status

.. image:: https://github.com/MacHu-GWU/music_bi_agent_poc-project/actions/workflows/main.yml/badge.svg
    :target: https://github.com/MacHu-GWU/music_bi_agent_poc-project/actions?query=workflow:CI

.. image:: https://codecov.io/gh/MacHu-GWU/music_bi_agent_poc-project/branch/main/graph/badge.svg
    :target: https://codecov.io/gh/MacHu-GWU/music_bi_agent_poc-project

.. image:: https://img.shields.io/pypi/v/music-bi-agent-poc.svg
    :target: https://pypi.python.org/pypi/music-bi-agent-poc

.. image:: https://img.shields.io/pypi/l/music-bi-agent-poc.svg
    :target: https://pypi.python.org/pypi/music-bi-agent-poc

.. image:: https://img.shields.io/pypi/pyversions/music-bi-agent-poc.svg
    :target: https://pypi.python.org/pypi/music-bi-agent-poc

.. image:: https://img.shields.io/badge/✍️_Release_History!--None.svg?style=social&logo=github
    :target: https://github.com/MacHu-GWU/music_bi_agent_poc-project/blob/main/release-history.rst

.. image:: https://img.shields.io/badge/⭐_Star_me_on_GitHub!--None.svg?style=social&logo=github
    :target: https://github.com/MacHu-GWU/music_bi_agent_poc-project

------

.. image:: https://img.shields.io/badge/Link-API-blue.svg
    :target: https://music-bi-agent-poc.readthedocs.io/en/latest/py-modindex.html

.. image:: https://img.shields.io/badge/Link-Install-blue.svg
    :target: `install`_

.. image:: https://img.shields.io/badge/Link-GitHub-blue.svg
    :target: https://github.com/MacHu-GWU/music_bi_agent_poc-project

.. image:: https://img.shields.io/badge/Link-Submit_Issue-blue.svg
    :target: https://github.com/MacHu-GWU/music_bi_agent_poc-project/issues

.. image:: https://img.shields.io/badge/Link-Request_Feature-blue.svg
    :target: https://github.com/MacHu-GWU/music_bi_agent_poc-project/issues

.. image:: https://img.shields.io/badge/Link-Download-blue.svg
    :target: https://pypi.org/pypi/music-bi-agent-poc#files


Music BI Agent - Intelligent Multi-Agent Business Intelligence System
==============================================================================
.. image:: https://music-bi-agent-poc.readthedocs.io/en/latest/_static/music_bi_agent_poc-logo.png
    :target: https://music-bi-agent-poc.readthedocs.io/en/latest/

**Music BI Agent** is an intelligent multi-agent system that answers business intelligence questions about the music industry using natural language. Built with the Anthropic Strands framework and Claude Sonnet 4, it demonstrates advanced agent orchestration patterns by routing queries to specialized agents and synthesizing comprehensive analytical reports.


Overview
------------------------------------------------------------------------------

Traditional business intelligence tools require users to know SQL syntax, understand data schemas, and manually correlate information from multiple sources. Music BI Agent solves this by providing a conversational interface that:

- Accepts natural language questions about music industry data
- Intelligently routes queries to specialized agents (SQL, Knowledge Base, Metrics)
- Combines quantitative data with qualitative insights
- Generates comprehensive, well-formatted analytical reports

**Example Query**: *"Which artist has the highest sales? Show me the SQL statement and results."*

**System Response**: Executes SQL against the Chinook database, formats results in a markdown table, and provides analysis with proper context.


Key Features
------------------------------------------------------------------------------

Multi-Agent Architecture (Agent-as-Tool Pattern)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The system implements a hierarchical architecture where specialized agents act as tools for higher-level orchestration:

.. code-block::

    User Query
        ↓
    [Router Agent] → Analyzes intent and delegates
        ↓
        ├──→ [SQL Agent] → Chinook SQLite database queries
        ├──→ [Knowledge Agent] → RAG-based documentation search
        └──→ [Metrics Agent] → Pre-aggregated KPIs (future)
        ↓
    [Report Agent] → Synthesizes final answer
        ↓
    Polished Final Response

Specialized Agents
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. **Router Agent**: Analyzes queries and delegates to appropriate specialists

   - Answers simple general questions directly
   - Calls SQL assistant for database/analytics queries
   - Calls knowledge assistant for documentation/code queries
   - Uses both for hybrid questions requiring multiple sources

2. **SQL Agent**: Executes analytical queries against the Chinook music database

   - Translates natural language to SQL
   - Queries transactional data (sales, artists, tracks, genres, customers)
   - Returns formatted results with proper analysis
   - Uses ``mcp_ohmy_sql`` library for safe SELECT-only execution

3. **Knowledge Agent**: Retrieves project documentation and code information

   - Semantic search over comprehensive knowledge base
   - Vector embeddings using FastEmbed (BAAI/bge-small-en-v1.5)
   - S3-based storage with ``s3vectorm`` library
   - Returns relevant code references and documentation

4. **Report Agent**: Synthesizes intermediate results into polished final answers

   - Combines outputs from multiple agents
   - Formats responses with proper structure (headings, tables, code blocks)
   - Ensures comprehensive coverage of all aspects

Data Sources
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- **Chinook SQLite Database**: Music store transactional data with tables for Invoice, InvoiceLine, Track, Album, Artist, Genre, and Customer
- **Vector Knowledge Base**: Project documentation, source code, and repository information stored in AWS S3 with semantic search capabilities
- **Future**: Pre-aggregated metrics store for fast KPI access


Architecture & Technology Stack
------------------------------------------------------------------------------

Core Framework
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- **Anthropic Strands**: Primary agent orchestration framework
- **Claude Sonnet 4**: LLM powering all agent reasoning
- **Python 3.11+**: Core language

Data & Storage
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- **Chinook SQLite**: Sample music store database
- **AWS S3**: Document storage for knowledge base
- **s3vectorm**: Vector similarity search over S3
- **FastEmbed**: Text embeddings (BAAI/bge-small-en-v1.5, 384 dimensions)

Specialized Libraries
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- **mcp_ohmy_sql**: SQL query execution via Model Context Protocol
- **boto3**: AWS S3 integration
- **strands**: Agent framework with tool composition


Quick Start
------------------------------------------------------------------------------

Installation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Install from PyPI:

.. code-block:: console

    $ pip install music-bi-agent-poc

Or install from source:

.. code-block:: console

    $ git clone https://github.com/MacHu-GWU/music_bi_agent_poc-project.git
    $ cd music_bi_agent_poc-project
    $ make venv-create
    $ make install-all


Basic Usage
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Simple Query - Router Answers Directly**:

.. code-block:: python

    from music_bi_agent_poc.agent import run_agent

    # General knowledge question
    response = run_agent("What is a music genre?")
    print(response)


**SQL Analytics Query**:

.. code-block:: python

    # Database query requiring SQL agent
    response = run_agent(
        "Which artist has the highest sales? "
        "Show me the SQL statement and results in a markdown table."
    )
    print(response)
    # Output: SQL query + formatted results table + analysis


**Knowledge Base Query**:

.. code-block:: python

    # Documentation/code query requiring knowledge agent
    response = run_agent(
        "How do I run the test suite in this project? "
        "Show me the exact commands."
    )
    print(response)
    # Output: Detailed test commands from project documentation


**Hybrid Query - Multiple Agents**:

.. code-block:: python

    # Complex query requiring both SQL and knowledge agents
    response = run_agent(
        "Show me the top 5 genres by revenue and explain "
        "how the Genre table is structured in the database schema."
    )
    print(response)
    # Output: SQL analysis + schema documentation from knowledge base


Low-Level API Access
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For direct agent access without orchestration:

.. code-block:: python

    from music_bi_agent_poc.one.api import one

    # Use SQL agent directly
    sql_response = one.sql_agent(
        "Run SQL if needed: 'What tables are in the database?'. "
        "Use your available tools to gather information."
    )
    print(sql_response)

    # Use knowledge agent directly
    knowledge_response = one.knowledge_agent(
        "Retrieve knowledge if needed: 'Which module defines the agents?'. "
        "Use your available tools to retrieve information from knowledge base."
    )
    print(knowledge_response)

    # Access RAG retrieval directly
    chunks = one.retrieve(query="How to configure database connections?")
    for chunk in chunks:
        print(chunk)


.. _install:

Development Setup
------------------------------------------------------------------------------

Prerequisites
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Python 3.11 or higher
- AWS credentials configured (for S3 knowledge base)
- Virtual environment (managed automatically)

Setup Steps
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. **Clone and Setup Environment**:

.. code-block:: console

    $ git clone https://github.com/MacHu-GWU/music_bi_agent_poc-project.git
    $ cd music_bi_agent_poc-project
    $ make venv-create
    $ make install-all

2. **Run Tests**:

.. code-block:: console

    $ make test          # Run unit tests
    $ make cov           # Run with coverage
    $ make view-cov      # View coverage report in browser

3. **Build Documentation**:

.. code-block:: console

    $ make build-doc     # Build Sphinx docs
    $ make view-doc      # Open docs in browser

4. **Explore Examples**:

Interactive Jupyter notebooks are available in ``docs/source/``:

- ``01-Rag-Agent-Example/index.ipynb``: Knowledge retrieval examples
- ``02-SQL-Agent-Example/index.ipynb``: Database query examples
- ``03-Main-Agent-Example/index.ipynb``: Full multi-agent orchestration

Run with:

.. code-block:: console

    $ jupyter notebook docs/source/


Project Structure
------------------------------------------------------------------------------

.. code-block::

    music_bi_agent_poc-project/
    ├── music_bi_agent_poc/          # Main package
    │   ├── agent.py                 # Multi-agent orchestration (run_agent)
    │   ├── one/                     # Core agent implementations
    │   │   ├── one_01_main.py       # Main One class
    │   │   ├── one_03_agent.py      # Agent definitions (router, sql, knowledge, report)
    │   │   ├── one_04_sql.py        # SQL tools and configuration
    │   │   └── one_05_rag.py        # RAG/vector search tools
    │   ├── paths.py                 # Path management
    │   └── prompts/                 # Agent system prompts
    ├── docs/source/                 # Documentation and examples
    │   ├── 01-Rag-Agent-Example/    # RAG agent demos
    │   ├── 02-SQL-Agent-Example/    # SQL agent demos
    │   └── 03-Main-Agent-Example/   # Full orchestration demos
    ├── tests/                       # Unit tests
    ├── Makefile                     # Development automation
    └── pyproject.toml              # Project dependencies


Use Cases
------------------------------------------------------------------------------

Business Intelligence
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- "What are the top 5 genres by revenue?"
- "Which customers spent the most? Include name, country, and total amount."
- "Show me sales trends for the Rock genre over time."

Code & Documentation Search
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- "Which Python module defines the agent and its prompt?"
- "How do I configure the database connection?"
- "What testing strategy does this project use?"

Hybrid Analysis
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- "Explain the Genre table structure and show me top-performing genres."
- "How is the SQL agent implemented and what queries can it run?"


Contributing
------------------------------------------------------------------------------

Contributions are welcome! Please follow the development workflow:

1. Fork the repository
2. Create a feature branch
3. Make changes following the Python development standards (see ``.claude/md/`` guides)
4. Run tests: ``make test``
5. Ensure coverage: ``make cov``
6. Submit a pull request

For detailed development guidelines, see:

- ``CLAUDE.md``: Project development guide
- ``.claude/md/Python-test-strategy-instruction.md``: Testing strategy
- ``.claude/md/pywf-open-source-Python-docstring-guide.md``: Docstring standards


Links
------------------------------------------------------------------------------

- **Documentation**: https://music-bi-agent-poc.readthedocs.io
- **GitHub**: https://github.com/MacHu-GWU/music_bi_agent_poc-project
- **PyPI**: https://pypi.org/project/music-bi-agent-poc
- **Issues**: https://github.com/MacHu-GWU/music_bi_agent_poc-project/issues
- **Release History**: https://github.com/MacHu-GWU/music_bi_agent_poc-project/blob/main/release-history.rst


License
------------------------------------------------------------------------------

This project is licensed under the MIT License. See the LICENSE file for details.


Acknowledgments
------------------------------------------------------------------------------

- **Chinook Database**: Sample database by Luis Rocha (https://github.com/lerocha/chinook-database)
- **Anthropic Strands**: Agent orchestration framework
- **Claude Sonnet 4**: Anthropic's LLM powering all agent reasoning
