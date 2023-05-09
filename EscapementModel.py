import math
from .constants import *
from .globals import *


class EscapmentParameters:
    def __init__(self):
        self.escapement_pin_diameter = None
        self.Wheel = WheelParameters()


class ForkParameters:
    def __init__(self):
        self.anchorDistance_inch = ANCHOR_DISTANCE_INCH_DEFAULT
        self.pallet_offset = PALLET_OFFSET_INCH_DEFAULT


class WheelParameters:
    def __init__(self):
        self.modelName = MODEL_NAME_DEFAULT
        self.notUsedA_inch = WHEEL_TOOTH_DEPTH_DEFAULT
        self.tipRadius_real = 0.5
        self.angle_offset = None
        self.toothCount_int = int(WHEEL_TEETH_COUNT_DEFAULT)
        self.bodyThickness_inch = BODY_THICKNESS_INCH_DEFAULT
        self.addendum_real = 0.0
        self.wheelToothDepth = WHEEL_TEETH_COUNT_DEFAULT
        self.trailingAngle_Degrees = 18.5
        # calculated

    # @property
    # def pitchRadius_internal(self):
        # return inchToCM(self.pitchRadius_internal)

    @property
    def RootRadius_real(self):
        return self.tipRadius_real - (self.wheelToothDepth)

    #@property
    #def wheelRadiusOuter_real(self):
        #return self.pitchRadius_real + self.addendum_real

    @property
    def circleOuterCircumference_real(self):
        return 2 * math.pi * self.wheelRadiusOuter_real

    @property
    def toothSpan_real(self):
        return self.circleOuterCircumference_real / self.toothCount_int

    @property
    def bodyThickness_cm(self):
        return inchToReal(self.bodyThickness_inch)

    @property
    def trailingAngle_radians(self):
        # angleDegrees =
        # degreesToRadians(angleDegrees)
        #angleRadians = 2 * math.pi / self.toothCount_int
        
        return degreesToRadians(self.trailingAngle_Degrees)

    @property
    def bodyWidth_cm(self):
        return self.bodyThickness_cm / math.sin(self.trailingAngle_radians / 2)
