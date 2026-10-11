from pathlib import Path
import tomllib


ROOT = Path(__file__).parents[1]


def test_image_and_checkpoint_runner_installation_extras_cover_required_libraries():
    extras = tomllib.loads((ROOT / 'pyproject.toml').read_text())['project']['optional-dependencies']
    expected = {
        'data-space-gpu': {'torch', 'scipy'},
        'post-training-gpu': {'torch', 'transformers', 'datasets', 'safetensors'},
        'multimodal': {'torch', 'transformers', 'Pillow'},
        'sparse-decoding-gpu': {'torch', 'transformers', 'triton'},
        'system-one-gpu': {'torch', 'transformers', 'laya'},
    }
    for extra, required in expected.items():
        names = {entry.split('>=')[0].split('==')[0] for entry in extras[extra]}
        assert required <= names, (extra, required - names)
    guide = (ROOT / 'docs/post-training/oct11-checkpoint-guide.md').read_text()
    for extra in expected:
        assert f'.[{extra}]' in guide
    assert 'gymnasium==1.1.1' in guide
