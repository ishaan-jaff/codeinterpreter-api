import asyncio

from codeinterpreterapi import CodeInterpreterSession, File

def run_sync(session: CodeInterpreterSession) -> bool:
    try:
        assert session.start() == "started"

        assert (
            "3.1"
            in session.generate_response_sync(
                "Compute pi using Monte Carlo simulation in Python and show me the result."
            ).content
        )

        assert (
            ".xlsx"
            in session.generate_response_sync(
                "Convert this csv file to excel.",
                files=[File.from_path("examples/assets/iris.csv")],
            )
            .files[0]
            .name
        )

    finally:
        assert session.stop() == "stopped"

    return True


def test_codebox():
    session = CodeInterpreterSession()
    assert run_sync(session), "Failed to run sync CodeInterpreterSession remotely"
    assert asyncio.run(
        run_async(session)
    ), "Failed to run async CodeInterpreterSession remotely"

def test_localbox():
    session = CodeInterpreterSession(local=True)
    assert run_sync(session), "Failed to run sync CodeInterpreterSession locally"
    assert asyncio.run(
        run_async(session)
    ), "Failed to run async CodeInterpreterSession locally"

async def run_async(session: CodeInterpreterSession) -> bool:
    try:
        assert (await session.astart()) == "started"

        assert (
            "3.1"
            in (
                await session.agenerate_response(
                    "Compute pi using Monte Carlo simulation in Python and show me the result."
                )
            ).content
        )

        assert (
            ".xlsx"
            in (
                await session.agenerate_response(
                    "Convert this csv file to excel.",
                    files=[File.from_path("examples/assets/iris.csv")],
                )
            )
            .files[0]
            .name
        )

    finally:
        assert await session.astop() == "stopped"

    return True


if __name__ == "__main__":
    test_codebox()
    test_localbox()
