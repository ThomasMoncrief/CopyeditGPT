from typing import Any

from langsmith.run_helpers import RunTypeEnum, trace


class APIWrapper:
    """
    APIWrapper is a class that wraps around any module (specifically designed for openai and anthropic)
    and intercepts function calls, providing automatic logging using the trace context manager.
    """

    __slots__ = ["_wrapped_module", "__weakref__", "_wrapped_name", "_provider_type"]

    def __init__(
        self, wrapped_module: Any, wrapped_name: str = "", provider_type: str = "openai"
    ):
        """
        Initialize the APIWrapper.
        Args:
            wrapped_module: The module that this class will wrap around.
            wrapped_name: The name of the function that is being wrapped.
            provider_type: The provider of the API, default is "openai".
        """
        self._wrapped_module = wrapped_module
        self._wrapped_name = wrapped_name
        self._provider_type = provider_type

    def __getattr__(self, attr_name: str) -> Any:
        """
        Get attribute from the wrapped module. If the attribute is callable, return a wrapped version of it.
        Args:
            attr_name: The name of the attribute.
        Returns:
            The attribute itself or a wrapped version of it if it's callable.
        """
        attr = getattr(self._wrapped_module, attr_name)
        if callable(attr):
            return APIWrapper(
                attr, f"{self._wrapped_name}.{attr_name}", self._provider_type
            )
        else:
            return attr

    def __call__(self, *args, **kwargs) -> Any:
        """
        Call the wrapped function and log the call.
        Args:
            *args: Positional arguments to pass to the function.
            **kwargs: Keyword arguments to pass to the function.
        Returns:
            The return value of the function call.
        """
        with trace(
            self._wrapped_name, RunTypeEnum.llm, inputs={"args": args, "kwargs": kwargs}
        ) as run:
            result = self._wrapped_module(*args, **kwargs)
            run.outputs = {"output": result}
            return result
