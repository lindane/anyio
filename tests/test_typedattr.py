from __future__ import annotations

from collections.abc import Callable, Mapping
from typing import Any

import pytest

from anyio import TypedAttributeProvider


class DummyAttributeProvider(TypedAttributeProvider):
    def get_dummyattr(self) -> str:
        raise KeyError("foo")

    @property
    def extra_attributes(self) -> Mapping[Any, Callable[[], Any]]:
        return {str: self.get_dummyattr}


def test_typedattr_keyerror() -> None:
    """
    Test that if the extra attribute getter raises KeyError, it won't be confused for a
    missing attribute.

    """
    with pytest.raises(KeyError, match="^'foo'$"):
        DummyAttributeProvider().extra(str)


def test_has_extra_present() -> None:
    """Test that has_extra returns True for an attribute in extra_attributes."""
    assert DummyAttributeProvider().has_extra(str) is True


def test_has_extra_missing() -> None:
    """Test that has_extra returns False for an attribute not in extra_attributes."""
    assert DummyAttributeProvider().has_extra(int) is False


def test_has_extra_empty_provider() -> None:
    """Test that has_extra returns False on a provider with no extra attributes."""
    assert TypedAttributeProvider().has_extra(str) is False
