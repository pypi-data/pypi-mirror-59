"""Test the doctr-versions-menu CLI interface."""
import json
import subprocess
from distutils.dir_util import copy_tree
from pathlib import Path

from click.testing import CliRunner
from pkg_resources import parse_version

import doctr_versions_menu
from doctr_versions_menu.cli import main as doctr_versions_menu_command


def test_version():
    """Test ``doctr-versions-menu --version``."""
    runner = CliRunner()
    result = runner.invoke(doctr_versions_menu_command, ['--version'])
    assert result.exit_code == 0
    normalized_version = str(parse_version(doctr_versions_menu.__version__))
    assert normalized_version in result.output


def test_default_run():
    """Test doctr-versions-menu "default" run."""
    root = Path(__file__).with_suffix('') / 'gh_pages_default'
    runner = CliRunner()
    with runner.isolated_filesystem():
        cwd = Path.cwd()
        subprocess.run(['git', 'init'], check=True)
        copy_tree(str(root), str(cwd))
        result = runner.invoke(doctr_versions_menu_command)
        assert result.exit_code == 0
        assert (cwd / 'index.html').is_file()
        assert (cwd / '.nojekyll').is_file()
        assert (cwd / 'versions.json').is_file()
        with (cwd / 'versions.json').open() as versions_json:
            versions_data = json.load(versions_json)
            assert versions_data['folders'] == ['master', 'v0.1.0', 'v1.0.0']
            assert versions_data['labels'] == {
                'master': 'master (dev)',
                'v0.1.0': 'v0.1.0',
                'v1.0.0': 'v1.0.0 (latest release)',
            }
            assert 'v0.1.0' in versions_data['outdated']
            assert versions_data['latest_release'] == 'v1.0.0'
            assert versions_data['downloads']['master'] == [
                ['pdf', '/master/master.pdf'],
                ['zip', '/master/master.zip'],
                ['epub', '/master/master.epub'],
            ]
            assert versions_data['downloads']['v1.0.0'] == [
                ['pdf', 'https://host/v1.0.0/v1.0.0.pdf'],
                ['html', 'https://host/v1.0.0/v1.0.0.zip'],
                ['epub', 'https://host/v1.0.0/v1.0.0.epub'],
            ]


def test_custm_index_html():
    """Test using a custom index.html."""
    root = Path(__file__).with_suffix('') / 'gh_pages_custom_index'
    runner = CliRunner()
    with runner.isolated_filesystem():
        cwd = Path.cwd()
        subprocess.run(['git', 'init'], check=True)
        copy_tree(str(root), str(cwd))
        result = runner.invoke(doctr_versions_menu_command)
        assert result.exit_code == 0
        assert (cwd / 'index.html').is_file()
        assert (cwd / '.nojekyll').is_file()
        assert (cwd / 'versions.json').is_file()
        msg = "This is the index.html for the gh_pages_custom_index test."
        assert msg in (cwd / 'index.html').read_text()
