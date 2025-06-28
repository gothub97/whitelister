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

## 🛠️ Stack Preview (Planned)

- **Django** — REST API interface
- **Web3.py** — On-chain data extraction via public RPC
- **Slither / solc** — Contract static analysis
- **PostgreSQL** — Structured profile storage
- **Celery (optional)** — For async processing
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

Initiated by [@gauthier_flowdesk](https://github.com/<your-handle>)  
Compliance + automation focused. Building with facts, not vibes.
