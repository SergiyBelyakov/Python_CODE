from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QTabWidget,
    QPushButton,
    QTextEdit,
    QLabel,
    QHBoxLayout,
)
from app.modules.metadata_loader import MetadataLoader
from app.modules.import_generator import OracleNeo4jImportGenerator
from app.modules.query_builder import QueryBuilder
from app.modules.graph_model_builder import GraphModelBuilder


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Oracle → Neo4j Graph ETL Workbench")
        self.resize(1400, 900)

        self.metadata_loader = MetadataLoader()
        self.import_generator = OracleNeo4jImportGenerator()
        self.graph_model_builder = GraphModelBuilder()
        self.query_builder = QueryBuilder()

        tabs = QTabWidget()
        tabs.addTab(self._metadata_tab(), "Metadata")
        tabs.addTab(self._neo4j_import_tab(), "Neo4j Import")
        tabs.addTab(self._graph_model_tab(), "Graph Model")
        tabs.addTab(self._query_tab(), "Query Builder")
        tabs.addTab(self._validation_tab(), "Validation")
        tabs.addTab(self._logs_tab(), "Logs")

        root = QWidget()
        layout = QVBoxLayout(root)
        layout.addWidget(tabs)
        self.setCentralWidget(root)

    def _metadata_tab(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.addWidget(QLabel("Load CSV/XLSX metadata and normalize TABLE/COLUMN/FK models."))
        return page

    def _neo4j_import_tab(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        buttons = [
            "Install libraries",
            "Generate metadata SQL",
            "Generate schema graph",
            "Generate constraints",
            "Generate import templates",
            "Run constraints",
            "Run imports",
            "Run relationships",
            "Run validations",
            "Clean Neo4j",
            "Test Neo4j connection",
        ]
        row = QHBoxLayout()
        for label in buttons:
            row.addWidget(QPushButton(label))
        layout.addLayout(row)
        return page

    def _graph_model_tab(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.addWidget(QLabel("Generate DbTable/DbColumn/FK_TO/HAS_COLUMN graph model."))
        return page

    def _query_tab(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.addWidget(QLabel("Advanced query builder with FK path resolution and dictionary filters."))
        return page

    def _validation_tab(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.addWidget(QLabel("Validation: FK checks, orphan nodes, relationship stats, path diagnostics."))
        return page

    def _logs_tab(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        self.log_box = QTextEdit()
        self.log_box.setReadOnly(True)
        layout.addWidget(self.log_box)
        return page
