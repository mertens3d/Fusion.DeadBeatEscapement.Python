import adsk.core
import adsk.fusion
import math
# global set of event handlers to keep them referenced for the duration of the command
handlers = []
app = adsk.core.Application.get()

if app:
    ui = app.userInterface
    __design = adsk.fusion.Design.cast(app.activeProduct)
    unitsMgr = __design.unitsManager
newComp = None


def inchToReal(value_inch):
    value_cm = value_inch * 2.54
    # if ui:
    # ui.messageBox("inchValue: " + str(inchValue))
    # ui.messageBox("metricValue: " + str(metricValue))
    return value_cm


def createNewComponent():
    product = app.activeProduct
    design = adsk.fusion.Design.cast(product)
    rootComp = design.rootComponent
    allOccs = rootComp.occurrences
    newOcc = allOccs.addNewComponent(adsk.core.Matrix3D.create())
    return newOcc.component


def degreesToRadians(angleDegrees):
    angle_radians = angleDegrees * (math.pi / 180)
    return angle_radians

       