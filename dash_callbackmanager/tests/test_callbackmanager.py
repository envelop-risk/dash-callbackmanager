from unittest import TestCase

from dash import Dash, Output, Input, State

from ..manager import CallbackManager


class TestCallbackManager(TestCase):
    def setUp(self):
        self.manager = CallbackManager()

        # test callback using manager
        @self.manager.callback(
            Output("test-output", "children"),
            Input("input-1", "value"),
            Input("input-2", "value"),
            State("state-data", ""),
        )
        def test_function():
            pass

    def test_callback_add(self):
        self.assertEqual(len(self.manager._callbacks), 1)

    def test_register(self):
        # server false defers loading of app server.
        app = Dash(name="test", server=False)
        self.manager.register_callbacks(app)

        self.assertEqual(len(app.callback_map), 1)

        callback = app.callback_map["test-output.children"]
        self.assertEqual(
            callback["inputs"],
            [
                {"id": "input-1", "property": "value"},
                {"id": "input-2", "property": "value"},
            ],
        )
        self.assertListEqual(
            callback["state"],
            [
                {
                    "id": "test-state",
                    "property": "children",
                }
            ],
        )
