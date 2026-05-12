from __future__ import annotations

import pandas as pd


class QueryBuilder:
    def build_fk_match(self, start_table: str, end_table: str, fk_path: pd.DataFrame) -> str:
        alias_map = {}
        statements = []

        for i, row in fk_path.iterrows():
            child = row["CHILD_TABLE"]
            parent = row["PARENT_TABLE"]
            child_alias = alias_map.setdefault(child, f"t{i}c")
            parent_alias = alias_map.setdefault(parent, f"t{i}p")
            if i == 0:
                statements.append(f"MATCH ({child_alias}:O{child})")
            statements.append(f"MATCH ({parent_alias}:O{parent})")
            statements.append(
                f"WHERE toString({child_alias}.{row['CHILD_COLUMN']})="
                f"toString({parent_alias}.{row['PARENT_COLUMN']})"
            )

        final_alias = alias_map.get(end_table, "end_node")
        statements.append(f"RETURN {final_alias} LIMIT 100")
        return "\n".join(statements)
