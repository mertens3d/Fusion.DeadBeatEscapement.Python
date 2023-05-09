import adsk.core
import adsk.fusion
import adsk.cam
import math
from .constants import *
from .globals import *
from .EscapementModel import WheelParameters, EscapmentParameters


class ModelWheelBuilder:
    def __init__(self,  escapementParams: EscapmentParameters):
        super().__init__()
        self.__escapementParams = escapementParams
        self.__wheelCenter = adsk.core.Point3D.create(0, 0, 0)

    def buildTrailingLine(self, currentAngle, sketch):

        aX_cm = self.__escapementParams.Wheel.tipRadius_real * \
            math.cos(currentAngle)
        aY_cm = self.__escapementParams.Wheel.tipRadius_real * \
            math.sin(currentAngle)
        pointA_cm = adsk.core.Point3D.create(aX_cm, aY_cm, 0)

        # create a temporary line
        workingTrailingAngle = degreesToRadians(
            270) - self.__escapementParams.Wheel.trailingAngle_radians
        tempX = 1 * math.cos(workingTrailingAngle)
        tempY = 1 * math.sin(workingTrailingAngle)
        tempPoint = adsk.core.Point3D.create(tempX, tempY, 0)

        tempLine = adsk.core.Line3D.create(pointA_cm, tempPoint)

        tempCurve = adsk.core.Circle2D.createByCenter(
            self.__wheelCenter, self.__escapementParams.Wheel.RootRadius_real)
        intersectionPoints = tempLine.intersectWithCurve(tempCurve)
        # now we should have two points. I think it will always be the closer of the two
        shortestDist = adsk
        if intersectionPoints.count > 0:
            closestPoint = intersectionPoints[0]
            shortestDist = pointA_cm.distanceTo(closestPoint)
            if intersectionPoints.count > 1:
                candidatePoint = intersectionPoints[1]
                candidateDist = pointA_cm.distanceTo(candidatePoint)
                if candidateDist < shortestDist:
                    closestPoint = candidatePoint
        else:
            raise "no intersection found"

        trailingEdgeLine = sketch.sketchCurves.sketchLines.addByTwoPoints(pointA_cm, closestPoint)



        '''dX_cm = (self.__escapementParams.Wheel.tipRadius_real + self.__escapementParams.Wheel.wheelToothDepth) * \
            math.cos(currentAngle +
                     self.__escapementParams.Wheel.trailingAngle_radians)
        dY_cm = (self.__escapementParams.Wheel.tipRadius_real + self.__escapementParams.Wheel.wheelToothDepth) * \
            math.sin(currentAngle +
                     self.__escapementParams.Wheel.trailingAngle_radians)
        endPoint_cm = adsk.core.Point3D.create(dX_cm, dY_cm, 0)
        toothLine = sketch.sketchCurves.sketchLines.addByTwoPoints(
            pointA_cm, endPoint_cm)'''
        return trailingEdgeLine

    def buildBodyLine1(self, currentAngle, targetSketch):
        try:
            startX_cm = self.__escapementParams.Wheel.wheelRadiusOuter_real * \
                math.cos(currentAngle)
            startY_cm = self.__escapementParams.Wheel.wheelRadiusOuter_real * \
                math.sin(currentAngle)
            startPoint_cm = adsk.core.Point3D.create(startX_cm, startY_cm, 0)

            endX_cm = self.__escapementParams.Wheel.RootRadius_real * \
                math.cos(currentAngle)
            endY_cm = self.__escapementParams.Wheel.RootRadius_real * \
                math.sin(currentAngle)
            endPoint_cm = adsk.core.Point3D.create(endX_cm, endY_cm, 0)

            bodyLine1 = targetSketch.sketchCurves.sketchLines.addByTwoPoints(
                startPoint_cm, endPoint_cm)
        except Exception as e:
            if ui:
                ui.messageBox('Failed buildBodyLine1 ' + str(e))

        return bodyLine1

    def buildBodyLine2(self, escapementParameters: WheelParameters, currentAngle, targetSketch):
        try:
            startX_cm = (escapementParameters.tipRadius_real + escapementParameters.wheelToothDepth +
                         escapementParameters.bodyWidth_cm) * math.cos(currentAngle + escapementParameters.trailingAngle_radians)
            startY_cm = (escapementParameters.tipRadius_real + escapementParameters.bodyThickness_cm +
                         escapementParameters.bodyWidth_cm) * math.sin(currentAngle + escapementParameters.trailingAngle_radians)
            startPoint_cm = adsk.core.Point3D.create(startX_cm, startY_cm, 0)

            endX_cm = (escapementParameters.tipRadius_real + escapementParameters.wheelToothDepth) * \
                math.cos(currentAngle +
                         escapementParameters.trailingAngle_radians)
            endY_cm = (escapementParameters.tipRadius_real + escapementParameters.wheelToothDepth) * \
                math.sin(currentAngle +
                         escapementParameters.trailingAngle_radians)
            endPoint_cm = adsk.core.Point3D.create(endX_cm, endY_cm, 0)

            body_line2 = targetSketch.sketchCurves.sketchLines.addByTwoPoints(
                startPoint_cm, endPoint_cm)
        except Exception as e:
            if ui:
                ui.messageBox('Failed buildBodyLine2 ' + str(e))

        return body_line2

    def buildConstructionCircles(self, workingSketch):

        # Create the outer circle
        outer_circle = workingSketch.sketchCurves.sketchCircles.addByCenterRadius(
            adsk.core.Point3D.create(0, 0, 0), self.__escapementParams.Wheel.wheelRadiusOuter_real)

        # Create the inner circle
        inner_circle = workingSketch.sketchCurves.sketchCircles.addByCenterRadius(
            adsk.core.Point3D.create(0, 0, 0), self.__escapementParams.Wheel.RootRadius_real)

        # Convert the circles to construction lines
        inner_circle.isConstruction = True
        outer_circle.isConstruction = True

    def buildWheelModel(self, escapementParameters: WheelParameters):
        try:
            global newComp
            newComp = createNewComponent()
            if newComp is None:
                ui.messageBox('New component failed to create',
                              'New Component Failed')
                return

            # Create a new sketch
            sketches = newComp.sketches
            xyPlane = newComp.xYConstructionPlane
            xzPlane = newComp.xZConstructionPlane
            toothSketch = sketches.add(xyPlane)

            # ui.messageBox('wheel Radius: ' + str(escapementParameters.wheelRadius))

            # Draw the escape wheel.
            # escape_wheel = toothSketch.sketchCurves.sketchCircles.addByCenterRadius(
            # adsk.core.Point3D.create(0, 0, 0), escapementParameters.wheelRadius_inch)

            currentAngle_radians = 0
            for index in range(escapementParameters.toothCount_int):
                # indexAngle_radians = escapementParameters.anglePerTooth_radians * index

                """ x = escapementParameters.wheelRadius_cm * \
                    math.cos(currentAngle_radians)
                y = escapementParameters.wheelRadius_cm * \
                    math.sin(currentAngle_radians)

                # escape_wheel.sketchArcs.addByCenterStartSweep(adsk.core.Point3D.create(
                #  0, 0, 0), adsk.core.Point3D.create(x, y, 0), 2*math.pi / (toothCountInt * 4))
                centerPoint = adsk.core.Point3D.create(0, 0, 0)
                startPoint = adsk.core.Point3D.create(x, y, 0)
                sweepAngle_radians = 2*math.pi / \
                    (escapementParameters.toothCount_int * 4)

                arcs = toothSketch.sketchCurves.sketchArcs
                arc = arcs.addByCenterStartSweep(
                    centerPoint, startPoint, sweepAngle_radians) """

                # toothLine = self.buildToothLine(
                # escapementParameters, currentAngle_radians, toothSketch)
                self.buildConstructionCircles(toothSketch)

                bodyLine1 = self.buildBodyLine1(
                    currentAngle_radians, toothSketch)
                # bodyLine2 = self.buildBodyLine2(
                # escapementParameters, currentAngle_radians, toothSketch)

                # ui.messageBox('bbb')
                """               body_arc = toothSketch.sketchCurves.sketchArcs.addByThreePoints(
                    bodyLine2.endSketchPoint, toothLine.startSketchPoint, bodyLine1.startSketchPoint) """

                currentAngle_radians += escapementParameters.trailingAngle_radians

            """   center = adsk.core.Point3D.create(0, 0, 0)
            vertices = [] """

            """ for index in range(0, 6):
                vertex = adsk.core.Point3D.create(center.x + (escapementParameters.anchor_distance/2) * math.cos(
                    math.pi * index/3), center.y + (escapementParameters.anchor_distance/2) * math.sin(math.pi * index/3), 0)
                vertices.append(vertex)

            for index in range(0, 6):
                sketch.sketchCurves.sketchLines.addByTwoPoints(vertices[(index+1) % 6], vertices[index]) """

            """ extrudes = newComp.features.extrudeFeatures
            prof = toothSketch.profiles[0]
            extInput = extrudes.createInput(
                prof, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)

            distance = adsk.core.ValueInput.createByReal(
                escapementParameters.pallet_offset)
            extInput.setDistanceExtent(False, distance)
            headExt = extrudes.add(extInput)

            fc = headExt.faces[0]
            bd = fc.body
            bd.name = escapementParameters.modelName """

        except Exception as e:
            if ui:
                ui.messageBox('Failed to compute the escapement. ' + str(e))
