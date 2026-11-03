"""Validate notebook structure and cell syntax without executing experiments."""
import ast
from pathlib import Path
import json

root = Path(__file__).resolve().parents[1]
path = root / 'notebooks' / 'Smart_Energy_Planner.ipynb'
notebook = json.loads(path.read_text())
assert notebook['nbformat'] == 4
assert isinstance(notebook['metadata'], dict)
assert isinstance(notebook['cells'], list)
count = 0
magic_count = 0
for index, cell in enumerate(notebook['cells']):
    assert cell['cell_type'] in {'code', 'markdown', 'raw'}
    assert isinstance(cell['metadata'], dict)
    source = cell['source']
    source = source if isinstance(source, str) else ''.join(source)
    if cell['cell_type'] == 'code':
        assert isinstance(cell['outputs'], list)
        python_lines = []
        for line in source.splitlines():
            if line.lstrip().startswith('%pip install '):
                magic_count += 1
                python_lines.append('# Colab pip installation magic')
            else:
                python_lines.append(line)
        ast.parse('\n'.join(python_lines), filename=f'cell_{index}')
        count += 1
print(f'Checked basic notebook structure and Python syntax of {count} code cells; '
      f'{magic_count} pip magic lines excluded. No experiments executed. '
      'This is not full nbformat schema validation.')
