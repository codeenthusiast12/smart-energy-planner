"""Run in the experiment runtime; records versions, never credentials."""
import json
import platform
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

packages = ['qiskit', 'numpy', 'pandas', 'scipy', 'scikit-learn', 'matplotlib', 'ucimlrepo']
versions = {}
for package in packages:
    try:
        versions[package] = version(package)
    except PackageNotFoundError:
        versions[package] = 'not installed'
payload = {'python': platform.python_version(), 'platform': platform.platform(), 'packages': versions}
target = Path('results') / 'runtime_environment.json'
target.parent.mkdir(parents=True, exist_ok=True)
target.write_text(json.dumps(payload, indent=2) + '\n')
print(f'Saved actual runtime versions to {target}')
