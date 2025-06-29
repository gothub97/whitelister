# 🕵️‍♂️ Whitelister

**Whitelister** is an open-source initiative to build a forensic profiler for ERC20 tokens, designed to help compliance teams and auditors evaluate token risk based entirely on on-chain data.

> FBI-style profiling for crypto assets — from contract bytecode to wallet relationships.

---

## 🚧 Project Status

This project is **in early design phase**.
We are currently defining:
- The `TokenComplianceProfile` JSON schema
- The core modules for contract and holder analysis
- The stack architecture (Django API + on-chain extractors)

Implementation is expected to begin soon. Contributions and collaborators are welcome.

---

## 🎯 Vision

Whitelister will generate both:
- 🔭 A high-level executive risk overview
- 🕵️ A detailed forensic trace for compliance audits

The output will be a structured JSON profile per token, designed to be LLM/agent-compatible and API-consumable.

---

## 🛠️ Getting Started

### Prerequisites

- Python 3.8+
- pip (Python package installer)
- PostgreSQL

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/whitelister.git
    cd whitelister
    ```

2.  **Set up the environment:**
    - Create a virtual environment (recommended):
      ```bash
      python -m venv venv
      source venv/bin/activate  # On Windows use `venv\Scripts\activate`
      ```
    - Create a `.env` file from the example:
      ```bash
      cp whitelister_backend/.env.example whitelister_backend/.env
      ```
    - Update `whitelister_backend/.env` with your PostgreSQL database credentials and any other necessary environment variables (e.g., RPC endpoint for Web3.py if you plan to fetch live on-chain data).

3.  **Install dependencies:**
    This project uses Poetry for managing dependencies, as defined in `pyproject.toml`. The recommended way to install dependencies is using Poetry:
    ```bash
    pip install poetry
    poetry install
    ```
    Alternatively, if you prefer to use pip directly, you will need to manually generate a `requirements.txt` file from the `pyproject.toml` file using a full Poetry installation (`poetry export -f requirements.txt --output requirements.txt --without-hashes`) and then install using `pip install -r requirements.txt`. Please note that a `requirements.txt` is not provided in the repository.

4.  **Apply database migrations:**
    If using Poetry:
    ```bash
    poetry run python manage.py migrate
    ```
    If using pip with a virtual environment:
    ```bash
    python manage.py migrate
    ```

### Running the Development Server

To start the Django development server:
- If using Poetry:
  ```bash
  poetry run python manage.py runserver
  ```
- If using pip with a virtual environment:
  ```bash
  python manage.py runserver
  ```

The API will typically be available at `http://127.0.0.1:8000/`.

### Running Tests

To run the test suite:
- If using Poetry:
  ```bash
  poetry run python manage.py test api
  ```
- If using pip with a virtual environment:
  ```bash
  python manage.py test api
  ```

---

## 📦 Planned Modules

| Module             | Purpose                                                  |
|--------------------|----------------------------------------------------------|
| `contractAnalysis` | Detect proxy patterns, upgradability, custom logic       |
| `holderGraph`      | Top holder concentration, sybil patterns, 2-hop graphing |
| `txAnalysis`       | Activity breakdown, flashloan detection                  |
| `identityCheck`    | Creator traceability, LinkedIn/GitHub matching           |
| `docAnalysis`      | Whitepaper/website scan                                  |
| `legalScreening`   | OFAC / sanctions / abuse db matching                     |

---

## ⚙️ Stack

- **Django & Django REST Framework** — REST API interface
- **Web3.py** — On-chain data extraction via public RPC (planned for full implementation)
- **Slither / solc** — Contract static analysis (planned)
- **PostgreSQL** — Structured profile storage
- **Celery (optional)** — For async processing (planned)
- **Agent-compatible JSON** — For LLM workflows

---

## 📤 Sample Output (in design)

```json
{
  "token_address": "0x...",
  "risk_score": 78.2,
  "recommendation": "enhanced_due_diligence",
  "flags": ["proxy_detected", "top10_hold_92_percent"],
  "modules": {
    "contractAnalysis": {...},
    "holderGraph": {...}
  }
}
```

---

## 🛡 License

Intended license: **Apache License 2.0** (will be added upon first release)

---

## 🤝 Join Us

If you’re a smart contract auditor, compliance engineer, or just curious about the mechanics of risk in crypto, we’re happy to collaborate.

Open issues, contribute ideas, or follow the roadmap as we build.

---

## 💡 Maintainer

Initiated by [@gothub97](https://github.com/gothub97)
Compliance + automation focused. Building with facts, not vibes.
