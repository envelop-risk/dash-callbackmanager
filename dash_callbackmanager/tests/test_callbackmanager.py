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
                    "id": "state-data",
                    "property": "",
                }
            ],
        )

    def test_sub_managers(self):
        app = Dash(name="test", server=False)
        manager1 = CallbackManager()

        @manager1.callback(Output("manager1", "value"))
        def func1():
            ...

        manager2 = CallbackManager()

        @manager2.callback(Output("manager2", "value"))
        def func2():
            ...

        base_manager = CallbackManager(manager1, manager2)

        @base_manager.callback(Output("base_manager", "test"))
        def base_func():
            ...

        base_manager.register_callbacks(app)

        self.assertEqual(len(app.callback_map), 3)
        self.assertListEqual(list(app.callback_map.keys()), [
            "base_manager.test",
            "manager1.value",
            "manager2.value",
        ])