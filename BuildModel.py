
            # Get the values from the parameters object
            angle = parameters.angle
            pallet_width = parameters.pallet_width
            pallet_depth = parameters.pallet_depth
            tooth_width = parameters.tooth_width
            tooth_height = parameters.tooth_height
            escape_wheel_teeth = parameters.escape_wheel_teeth
            wheel_radius = parameters.wheel_radius
            pallet_offset = parameters.pallet_offset
            drop_angle = parameters.drop_angle

            # Create a new sketch.
            sketches = design.rootComponent.sketches
            xzPlane = design.rootComponent.xZConstructionPlane
            sketch = sketches.add(xzPlane)

            # Draw the escape wheel.
            escape_wheel = sketch.sketchCurves.sketchCircles.addByCenterRadius(
                adsk.core.Point3D.create(0, 0, 0), wheel_radius)
            for i in range(escape_wheel_teeth):
                angle_degrees = (360 / escape_wheel_teeth) * i
                angle_radians = angle_degrees * (3.14159 / 180)
                x = wheel_radius * adsk.core.math.cos(angle_radians)
                y = wheel_radius * adsk.core.math.sin(angle_radians)
                escape_wheel.sketchArcs.addByCenterStartSweep(adsk.core.Point3D.create(
                    0, 0, 0), adsk.core.Point3D.create(x, y, 0), 2*3.14159 / (escape_wheel_teeth * 4))

            # Draw the pallet fork.
            pallet_fork = sketch.sketchCurves.sketchLines.addByTwoPoints(
                adsk.core.Point3D.create(-pallet_width / 2, 0, 0), adsk.core.Point3D.create(pallet_width / 2, 0, 0))
            pallet_fork_sketch_lines = sketch.sketchCurves.sketchLines
            pallet_fork_sketch_lines.addByTwoPoints(adsk.core.Point3D.create(
                -pallet_width / 2, 0, 0), adsk.core.Point3D.create(-pallet_width / 2, -pallet_depth, 0))
            pallet_fork_sketch_lines.addByTwoPoints(adsk.core.Point3D.create(
                pallet_width / 2, 0, 0), adsk.core.Point3D.create(pallet_width / 2, -pallet_depth, 0))

            # Create a new component and add the pallet fork.
            component = design.rootComponent.occurrences.addNewComponent(
                adsk.core.Matrix3D.create())
            component.name = 'Pallet Fork'
            body = component.bRepBodies.add()
            body.createFromSketch(sketch.profiles.item(
                2), adsk.fusion.tProfileOrientationType.tOppositeOrientation)

            # Move the pallet fork to the correct position.