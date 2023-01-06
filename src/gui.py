import sys

import PySimpleGUI as sg


class Gui:
    def __init__(self, title, layout, event_handler, debug=False, exit_program_on_exit_event=True, **kwargs):
        self.event_handler = event_handler
        self.event_handler.register_handler(self.close, sg.WIN_CLOSED, "-EXIT-", "WIN_CLOSED")
        self.exit_program_on_exit_event = exit_program_on_exit_event
        self.debug = debug


        # no_titlebar = kwargs.get("window_no_titlebar", False)
        # grab_anywhere = kwargs.get("window_grab_anywhere", False)
        # return_keyboard_events = kwargs.get("window_return_keyboard_events", False)

        layout[-1].append(sg.T(key="-ERROR-"))

        self.window = sg.Window(
            title,
            layout,
            resizable=True,
            finalize=True,
            **kwargs
        )

    def new_handler(self, handler, *events):
        self.event_handler.register_handler(handler, *events)

    def run(self):
        ret = None
        
        event, values = self.window.read()
        if self.debug:
            print(event, values)

        if event in self.event_handler.handlers:
            try:
                ret = self.event_handler.handle_event(event)(values)
            except Exception as e:
                self.window["-ERROR-"].update(e)
                raise e

        if not ret is None:
            return ret

    def close(self, *_):
        """Close the window and exit the program. 
        """

        self.window.close()
        if self.exit_program_on_exit_event: 
            sys.exit()

        # Set run to false
        return False