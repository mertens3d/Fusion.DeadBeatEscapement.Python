import adsk.core
import adsk.fusion
import adsk.cam
import traceback
from ..EscapementModel import WheelParameters
from ..constants import *
from ..ModelWheelBuilder import ModelWheelBuilder
from ..globals import *


class CommandExecuteHandler(adsk.core.CommandEventHandler):
    def __init__(self):
        super().__init__()

    def notify(self, args):
        try:
            design = app.activeProduct
            if not design:
                ui.messageBox('No active Fusion 360 design', 'No Design')
                return

            command = args.firingEvent.sender
            inputs = command.commandInputs

            escapementParameters = WheelParameters()

            for input in inputs:
                if input.id == MODEL_NAME_INPUT_ID:
                    escapementParameters.modelName = input.value
                elif input.id == WHEEL_TEETH_COUNT_INPUT_ID:
                    escapementParameters.toothCount_int = int(input.value)
                #elif input.id == WHEEL_RADIUS_INPUT_ID:
                 #   escapementParameters.wheelRadius_inch = input.value
                elif input.id == TIP_RADIUS_INPUT_ID:
                    escapementParameters.tipRadius_real = input.value

            wheelBuilder = ModelWheelBuilder(escapementParameters)
            wheelBuilder.buildWheelModel(escapementParameters)

            args.isValidResult = True

        except:
            if ui:
                ui.messageBox("Failed:\n{}".format(traceback.format_exc()))
