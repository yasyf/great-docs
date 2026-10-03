import sys
from pathlib import Path

import pytest

from great_docs import GreatDocs


@pytest.mark.parametrize("dynamic", [False, True])
def test_categorization_honors_dynamic_config(tmp_path: Path, monkeypatch, dynamic: bool):
    package_name = f"gd_category_{str(dynamic).lower()}"
    package_dir = tmp_path / package_name
    package_dir.mkdir()
    (package_dir / "__init__.py").write_text(
        'from pathlib import Path\n'
        'Path(__file__).with_name("imported").write_text("loaded")\n'
        'class Widget:\n'
        '    def run(self):\n'
        '        return 42\n'
    )
    (tmp_path / "great-docs.yml").write_text(f"dynamic: {str(dynamic).lower()}\n")
    monkeypatch.syspath_prepend(str(tmp_path))
    try:
        docs = GreatDocs(project_path=tmp_path)
        categories = docs._categorize_api_objects(package_name, ["Widget"])
        assert categories["class_method_names"]["Widget"] == ["run"]
        assert (package_dir / "imported").exists() is dynamic
    finally:
        sys.modules.pop(package_name, None)
