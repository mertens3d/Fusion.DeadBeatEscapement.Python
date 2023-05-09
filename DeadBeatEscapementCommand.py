from .Handlers.CommandCreatedHandler import CommandCreatedHandler
import adsk.core
import adsk.fusion
import traceback
from .EscapementModel import WheelParameters
#from .DeadBeatEscapementGeometry import DeadBeatEscapementGeometry
from .constants import COMMAND_ID


class DeadBeatEscapementCommand:
    def __init__(self):
        self.app = adsk.core.Application.get()
        self.ui = self.app.userInterface
        self.design = adsk.fusion.Design.cast(self.app.activeProduct)
        self.params = WheelParameters(self.ui)
        #self.geom = DeadBeatEscapementGeometry(self.params)

        self.command = None
        self.executePreview = False

        self.handlers = []

    def start(self):
        try:
            self.command = self.ui.commandDefinitions.itemById(COMMAND_ID)
            if not self.command:
                self.command = self.ui.commandDefinitions.addButtonDefinition(
                    COMMAND_ID, "Dead Beat Escapement", "Creates a dead beat escapement."
                )
            onCommandCreated = CommandCreatedHandler(self)
            self.command.commandCreated.add(onCommandCreated)
            self.handlers.append(onCommandCreated)

        except:
            if self.ui:
                self.ui.messageBox("Failed:\n{}".format(traceback.format_exc()))



