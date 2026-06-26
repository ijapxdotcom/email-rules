# 📧 Email-RuleOps: Agnostic Triage & Routing Framework

An enterprise-grade, deterministic triage and routing engine designed as an intelligent gateway for complex email operations. 

> [!NOTE]
> This framework serves as a scalable, high-performance triage system. It operates deterministically using regex-based intent classification before routing payloads to downstream workflow automation, CRM tools, or AI Agents (MCP/LangGraph). It applies core MLOps principles—such as Shadow Mode, Human-in-the-Loop, and Telemetry—to a deterministic rule engine, a practice known as Continuous Rule Engineering (RuleOps).

---

## 🏛️ Architecture Overview

The system is designed with an **Agnostic Architecture**. It is not tied to a specific email client interface, relying instead on universal protocols (IMAP/SMTP). Although the current use case implementation is configured for a commercial B2B/B2G operation (CFTV, SCA, Government Contracts), the core pipeline is completely decoupled. By simply replacing the regex patterns and target dictionary values in the rules engine, this gateway can be adapted to any domain (e.g., healthcare, logistics, customer support).

```mermaid
graph TD
    A[Incoming Email/Payload via IMAP] --> B[RuleOps Engine Core]
    B --> C{Deterministic Regex Engine}
    C -->|Priority: Max| D[Risco Contratual & Prazos]
    C -->|Priority: High| E[Oportunidades Gov / Projetos Core]
    C -->|Priority: Medium| F[Operação Comercial / Suprimentos]
    C -->|Priority: Low| G[Informativo / Descarte]
    C -->|Fallback| H[Triagem Manual / AI Gateway Audit]
    D --> I[Dict Serialization]
    E --> I
    F --> I
    G --> J[Auto Archive]
    H --> K[Manual Review Queue / CSV Telemetry]
    I --> L[Downstream: APIs / AI Agents (MCP) / CRM]
```

## ✨ Core Features

- **Fail-Fast Evaluation**: High-priority risks (e.g., contractual delays, government notices) are evaluated at the top of the decision tree to ensure near-zero latency for critical paths.
- **Agnostic Ingestion**: Operates flawlessly in background environments via IMAP, eliminating UI/RPA fragilities.
- **Structured Dict Serialization**: Instead of raw strings, the engine returns clean `Dict[str, str]` outputs (JSON-like structure) natively ready for downstream integrations like ServiceNow, Salesforce CRM, or LLM-based Tool Calling.
- **Built-in Telemetry**: Every routing decision is logged locally (CSV), providing the dataset needed for future Machine Learning tracking and continuous tuning.

## 🚀 Evolutionary Roadmap (Design to Scale)

This project is built using Evolutionary Design principles, allowing it to start as a zero-cost deterministic engine and scale into a fully autonomous AI platform.

### Phase 1: RuleOps & Observability (Current)
- Asynchronous email processing via IMAP using a Regex rule engine.
- Establishes Observability via CSV logging (the foundation for ML Tracking).

### Phase 2: Modularization & API Gateway
- Transforming the rules engine into a REST API using FastAPI.
- The script transitions from a standalone file to a microservice responding on `localhost:8000`.

### Phase 3: Tool Calling & MCP Integration
- Wrapping the framework into a Tool or MCP (Model Context Protocol) Server.
- Integration with AI orchestration frameworks (LangGraph/CrewAI) where an Agent decides when to fetch and triage emails.

### Phase 4: Cloud & Predictive Intelligence
- Leveraging the telemetry dataset to train NLP models (Scikit-Learn/Embeddings), replacing Regex with true Predictive Intelligence.
- Containerization with Docker and deployment to Cloud environments (AWS/GCP).

## 🧠 Executive Triage & Automation Matrix (Sample Implementation)

The current implementation routes highly complex workflows autonomously. Below is a subset of the configured logic:

| Category | Priority | Triggers (Subject / Body) | Route Target | Action Workflow |
| :--- | :--- | :--- | :--- | :--- |
| **Risco Contratual e Prazos** | MÁXIMA | `notificação de atraso`, `prorrogação de prazo`, `cronograma`, `ofício` | Engenharia / Gestão de Contas | Mitigate financial risk and coordinate executive response. |
| **Oportunidades Gov. (14.133)** | ALTA - CRÍTICO | `cotação eletrônica`, `dispensa de licitação`, `comprasnet`, `14.133` | Comercial / Licitações | Analyze bidding window, prepare bid document, and track dispute. |
| **Projetos Técnicos (Core)** | ALTA | `CFTV`, `SCA`, `CÂMERAS`, `CONTROLE DE ACESSO` | Engenharia / Pré-Vendas | Scope technical viability and hardware requirements. |
| **Gestão de Contratos (CREA)** | ALTA - TRAVA FATURAMENTO | `ART`, `Crea`, `Apostilamento`, `Aditivo` | Licitações e Contratos | Validate replacement documentation and align with contract fiscal. |

## 🛠️ Getting Started (Local Setup)

1. **Clone the repository**:
   ```bash
   git clone https://github.com/ijapxdotcom/email-rules.git
   cd email-rules
   ```

2. **Environment Setup**:
   Create a `.env` file in the root directory (this file is git-ignored for security):
   ```env
   EMAIL_HOST="imap.yourprovider.com"
   EMAIL_USER="your-email@company.com"
   EMAIL_PASS="your-app-password"
   ```

3. **Install Dependencies**:
   This project relies on strict typing and linting for enterprise standards.
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Engine**:
   ```bash
   python main.py
   ```
