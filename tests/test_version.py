from cfpm import console
from click.testing import CliRunner


def test_version():
    runner = CliRunner()
    result = runner.invoke(console.cli, ["version", "-c"])
    assert result.exit_code == 0
    assert "cfpm version " in result.output


def test_debug():
    runner = CliRunner()
    result = runner.invoke(
        console.cli, ["version"], env={"CFPM_VERBOSITY": "DEBUG"}
    )
    assert result.exit_code == 0
    assert "DEBUG" in result.output
