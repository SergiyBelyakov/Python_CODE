# Oracle → Neo4j Graph ETL Workbench (Desktop)

Python desktop застосунок для:
- завантаження metadata Oracle (tables/columns/FK),
- генерації імпортних Cypher/Oracle SQL шаблонів,
- побудови графової схеми FK,
- конструктора Cypher запитів на базі FK-зв'язків.

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m app.main
```

## Implemented foundation

- Tabbed UI: Metadata, Neo4j Import, Graph Model, Query Builder, Validation, Logs.
- Metadata loader (CSV/XLSX) with normalization (uppercase/trim/column mapping).
- Oracle→Neo4j import generator with explicit SELECT columns and DATE/TIMESTAMP formatting.
- FK relationship query generation.
- Basic graph table classification helper.
- FK-based Cypher query builder skeleton.
