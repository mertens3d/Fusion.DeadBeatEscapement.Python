import adsk.core


import traceback


class CommandDestroyHandler(adsk.core.CommandEventHandler):
    def __init__(self):
        super().__init__()

    def notify(self, args):
        try:
            self.inputs.clear_all_widgets()

        except:
            if self.ui:
                self.ui.messageBox(
                    "Failed:\n{}".format(traceback.format_exc()))