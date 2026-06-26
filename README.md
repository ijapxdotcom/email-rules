# 📧 Email-RuleOps: Agnostic Triage & Routing Framework

An enterprise-grade, deterministic triage and routing engine designed as an intelligent gateway for complex email operations.

> [!NOTE]
> This framework serves as a scalable, high-performance triage system. It operates deterministically using regex-based intent classification before routing payloads to downstream workflow automation, CRM tools, or AI Agents (MCP/LangGraph).
>
> It applies core MLOps principles—such as Shadow Mode, Human-in-the-Loop, and Telemetry—to a deterministic rule engine, a practice known as **Continuous Rule Engineering (RuleOps)**.

---

## 🏛️ Architecture Overview

The system is designed with an **Agnostic Architecture**. It is not tied to a specific email client interface, relying instead on universal protocols (IMAP/SMTP). 

Although the current use case implementation is configured for a commercial B2B/B2G operation (CFTV, SCA, Government Contracts), the core pipeline is completely decoupled. By simply replacing the regex patterns and target dictionary values in the rules engine, this gateway can be adapted to any domain (e.g., healthcare, logistics, customer support).

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

---

## 🧠 Executive Triage & Automation Matrix

The system implements 13 production-ready routing rules mapped directly to corporate workflows:

| # | Category | Priority | Triggers (Subject / Body) | Route Target | Action Workflow |
| :---: | :--- | :---: | :--- | :--- | :--- |
| **1** | **Risco Contratual e Prazos** | **MÁXIMA** | `notificação de atraso`, `prorrogação de prazo`, `cronograma`, `ofício` | Engenharia / Gestão de Contas (Aloisio) | Mitigate financial risk and coordinate executive response. |
| **2** | **Oportunidades Gov. (14.133)** | **ALTA - CRÍTICO** | `cotação eletrônica`, `dispensa de licitação`, `comprasnet`, `14.133` | Comercial / Licitações | Analyze bidding window, prepare bid document, and track dispute. |
| **3** | **Licitações Estatais** | **ALTA - CRÍTICO** | `licitação eletrônica aberta`, `copasa`, `envio de propostas` | Comercial / Licitações | Fetch bidding document (Edital) and run feasibility study. |
| **4** | **Pesquisa de Preços Judiciária** | **ALTA - CRÍTICO** | `pesquisa de preços`, `prorrogação da vigência`, `tst`, `solicitação de orçamento` | Comercial / Gestão de Contas | Prepare signed commercial proposal including taxes. |
| **5** | **Projetos Técnicos (Core)** | **ALTA** | `cftv`, `sca`, `câmeras`, `controle de acesso`, `vídeomonitoramento` | Engenharia / Pré-Vendas | Technical requirements analysis, item quantification, and design validation. |
| **6** | **Gestão de Contratos (CREA)** | **ALTA - TRAVA FATURAMENTO** | `art`, `crea`, `pendente de aprovação`, `apostilamento`, `aditivo` | Licitações e Contratos / Engenharia (Kevin Diego) | Validate replacement documentation and align with contract fiscal. |
| **7** | **Assinaturas Externas Gov.** | **ALTA** | `assinatura externa`, `disponibilizada para a assinatura` | Diretoria / Administrativo (Marcelo de Almeida) | Notify board to run digital signature on government portal (e.g., SEI). |
| **8** | **Cotações e Contratos** | **ALTA** | `cotação de preço`, `contratos`, `aditivos` | Gestão de Contas (Aloisio) | Flag as 'New' and route to Account Management. |
| **9** | **Fornecimento e Faturamento** | **MÉDIA** | `faturamento`, `faturar`, `cnpj`, `cadastro` | Compras / Financeiro (Aloisio) | Cross-reference tax details and execute procurement. |
| **10** | **Fornecedores Técnicos** | **MÉDIA** | `invenzi`, `intelbras`, `dahua` | Engenharia / Suprimentos | Analyze vendor documentation and hardware pricing sheets. |
| **11** | **Pipeline Comercial e CRM** | **MÉDIA** | `oportunidades de licitação`, `status atual`, `crm` | Comercial / Gestão de Contas (Igor / Luana) | Synchronize statuses with pipeline tracking systems. |
| **12** | **Conselhos e Protocolos** | **MÉDIA** | `conselho regional`, `crt`, `baixa de registro`, `sinceti` | Suporte Técnico / Administrativo (Alessandro) | Audit external council status and portal credentials. |
| **13** | **Informativo / Descarte** | **BAIXA** | `sigeo`, `documentos fiscais devolvidos` | Nenhuma | Auto-archive quietly. |

---

## 💻 Simulation Case Study: Input vs. Output

This shows exactly how the structured Python engine parses an incoming request:

### Input Email Payload
```json
{
  "remetente": "engenharia@control-t.com.br",
  "assunto": "Fwd: Notificação de atraso de OS",
  "corpo": "Bom dia Helen, encaminho em anexo nossa solicitação de prorrogação de prazo..."
}
```

### Execution
```python
from src.core.rules import classificar_email

resultado = classificar_email(
    remetente="engenharia@control-t.com.br",
    assunto="Fwd: Notificação de atraso de OS",
    corpo="Bom dia Helen, encaminho em anexo nossa solicitação de prorrogação de prazo..."
)
print(resultado)
```

### Serialized Dict Output (JSON)
```json
{
  "categoria": "Risco Contratual e Prazos",
  "destino": "Engenharia / Gestão de Contas (Aloisio)",
  "prioridade": "MÁXIMA",
  "acao": "Rotear para Aloisio montar resposta executiva/técnica para mitigar risco financeiro."
}
```

---

## 🎯 Best Practices & Engineering Cleanliness

This project is built under strict enterprise development standards:

1. **Security-First (Secret Masking)**: No credentials are hardcoded. A template [`.env.example`](file:///.env.example) outlines required parameters, while the local [`.env`](file:///.env) is completely Git-ignored via [`.gitignore`](file:///.gitignore).
2. **Predictive Tool-Calling Schema**: Returns dictionary serialization (`Dict[str, str]`) instead of unstructured logs. This is naturally aligned to function calling/tool calling in modern AI Orchestrators (LangGraph, CrewAI, AutoGen).
3. **Regex Robustness**: Patterns handle Brazilian-Portuguese diacritics and character variants safely (e.g., `notifica[cç][aã]o` matches both "notificação" and "notificacao").
4. **Consistent Style Guidelines**: The codebase configures standard python specifications using [`.editorconfig`](file:///.editorconfig), and sets dependencies cleanly using frozen versions in [`requirements.txt`](file:///requirements.txt).

---

## 📂 Project Structure

```
Email-RuleOps/
├── data/              # Classification logs and local databases (CSV Telemetry)
├── src/
│   ├── core/          # Business logic and RuleOps core config
│   │   ├── config.py  # Environment variables loader and fail-fast check
│   │   └── rules.py   # Main deterministic intent-matching engine
│   ├── models/        # Strict typings and schema structures (Future Pydantic models)
│   └── services/      # Connection interfaces (IMAP/SMTP/API)
├── .editorconfig
├── .env.example
├── .gitignore
└── requirements.txt
```

---

## 🚀 Evolutionary Roadmap (Design to Scale)

This project is built using Evolutionary Design principles, allowing it to start as a zero-cost deterministic engine and scale into a fully autonomous AI platform.

- **Phase 1: RuleOps & Observability (Current)**: Asynchronous email processing via IMAP using a Regex rule engine. Establishes Observability via CSV logging (the foundation for ML Tracking).
- **Phase 2: Modularization & API Gateway**: Transforming the rules engine into a REST API using FastAPI. The script transitions from a standalone file to a microservice responding on `localhost:8000`.
- **Phase 3: Tool Calling & MCP Integration**: Wrapping the framework into a Tool or MCP (Model Context Protocol) Server. Integration with AI orchestration frameworks (LangGraph/CrewAI) where an Agent decides when to fetch and triage emails.
- **Phase 4: Cloud & Predictive Intelligence**: Leveraging the telemetry dataset to train NLP models (Scikit-Learn/Embeddings), replacing Regex with true Predictive Intelligence. Containerization with Docker and deployment to Cloud environments (AWS/GCP).

---

## 🛠️ Getting Started (Local Setup)

1. **Clone the repository**:
   ```bash
   git clone https://github.com/ijapxdotcom/email-rules.git
   cd email-rules
   ```

2. **Environment Setup**:
   Create a `.env` file in the root directory:
   ```env
   EMAIL_HOST="imap.yourprovider.com"
   EMAIL_USER="your-email@company.com"
   EMAIL_PASS="your-app-password"
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Engine**:
   ```bash
   python main.py
   ```
