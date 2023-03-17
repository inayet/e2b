from typing import List, Any, Tuple

from session.env import EnvVar
from codegen.tools.playground.mock.request import MockRequestFactory

from ....session.playground import NodeJSPlayground
from .tools.filesystem import create_filesystem_tools
from .tools.process import create_process_tools
from .tools.code import create_code_tools


def create_playground_tools(
    envs: List[EnvVar],
    method: str,
    route: str,
    request_body_template: str | None,
) -> Tuple[List[Any], NodeJSPlayground]:
    playground = NodeJSPlayground(envs)

    mock = MockRequestFactory(
        method=method,
        route=route,
        body_template=request_body_template,
        playground=playground,
    )

    subtools = [
        tool
        for tools in (
            tool_factory(playground=playground, mock=mock)
            for tool_factory in [
                # create_filesystem_tools,
                # create_process_tools,
                create_code_tools,
            ]
        )
        for tool in tools
    ]
    return subtools, playground
