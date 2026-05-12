from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict

import pandas as pd


@dataclass
class MetadataBundle:
    tables: pd.DataFrame
    columns: pd.DataFrame
    fks: pd.DataFrame
    table_classification: pd.DataFrame | None = None
    stats: pd.DataFrame | None = None


class MetadataLoader:
    REQUIRED_COLUMNS = {
        "tables": ["TABLE_NAME"],
        "columns": ["TABLE_NAME", "COLUMN_NAME", "DATA_TYPE"],
        "fk": ["CHILD_TABLE", "PARENT_TABLE", "CHILD_COLUMN", "PARENT_COLUMN"],
    }

    def load(self, paths: Dict[str, str | Path]) -> MetadataBundle:
        tables = self._read_any(paths["tables"])
        columns = self._read_any(paths["columns"])
        fks = self._read_any(paths["fk"])

        tables = self._normalize(tables)
        columns = self._normalize(columns)
        fks = self._normalize(fks)

        self._assert_columns("tables", tables)
        self._assert_columns("columns", columns)
        self._assert_columns("fk", fks)

        return MetadataBundle(tables=tables, columns=columns, fks=fks)

    def _read_any(self, path: str | Path) -> pd.DataFrame:
        path = Path(path)
        if path.suffix.lower() == ".csv":
            return pd.read_csv(path)
        if path.suffix.lower() in {".xlsx", ".xls"}:
            return pd.read_excel(path)
        raise ValueError(f"Unsupported metadata format: {path.suffix}")

    def _normalize(self, frame: pd.DataFrame) -> pd.DataFrame:
        frame = frame.rename(columns={c: c.strip().upper() for c in frame.columns})
        for col in frame.columns:
            if frame[col].dtype == object:
                frame[col] = frame[col].astype(str).str.strip()
        for candidate in ["TABLE_NAME", "COLUMN_NAME", "CHILD_TABLE", "PARENT_TABLE", "CHILD_COLUMN", "PARENT_COLUMN"]:
            if candidate in frame.columns:
                frame[candidate] = frame[candidate].str.upper()
        return frame

    def _assert_columns(self, name: str, frame: pd.DataFrame) -> None:
        missing = [c for c in self.REQUIRED_COLUMNS[name] if c not in frame.columns]
        if missing:
            raise ValueError(f"{name} metadata misses required columns: {missing}")
