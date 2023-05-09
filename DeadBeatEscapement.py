import adsk.core
import adsk.fusion
import adsk.cam, traceback
from .EscapementModel import WheelParameters
from .Handlers.CommandCreatedHandler import CommandCreatedHandler
from.Handlers.CommandExecuteHandler import CommandExecuteHandler
from .DeadBeatEscapementCommand import DeadBeatEscapementCommand
from .DeadBeatEscapementUI import DeadBeatEscapementUI
from .constants import *
from .globals import *

def run(context):
    ui = None
    try:
        product = app.activeProduct
        design = adsk.fusion.Design.cast(product)
        ui = app.userInterface

        if not design:
            ui.messageBox('It is not support in the current workspace, please change to MODEL workspace and try again')
            return

        
        cmdDef = ui.commandDefinitions.itemById(COMMAND_ID)

        if not cmdDef:
            cmdDef = ui.commandDefinitions.addButtonDefinition(
                COMMAND_ID,
                COMMAND_DEFINITION,
                COMMAND_TOOLTIP,
                COMMAND_RESOURCEFOLDER
            )

        onCommandCreated = CommandCreatedHandler(handlers)
        cmdDef.commandCreated.add(onCommandCreated)
        handlers.append(onCommandCreated)
        inputs = adsk.core.NamedValues.create()
        cmdDef.execute(inputs)
        #adsk.autoTerminate(False)
    except Exception as e:
        if ui:
            #ui.messageBox('Failed.' + str(e))
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
