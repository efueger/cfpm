from cfpm import console
from click.testing import CliRunner


def test_version():
    runner = CliRunner()
    result = runner.invoke(console.cli, ["-v", "DEBUG", "version"])
    assert result.exit_code == 0
    assert "cfpm version " in result.output
