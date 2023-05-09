import adsk.core, adsk.fusion, traceback

class DeadBeatEscapementUI:

    def __init__(self, command: adsk.core.Command):
        self.command = command

    def on_preview(self, args: adsk.core.CommandEventArgs):
        try:
            pass # placeholder code for now
        except:
            traceback.print_exc()

    def on_input_changed(self, args: adsk.core.InputChangedEventArgs):
        try:
            pass # placeholder code for now
        except:
            traceback.print_exc()

    def on_execute(self, args: adsk.core.CommandEventArgs):
        try:
            pass # placeholder code for now
        except:
            traceback.print_exc()