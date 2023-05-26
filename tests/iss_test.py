#!/usr/bin/env python3
"""Tests for ISS notifier."""
import pytest
import src.iss.main
import src.iss.iss
import src.iss.iss_email


@pytest.mark.parametrize("option", ("-l", "--list"))
def test_people(capsys, option):
    """Test the people aboard the ISS method."""
    src.iss.main.main([option])
    out, err = capsys.readouterr()
    assert "Warren" in out
    assert err == ""
