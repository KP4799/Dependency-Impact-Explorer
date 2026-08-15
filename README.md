# 🔍 Dependency Impact Explorer

A graph-based application for analyzing how package dependencies affect software repositories.

This project uses Neo4j-compatible graph storage (CognoDB), Python, and Streamlit to model and explore dependency relationships between developers, repositories, packages, technologies, and vulnerabilities.

The application allows users to select a package and immediately identify:

- Which repositories are affected
- Which developers maintain those repositories
- The complete dependency chain between a repository and the selected package

---

## 📖 Overview

Modern software systems rely heavily on third-party packages and internal libraries. A change in a single dependency can affect multiple repositories across an organization.

Traditional relational databases can store dependency information, but traversing variable-length dependency chains often requires complex recursive queries and multiple self-joins.

Graph databases are better suited for this type of problem because relationships are stored as first-class entities and can be traversed efficiently.

This project demonstrates how graph databases can be used to perform dependency impact analysis.

---

## ✨ Features

- Dependency impact analysis
- Multi-hop graph traversal
- Developer-to-repository relationships
- Repository-to-package relationships
- Package-to-package dependency mapping
- Vulnerability propagation analysis
- Interactive web interface
- Parameterized Cypher queries
- Graceful error handling

---

## 🏗️ Graph Data Model

### Nodes

| Node | Properties |
| --- | --- |
| Developer | name |
| Repository | name, language |
| Package | name, version |
| Technology | name |
| Vulnerability | name, severity |

---

### Relationships

| Relationship | Description |
| --- | --- |
| MAINTAINS | Developer → Repository |
| DEPENDS_ON | Repository → Package |
| DEPENDS_ON | Package → Package |
| USES | Package → Technology |
| HAS_VULNERABILITY | Package → Vulnerability |

---

## 📊 Graph Diagram

```text
Developer
    │
    ▼
Repository
    │
    ▼
Package
   ╱ ╲
  ▼   ▼
Technology   Vulnerability
```

Replace this section with a screenshot of the graph visualization from CognoDB if available.

---

## 🗂️ Dataset

The dataset is generated automatically using a seed script.

### Dataset Statistics

| Entity | Count |
| --- | --- |
| Developers | 10 |
| Repositories | 10 |
| Packages | 20 |
| Technologies | 5 |
| Vulnerabilities | 5 |

### Example Repositories

- payments-api
- checkout-service
- customer-api
- analytics-worker
- auth-service

### Example Packages

- auth-lib
- jwt-lib
- crypto-lib
- payment-sdk
- notification-sdk

---

## 🔍 Graph Queries

### 1. Repository Impact Analysis

Find all repositories affected by a selected package.

```cypher
MATCH path =
    (r:Repository)-[:DEPENDS_ON*1..5]->
    (p:Package {name: $package})

OPTIONAL MATCH
    (d:Developer)-[:MAINTAINS]->(r)

RETURN
    r.name AS repository,
    collect(DISTINCT d.name) AS developers,
    path

ORDER BY repository
```

Example:

```text
crypto-lib

↓

payments-api
customer-api
checkout-service
auth-service
```

This query performs a variable-length traversal through the dependency graph.

---

### 2. Vulnerability Propagation Analysis

Determine which repositories are affected by a specific vulnerability.

```cypher
MATCH
    (r:Repository)-[:DEPENDS_ON*1..5]->
    (p:Package)-[:HAS_VULNERABILITY]->
    (v:Vulnerability {name: $vulnerability})

RETURN DISTINCT
    r.name AS repository

ORDER BY repository
```

Example:

```text
Weak encryption affects:

auth-service
checkout-service
customer-api
payments-api
```

---

### Why is this query difficult in a relational database?

A relational implementation would require:

- Recursive queries
- Multiple self-joins
- Additional dependency tables

Graph databases handle variable-length traversals naturally.

---

## 🖥️ User Interface

The application provides an interactive interface for dependency exploration.

Workflow:

1. Select a package.
2. Click **Analyze**.
3. Review the affected repositories.
4. Examine the dependency path.
5. Identify repository maintainers.

---

## 📸 Screenshots

### Application Interface

Insert screenshot here.

---

### Dependency Analysis

Insert screenshot here.

---

### Graph Visualization

Insert screenshot here.

---

### Vulnerability Analysis Query

Insert screenshot here.

---

## 📁 Project Structure

```text
dependency-impact-explorer
│
├── app
│   ├── db
│   │   ├── connection.py
│   │   └── queries.py
│   │
│   └── main.py
│
├── scripts
│   ├── seed.py
│   ├── test_connection.py
│   └── verify.py
│
├── docs
│
├── requirements.txt
│
├── .env.example
│
└── README.md
```

---

## ⚙️ Installation

Clone the repository:

```bash
git clone <repository-url>

cd dependency-impact-explorer
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment:

### macOS/Linux

```bash
source venv/bin/activate
```

### Windows

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 🔐 Environment Variables

Create a `.env` file:

```env
NEO4J_URI=

NEO4J_USERNAME=

NEO4J_PASSWORD=
```

---

## 🌱 Seed the Database

```bash
python -m scripts.seed
```

---

## 🚀 Run the Application

```bash
python -m streamlit run app/main.py
```

---

## ⚠️ Error Handling

The application handles database failures gracefully.

If the database becomes unavailable, the user receives a descriptive error message instead of a Python exception.

---

## 🔮 Future Improvements

- Dependency graph visualization inside the application
- Repository search
- Vulnerability dashboard
- Interactive graph exploration
- Repository filtering

---

## 🛠️ Technologies

- Python
- Streamlit
- Neo4j Driver
- Cypher
- CognoDB

---

## 👤 Author

Your Name
