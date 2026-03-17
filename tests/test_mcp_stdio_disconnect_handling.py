import anyio

from opensearch_orchestrator.mcp_server import _is_expected_stdio_disconnect

# ExceptionGroup is a builtin on 3.11+; on 3.10 use the backport.
try:
    ExceptionGroup  # noqa: B018
except NameError:
    from exceptiongroup import ExceptionGroup  # type: ignore[no-redef]


def test_expected_disconnect_group_returns_true() -> None:
    exc = ExceptionGroup(
        "disconnect",
        [
            anyio.BrokenResourceError(),
            anyio.ClosedResourceError(),
            BrokenPipeError(),
        ],
    )
    assert _is_expected_stdio_disconnect(exc)


def test_mixed_group_with_unexpected_exception_returns_false() -> None:
    exc = ExceptionGroup(
        "mixed",
        [
            anyio.BrokenResourceError(),
            RuntimeError("unexpected"),
        ],
    )
    assert not _is_expected_stdio_disconnect(exc)


def test_nested_disconnect_group_returns_true() -> None:
    exc = ExceptionGroup(
        "outer",
        [
            ExceptionGroup(
                "inner",
                [
                    anyio.BrokenResourceError(),
                    EOFError(),
                ],
            ),
        ],
    )
    assert _is_expected_stdio_disconnect(exc)
