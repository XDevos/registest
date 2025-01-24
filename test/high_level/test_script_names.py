import subprocess

import pytest

# List of script names to test
SCRIPT_NAMES = ["registest", "regis_transform", "regis_register", "regis_compare"]


@pytest.mark.parametrize("script_name", SCRIPT_NAMES)
def test_script_execution(script_name):
    """
    Test if each script can be executed in the terminal without errors.
    It runs the script with `--help` to check if it provides usage information.
    """
    try:
        result = subprocess.run(
            [script_name, "--help"],  # Using --help to avoid modifying data
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
        )

        # Verify that the output contains "Usage" or similar help instructions
        assert "Usage" in result.stdout or "usage" in result.stdout.lower()

    except subprocess.CalledProcessError as e:
        pytest.fail(f"Execution of {script_name} failed: {e.stderr}")


def test_all_scripts_exist():
    """
    Ensure that all script names are available as commands in the terminal.
    Uses `which` command to verify that the script exists in the system's PATH.
    """
    for script in SCRIPT_NAMES:
        result = subprocess.run(["which", script], stdout=subprocess.PIPE, text=True)
        assert result.stdout.strip(), f"Script '{script}' not found in PATH"
