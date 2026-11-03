# SPDX-FileCopyrightText: Fondation RERO+
# SPDX-License-Identifier: AGPL-3.0-or-later

"""Test cli."""

from os.path import dirname, join

from click.testing import CliRunner

from rero_ils.modules.migrations.data.cli import dedup, get, load, subsets


def test_migrations_cli(app, migration, tmp_path):
    """Test validate cli."""
    runner = CliRunner()
    file_name = join(dirname(__file__), "../../data/migration.xml")
    res = runner.invoke(load, [migration.name, file_name, "-n"])
    assert res.exit_code == 0

    res = runner.invoke(get, [migration.name, "-f", "ids"])
    assert res.output == ""
    assert res.exit_code == 0

    res = runner.invoke(load, [migration.name, file_name])
    assert res.exit_code == 0

    res = runner.invoke(get, [migration.name, "-f", "ids"])
    assert "R003448321" in res.output
    assert res.exit_code == 0

    out_file = tmp_path / "conversion-status.txt"
    res = runner.invoke(get, [migration.name, "-f", "conversion-status", "-o", str(out_file)])
    assert res.exit_code == 0
    assert out_file.read_text().startswith("R003448321\t")

    out_file = tmp_path / "logs.txt"
    res = runner.invoke(get, [migration.name, "-i", "R003448321", "-f", "logs", "-o", str(out_file)])
    assert res.exit_code == 0
    assert out_file.read_text() == "Logs for R003448321\nConversion ok\nFixtures conversions\n"

    res = runner.invoke(dedup, [migration.name, "-n"])
    assert "R003448321" in res.output
    assert "Status" in res.output
    assert res.exit_code == 0

    res = runner.invoke(dedup, [migration.name])
    assert res.exit_code == 0

    res = runner.invoke(subsets, [migration.name, "set1"])
    assert "1 record" in res.output
    assert res.exit_code == 0
