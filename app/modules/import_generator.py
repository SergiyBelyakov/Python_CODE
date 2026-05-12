from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


@dataclass
class ImportArtifacts:
    constraints: list[str]
    import_queries: list[str]
    rel_queries: list[str]
    validation_queries: list[str]


class OracleNeo4jImportGenerator:
    def generate(self, tables: pd.DataFrame, columns: pd.DataFrame, fks: pd.DataFrame, schema: str) -> ImportArtifacts:
        constraints = [
            "CREATE CONSTRAINT dbtable_name_unique IF NOT EXISTS FOR (t:DbTable) REQUIRE t.name IS UNIQUE",
            "CREATE CONSTRAINT dbcolumn_key_unique IF NOT EXISTS FOR (c:DbColumn) REQUIRE c.key IS UNIQUE",
        ]

        imports: list[str] = []
        for table_name in tables["TABLE_NAME"].dropna().unique():
            tcols = columns[columns["TABLE_NAME"] == table_name]
            select_columns = [self._oracle_select_expr(row["COLUMN_NAME"], str(row.get("DATA_TYPE", ""))) for _, row in tcols.iterrows()]
            sql = f"SELECT {', '.join(select_columns)} FROM {schema}.{table_name}"
            imports.append(
                "CALL apoc.periodic.iterate(" 
                f"\"{sql}\", "
                f"\"MERGE (n:O{table_name} {{id:toString(row.ID)}}) SET n += row\","
                "{batchSize:$batch_size, parallel:false})"
            )

        rel_queries = []
        for _, fk in fks.iterrows():
            rel_queries.append(
                f"MATCH (c:O{fk['CHILD_TABLE']}), (p:O{fk['PARENT_TABLE']}) "
                f"WHERE toString(c.{fk['CHILD_COLUMN']}) = toString(p.{fk['PARENT_COLUMN']}) "
                f"MERGE (c)-[:FK_TO {{fk:'{fk['CHILD_TABLE']}.{fk['CHILD_COLUMN']}->{fk['PARENT_TABLE']}.{fk['PARENT_COLUMN']}'}}]->(p)"
            )

        return ImportArtifacts(constraints, imports, rel_queries, ["MATCH ()-[r:FK_TO]->() RETURN count(r)"])

    def _oracle_select_expr(self, column: str, dtype: str) -> str:
        dt = dtype.upper()
        if "TIMESTAMP" in dt:
            return f"TO_CHAR({column}, q'[YYYY-MM-DD HH24:MI:SS.FF6]') AS {column}"
        if "DATE" in dt:
            return f"TO_CHAR({column}, q'[YYYY-MM-DD HH24:MI:SS]') AS {column}"
        return column
