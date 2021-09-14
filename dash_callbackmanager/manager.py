from dash import Dash
from dash.dependencies import handle_callback_args


class CallbackManager:
    """
    This class takes over the standard dash apps callback registration duties,
    allowing us to collect the callbacks and deliver them to the app when we
    instansiate it.
    """

    def __init__(self, *managers: "CallbackManager"):
        self._callbacks = []
        self._managers = managers

    def callback(self, *args, **kwargs):
        """
        Dash, app.callback are a decorator around a function. We intercept this
        function and store it. Post load of the dash app we register the
        callback functions.
        """
        outputs, inputs, state, prevent_initial_call = handle_callback_args(
            args, kwargs
        )

        def func(function):
            self._callbacks.append(
                {
                    "function": function,
                    "outputs": outputs,
                    "inputs": inputs,
                    "state": state,
                    "kwargs": {"prevent_initial_call": prevent_initial_call},
                }
            )

        return func

    def register_callbacks(self, app: Dash):
        """
        Register the callbacks into the dash application space. You need to
        register the callbacks else they will not be added into the app scope.
        This will mean callbacks cannot be called.
        """
        for callback in self._callbacks:
            func = callback.pop("function")
            outputs, inputs, state, kwargs = (
                callback["outputs"],
                callback["inputs"],
                callback["state"],
                callback["kwargs"],
            )

            app.callback(
                outputs,
                inputs,
                state,
                **kwargs,
            )(func)

        for manager in self._managers:
            manager.register_callbacks(app)
