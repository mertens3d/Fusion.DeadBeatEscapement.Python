import adsk.core


import traceback


class DeadBeatEscapementCommandInputChangedHandler(adsk.core.InputChangedEventHandler):
    def __init__(self, inputs):
        super().__init__()
        self.inputs = inputs

    def notify(self, args):
        try:
            cmdInput = args.input
            if cmdInput.id == "escapementType":
                self.inputs.show_hide_widgets()

        except:
            if self.ui:
                self.ui.messageBox(
                    "Failed:\n{}".format(traceback.format_exc()))