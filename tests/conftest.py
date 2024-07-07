import pytest
import importlib.util
import sys
import os
from pathlib import Path

# Ensure the parent directory of the tests is in the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
print("sys.path:", sys.path)

def pytest_collect_file(parent, file_path):
    if file_path.suffix == ".py" and "spec" in file_path.stem:
        return SpecFile.from_parent(parent, path=file_path)

class SpecFile(pytest.Module):
    def _getobj(self):
        module_name = self.path.stem.replace('.', '_')
        spec = importlib.util.spec_from_file_location(module_name, self.path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        return module

@pytest.hookimpl(tryfirst=True)
def pytest_load_initial_conftests(args, early_config, parser):
    test_dir = Path(__file__).parent.resolve()
    if str(test_dir) not in sys.path:
        sys.path.insert(0, str(test_dir))
