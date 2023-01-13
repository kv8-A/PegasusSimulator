#!/usr/bin/env python
import carb
import omni.ui as ui

from pegasus_isaac.ui.ui_delegate import UIDelegate
from pegasus_isaac.params import ROBOTS, SIMULATION_ENVIRONMENTS, THUMBNAIL, WORLD_THUMBNAIL

class WidgetWindow:

    # Design constants for the widgets
    LABEL_PADDING = 120
    BUTTON_HEIGHT = 50
    GENERAL_SPACING = 5

    WINDOW_WIDTH=450
    WINDOW_HEIGHT=800

    def __init__(self, delegate: UIDelegate):
        """
        Constructor for the Window UI widget of the extension. Receives as input a UIDelegate that implements
        all the callbacks to handle button clicks, drop-down menu actions, etc. (abstracting the interface between
        the logic of the code and the ui)
        """

        self._window = None
        self._delegate = delegate

    def shutdown(self):
        """Should be called when the extesion is unloaded"""
        # --------------------
        # According to NVidia:
        # --------------------
        # Unfortunatley, the member variables are not destroyed when the extension is unloaded. We need to do it
        # automatically. Usually, it's OK because the Python garbage collector will eventually destroy everythigng. But
        # we need the images to be destroyed right now because Kit know nothing about Python garbage collector and it
        # will fire warning that texture is not destroyed.
        self._window = None

    def build_window(self):

        self._window = ui.Window("Pegasus Simulation", width=WidgetWindow.WINDOW_WIDTH, height=WidgetWindow.WINDOW_HEIGHT, visible=True)
        self._window.deferred_dock_in("Property", ui.DockPolicy.CURRENT_WINDOW_IS_ACTIVE)
        self._window.setPosition(0.0, 0.0)

        carb.log_warn("drawing")
        
        # Define the UI of the widget window
        with self._window.frame:

            # Vertical Stack of menus
            with ui.VStack():
            
                # Create a frame for selecting which scene to load
                self._scene_selection_frame()
                ui.Spacer(height=5)

                # Create a frame for selecting which vehicle to load in the simulation environment
                self._robot_selection_frame()
                ui.Spacer(height=5)
                
                # Create a frame for selecting the camera position, and what it should point torwards to
                self._viewport_camera_frame()
                ui.Spacer()

                
    def _scene_selection_frame(self):
        """
        Method that implements a dropdown menu with the list of available simulation environemts for the vehicle
        """

        # Frame for selecting the simulation environment to load
        with ui.CollapsableFrame("Scene Selection"):
            with ui.VStack(height=0, spacing=10, name="frame_v_stack"):
                ui.Spacer(height=WidgetWindow.GENERAL_SPACING)

                # Iterate over all existing pre-made worlds bundled with this extension
                with ui.HStack():
                    ui.Label("World Assets", width=WidgetWindow.LABEL_PADDING, height=10.0)

                    # Combo box with the available environments to select from
                    dropdown_menu = ui.ComboBox(0, height=10, name="environments")
                    for environment in SIMULATION_ENVIRONMENTS:
                        dropdown_menu.model.append_child_item(None, ui.SimpleStringModel(environment))

                    # Allow the delegate to know which option was selected in the dropdown menu
                    self._delegate.set_scene_dropdown(dropdown_menu.model)

                ui.Spacer(height=0)

                with ui.HStack():
                    
                    # Add a thumbnail image to have a preview of the world that is about to be loaded
                    with ui.ZStack(width=WidgetWindow.LABEL_PADDING, height=WidgetWindow.BUTTON_HEIGHT*2):
                        ui.Rectangle()
                        ui.Image(WORLD_THUMBNAIL, fill_policy=ui.FillPolicy.PRESERVE_ASPECT_FIT, alignment=ui.Alignment.LEFT_CENTER)

                    ui.Spacer(width=WidgetWindow.GENERAL_SPACING)

                    with ui.VStack():
                        # Button for loading a desired scene
                        ui.Button("Load Scene", height=WidgetWindow.BUTTON_HEIGHT, clicked_fn=self._delegate.on_load_scene)

                        # Button to reset the stage
                        ui.Button("Clear Scene", height=WidgetWindow.BUTTON_HEIGHT, clicked_fn=self._delegate.on_clear_scene)

    def _robot_selection_frame(self):
        """
        Method that implements a frame that allows the user to choose which robot that is about to be spawned
        """

        # Frame for selecting the vehicle to load
        with ui.CollapsableFrame(title="Vehicle Selection"):
            with ui.VStack(height=0, spacing=10, name="frame_v_stack"):
                ui.Spacer(height=WidgetWindow.GENERAL_SPACING)
                # Iterate over all existing robots in the extension
                with ui.HStack():
                    ui.Label("Vehicle Model", name="label", width=WidgetWindow.LABEL_PADDING)
                    
                    # Combo box with the available vehicles to select from
                    dropdown_menu = ui.ComboBox(0, height=10, name="robots")
                    for robot in ROBOTS:
                        dropdown_menu.model.append_child_item(None, ui.SimpleStringModel(robot))  
                    self._delegate.set_vehicle_dropdown(dropdown_menu.model)

                # Add a frame transform to select the position of where to place the selected robot in the world
                self._transform_frame()

                ui.Label("Streaming Backend")
                
                with ui.HStack():
                    # Add a thumbnail image to have a preview of the world that is about to be loaded
                    with ui.ZStack(width=WidgetWindow.LABEL_PADDING, height=WidgetWindow.BUTTON_HEIGHT*2):
                        ui.Rectangle()
                        ui.Image(THUMBNAIL, fill_policy=ui.FillPolicy.PRESERVE_ASPECT_FIT, alignment=ui.Alignment.LEFT_CENTER)

                    ui.Spacer(width=WidgetWindow.GENERAL_SPACING)
                    with ui.VStack():
                        ui.Button("PX4 + ROS 2", height=WidgetWindow.BUTTON_HEIGHT)
                        ui.Button("ROS 2 (Only)", height=WidgetWindow.BUTTON_HEIGHT)

                # Button to load the drone
                ui.Button("Load Vehicle", height=WidgetWindow.BUTTON_HEIGHT, clicked_fn=self._delegate.on_load_vehicle)


    def _viewport_camera_frame(self):
        """
        Method that implements a frame that allows the user to choose what is the viewport camera pose easily
        """

        all_axis=["X", "Y", "Z"]
        colors={"X": 0xFF5555AA, "Y": 0xFF76A371, "Z": 0xFFA07D4F}
        components=["Position"]

        # Frame for setting the camera to visualize the vehicle in the simulator viewport
        with ui.CollapsableFrame("Viewport Camera"):

            with ui.VStack(spacing=8):

                ui.Spacer(height=0)

                # Iterate over the position and rotation menus
                with ui.HStack():
                    with ui.HStack():
                        ui.Label("Position", name="transform", width=50, height=20)
                        ui.Spacer()
                    # Fields X, Y and Z
                    for axis in all_axis:
                        with ui.HStack():
                            with ui.ZStack(width=15):
                                ui.Rectangle(width=15, height=20, style={"background_color": colors[axis], "border_radius": 3, "corner_flag": ui.CornerFlag.LEFT})
                                ui.Label(axis, height=20, name="transform_label", alignment=ui.Alignment.CENTER)
                            ui.FloatDrag(name="transform", min=-1000000, max=1000000, step=0.01)
                            ui.Circle(name="transform", width=20, height=20, radius=3.5, size_policy=ui.CircleSizePolicy.FIXED)

                # Button to set the camera view
                ui.Button("Set Camera Pose", height=WidgetWindow.BUTTON_HEIGHT, clicked_fn=self._delegate.on_set_viewport_camera) 
                ui.Spacer()

    def _transform_frame(self):
        """
        Method that implements a transform frame to translate and rotate an object that is about to be spawned
        """

        components=["Position", "Rotation"]
        all_axis=["X", "Y", "Z"]
        colors={"X": 0xFF5555AA, "Y": 0xFF76A371, "Z": 0xFFA07D4F}

        with ui.CollapsableFrame("Position and Orientation"):
            with ui.VStack(spacing=8):

                ui.Spacer(height=0)

                # Iterate over the position and rotation menus
                for component in components:
                    with ui.HStack():
                        with ui.HStack():
                            ui.Label(component, name="transform", width=50)
                            ui.Spacer()
                        # Fields X, Y and Z
                        for axis in all_axis:
                            with ui.HStack():
                                with ui.ZStack(width=15):
                                    ui.Rectangle(width=15, height=20, style={"background_color": colors[axis], "border_radius": 3, "corner_flag": ui.CornerFlag.LEFT})
                                    ui.Label(axis, name="transform_label", alignment=ui.Alignment.CENTER)
                                if component == "Position":
                                    ui.FloatDrag(name="transform", min=-1000000, max=1000000, step=0.01)
                                else:
                                    ui.FloatDrag(name="transform", min=-180.0, max=180.0, step=0.01)
                                ui.Circle(name="transform", width=20, radius=3.5, size_policy=ui.CircleSizePolicy.FIXED)
                ui.Spacer(height=0)
