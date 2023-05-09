
# Define the event handler for when the command is executed.
import adsk.core
from .CommandExecuteHandler import CommandExecuteHandler
from .CommandDestroyHandler import CommandDestroyHandler
from ..constants import *
from ..globals import *
import traceback


class CommandCreatedHandler(adsk.core.CommandCreatedEventHandler):
    def __init__(self, handlers):
        super().__init__()
        self.handlers = handlers

    def notify(self, args):
        try:
            cmd = args.command
            cmd.isRepeatable = False
            app = adsk.core.Application.get()
            ui = app.userInterface

            onExecute = CommandExecuteHandler()
            cmd.execute.add(onExecute)
            onExecutePreview = CommandExecuteHandler()
            cmd.executePreview.add(onExecutePreview)
            onDestroy = CommandDestroyHandler()
            cmd.destroy.add(onDestroy)

            self.handlers.append(onExecute)

            # app = adsk.core.Application.get()
            # ui = app.userInterface

            cmd.isRepeatable = False

            inputs = cmd.commandInputs
            inputs.addStringValueInput(
                MODEL_NAME_INPUT_ID, MODEL_NAME_FIELD_TITLE, MODEL_NAME_DEFAULT)

            inputs.addStringValueInput(
                WHEEL_TEETH_COUNT_INPUT_ID, WHEEL_TEETH_COUNT_FIELD_TITLE, WHEEL_TEETH_COUNT_DEFAULT)

            initNotUsedA = adsk.core.ValueInput.createByReal(
                WHEEL_TOOTH_DEPTH_DEFAULT)
            inputs.addValueInput(
                WHEEL_TOOTH_DEPTH_INPUT_ID, NOT_USED_A_FIELD_TITLE, 'in', initNotUsedA)

            initPitchRadius = adsk.core.ValueInput.createByReal(
                inchToReal(WHEEL_TIP_RADIUS_INCH_DEFAULT))
            inputs.addValueInput(
                TIP_RADIUS_INPUT_ID, WHEEL_TIP_RADIUS_FIELD_TITLE, 'in', initPitchRadius)

            initWheelThickness = adsk.core.ValueInput.createByReal(
                inchToReal(WHEEL_THICKNESS_INCH_DEFAULT))
            inputs.addValueInput(
                WHEEL_THICKNESS_INPUT_ID, WHEEL_THICKNESS_FIELD_TITLE, 'in', initWheelThickness)

        except:
            if ui:
                ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
