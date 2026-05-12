from __future__ import annotations

import pandas as pd


class GraphModelBuilder:
    def classify_table(self, table_name: str, stats: pd.DataFrame | None = None) -> str:
        name = table_name.upper()
        if name.endswith("_DICT") or name.startswith("REF_"):
            return "dictionary"
        if name.startswith("TRN_") or "ACT" in name:
            return "transaction"
        return "entity"
