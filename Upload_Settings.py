import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from tkinter import filedialog as fd
from datetime import date


class UI(tk.Frame):
    def __init__(self, master, **options):
        tk.Frame.__init__(self, master, **options)

        self.fr_input = InputData(self)
        self.fr_input.grid(row=0, column=0)


class InputData(tk.Frame):
    def __init__(self, master, **options):
        tk.Frame.__init__(self, master, **options)

        self.fr_left = tk.Frame(self)
        self.fr_center = tk.Frame(self)
        self.fr_right = tk.Frame(self)

        self.fr_left.grid(row=0, column=0, sticky=tk.N, padx=5)
        self.fr_center.grid(row=0, column=1, sticky=tk.N, padx=5)
        self.fr_right.grid(row=0, column=2, sticky=tk.N, padx=5)

        self.fr_shot_id = tk.LabelFrame(self.fr_left, text="Shot ID")
        self.fr_artifacts = tk.LabelFrame(self.fr_left, text="Shot Artifacts")
        self.fr_parameters = tk.LabelFrame(self.fr_center, text="Shot Parameters")
        self.fr_metrics = tk.LabelFrame(self.fr_right, text="Shot Metrics")

        self.fr_shot_id.grid(row=0, column=0, sticky=tk.N)
        self.fr_artifacts.grid(row=1, column=0, sticky=tk.N, pady=5)
        self.fr_parameters.grid(row=0, column=0, sticky=tk.N)
        self.fr_metrics.grid(row=0, column=0, sticky=tk.N)

        total_width = 65

        # Remove after testing
        self.btn_test = tk.Button(self.fr_artifacts, text="Test", command=lambda: self.get_settings())
        #self.btn_test.grid(row=3, column=0)

        """ Shot ID """
        self.lbl_exp_name = tk.Label(self.fr_shot_id, text="Experiment Name")
        self.entry_exp_name = tk.Entry(self.fr_shot_id, width=int(2 / 3 * total_width))
        self.lbl_shot_num = tk.Label(self.fr_shot_id, text="Shot Number")
        self.lbl_shot_date = tk.Label(self.fr_shot_id, text="Shot Date")
        self.lbl_shot_time = tk.Label(self.fr_shot_id, text="Shot Time")
        self.entry_shot_num = tk.Entry(self.fr_shot_id, width=int(1 / 3 * total_width))
        self.entry_shot_date = tk.Entry(self.fr_shot_id, width=int(2 / 3 * total_width))
        self.entry_shot_time = tk.Entry(self.fr_shot_id, width=int(1 / 3 * total_width))

        self.lbl_exp_name.grid(row=0, column=0)
        self.lbl_shot_num.grid(row=0, column=1)
        self.entry_exp_name.grid(row=1, column=0)
        self.entry_shot_num.grid(row=1, column=1)

        self.lbl_shot_date.grid(row=2, column=0)
        self.lbl_shot_time.grid(row=2, column=1)
        self.entry_shot_date.grid(row=3, column=0)
        self.entry_shot_time.grid(row=3, column=1)

        """ Shot Parameters """
        # Frame 1: Driver/injector beam energy/spot size, laser contrast, compressor grating position, gas pressure
        self.fr_parameters_1 = tk.Frame(self.fr_parameters)
        self.fr_parameters_1.grid(row=0, column=0)

        self.lbl_driver_beam_energy = tk.Label(self.fr_parameters_1, text="Driver Beam Energy (J)")
        self.lbl_injector_beam_energy = tk.Label(self.fr_parameters_1, text="Injector Beam Energy (J)")
        self.entry_driver_beam_energy = tk.Entry(self.fr_parameters_1, width=int(0.5 * total_width))
        self.entry_injector_beam_energy = tk.Entry(self.fr_parameters_1, width=int(0.5 * total_width))
        self.lbl_driver_beam_spot_size = tk.Label(self.fr_parameters_1, text="Driver Beam Spot Size (micron)")
        self.lbl_injector_beam_spot_size = tk.Label(self.fr_parameters_1, text="Injector Beam Spot Size (micron)")
        self.entry_driver_beam_spot_size = tk.Entry(self.fr_parameters_1, width=int(0.5 * total_width))
        self.entry_injector_beam_spot_size = tk.Entry(self.fr_parameters_1, width=int(0.5 * total_width))
        self.lbl_laser_contrast = tk.Label(self.fr_parameters_1, text="Laser Contrast")
        self.lbl_compressor_grating_position = tk.Label(self.fr_parameters_1, text="Compressor Grating Position (mm)")
        self.entry_laser_contrast = tk.Entry(self.fr_parameters_1, width=int(0.5 * total_width))
        self.entry_compressor_grating_position = tk.Entry(self.fr_parameters_1, width=int(0.5 * total_width))

        self.lbl_driver_beam_energy.grid(row=0, column=0)
        self.lbl_driver_beam_spot_size.grid(row=0, column=1)
        self.entry_driver_beam_energy.grid(row=1, column=0)
        self.entry_driver_beam_spot_size.grid(row=1, column=1)
        self.lbl_injector_beam_energy.grid(row=2, column=0)
        self.lbl_injector_beam_spot_size.grid(row=2, column=1)
        self.entry_injector_beam_energy.grid(row=3, column=0)
        self.entry_injector_beam_spot_size.grid(row=3, column=1)
        self.lbl_laser_contrast.grid(row=4, column=0)
        self.lbl_compressor_grating_position.grid(row=4, column=1)
        self.entry_laser_contrast.grid(row=5, column=0)
        self.entry_compressor_grating_position.grid(row=5, column=1)

        # Frame 2: target x/y/z, objective lens x/y/z, sample x/y/z
        self.fr_parameters_2 = tk.Frame(self.fr_parameters)
        self.fr_parameters_2.grid(row=1, column=0)

        self.lbl_target_x = tk.Label(self.fr_parameters_2, text="Target x (mm)")
        self.lbl_target_y = tk.Label(self.fr_parameters_2, text="Target y (mm)")
        self.lbl_target_z = tk.Label(self.fr_parameters_2, text="Target z (mm)")
        self.entry_target_x = tk.Entry(self.fr_parameters_2, width=int(1 / 3 * total_width))
        self.entry_target_y = tk.Entry(self.fr_parameters_2, width=int(1 / 3 * total_width))
        self.entry_target_z = tk.Entry(self.fr_parameters_2, width=int(1 / 3 * total_width))
        self.lbl_objective_lens_x = tk.Label(self.fr_parameters_2, text="Objective Lens x (mm)")
        self.lbl_objective_lens_y = tk.Label(self.fr_parameters_2, text="Objective Lens y (mm)")
        self.lbl_objective_lens_z = tk.Label(self.fr_parameters_2, text="Objective Lens z (mm)")
        self.entry_objective_lens_x = tk.Entry(self.fr_parameters_2, width=int(1 / 3 * total_width))
        self.entry_objective_lens_y = tk.Entry(self.fr_parameters_2, width=int(1 / 3 * total_width))
        self.entry_objective_lens_z = tk.Entry(self.fr_parameters_2, width=int(1 / 3 * total_width))
        self.lbl_sample_x = tk.Label(self.fr_parameters_2, text="Sample x (mm)")
        self.lbl_sample_y = tk.Label(self.fr_parameters_2, text="Sample y (mm)")
        self.lbl_sample_z = tk.Label(self.fr_parameters_2, text="Sample z (mm)")
        self.entry_sample_x = tk.Entry(self.fr_parameters_2, width=int(1 / 3 * total_width))
        self.entry_sample_y = tk.Entry(self.fr_parameters_2, width=int(1 / 3 * total_width))
        self.entry_sample_z = tk.Entry(self.fr_parameters_2, width=int(1 / 3 * total_width))

        self.lbl_target_x.grid(row=0, column=0)
        self.lbl_target_y.grid(row=0, column=1)
        self.lbl_target_z.grid(row=0, column=2)
        self.entry_target_x.grid(row=1, column=0)
        self.entry_target_y.grid(row=1, column=1)
        self.entry_target_z.grid(row=1, column=2)
        self.lbl_objective_lens_x.grid(row=2, column=0)
        self.lbl_objective_lens_y.grid(row=2, column=1)
        self.lbl_objective_lens_z.grid(row=2, column=2)
        self.entry_objective_lens_x.grid(row=3, column=0)
        self.entry_objective_lens_y.grid(row=3, column=1)
        self.entry_objective_lens_z.grid(row=3, column=2)
        self.lbl_sample_x.grid(row=4, column=0)
        self.lbl_sample_y.grid(row=4, column=1)
        self.lbl_sample_z.grid(row=4, column=2)
        self.entry_sample_x.grid(row=5, column=0)
        self.entry_sample_y.grid(row=5, column=1)
        self.entry_sample_z.grid(row=5, column=2)

        # Frame 3: probe stage/beams delay, injector materials/OAP settings
        self.fr_parameters_3 = tk.Frame(self.fr_parameters)
        self.fr_parameters_3.grid(row=2, column=0)

        self.lbl_gas_pressure_1 = tk.Label(self.fr_parameters_3, text="Gas Pressure 1 (PSI)")
        self.lbl_gas_pressure_2 = tk.Label(self.fr_parameters_3, text="Gas Pressure 2 (PSI)")
        self.entry_gas_pressure_1 = tk.Entry(self.fr_parameters_3, width=int(0.5 * total_width))
        self.entry_gas_pressure_2 = tk.Entry(self.fr_parameters_3, width=int(0.5 * total_width))
        self.lbl_probe_stage_delay = tk.Label(self.fr_parameters_3, text="Probe Stage Delay (mm)")
        self.lbl_beams_delay = tk.Label(self.fr_parameters_3, text="Beams Delay (mm)")
        self.entry_probe_stage_delay = tk.Entry(self.fr_parameters_3, width=int(0.5 * total_width))
        self.entry_beams_delay = tk.Entry(self.fr_parameters_3, width=int(0.5 * total_width))
        self.lbl_xray_filter_materials = tk.Label(self.fr_parameters_3, text="X-Ray Filter Materials")
        self.entry_xray_filter_materials = tk.Entry(self.fr_parameters_3, width=total_width)
        self.lbl_injector_oap_motor_settings = tk.Label(self.fr_parameters_3, text="Injector OAP Motor Settings")
        self.entry_injector_oap_motor_settings = tk.Entry(self.fr_parameters_3, width=total_width)

        self.lbl_gas_pressure_1.grid(row=0, column=0)
        self.lbl_gas_pressure_2.grid(row=0, column=1)
        self.entry_gas_pressure_1.grid(row=1, column=0)
        self.entry_gas_pressure_2.grid(row=1, column=1)
        self.lbl_probe_stage_delay.grid(row=2, column=0)
        self.lbl_beams_delay.grid(row=2, column=1)
        self.entry_probe_stage_delay.grid(row=3, column=0)
        self.entry_beams_delay.grid(row=3, column=1)
        self.lbl_xray_filter_materials.grid(row=4, column=0, columnspan=2)
        self.entry_xray_filter_materials.grid(row=5, column=0, columnspan=2)
        self.lbl_injector_oap_motor_settings.grid(row=6, column=0, columnspan=2)
        self.entry_injector_oap_motor_settings.grid(row=7, column=0, columnspan=2)

        # Frame 4:  Laser polarization, ESPEC 1/2 in, pointing/interferometry/spectroscopy beam in,
        #           injector/probe beam, block in, leak through camera
        self.fr_parameters_4 = tk.Frame(self.fr_parameters)
        self.fr_parameters_4.grid(row=3, column=0)

        self.espec_1_in = tk.BooleanVar(value=True)
        self.checkbutton_espec_1_in = tk.Checkbutton(self.fr_parameters_4, text="ESPEC 1 In", variable=self.espec_1_in)
        self.espec_2_in = tk.BooleanVar(value=True)
        self.checkbutton_espec_2_in = tk.Checkbutton(self.fr_parameters_4, text="ESPEC 2 In", variable=self.espec_2_in)
        self.pointing_cam_filters_in = tk.BooleanVar(value=True)
        self.checkbutton_pointing_cam_filters_in = tk.Checkbutton(self.fr_parameters_4,
                                                                  text="Pointing Camera Filters In",
                                                                  variable=self.pointing_cam_filters_in)
        self.interferometry_filters_in = tk.BooleanVar(value=True)
        self.checkbutton_interferometry_filters_1_in = tk.Checkbutton(self.fr_parameters_4,
                                                                      text="Interferometry Filters In",
                                                                      variable=self.interferometry_filters_in)
        self.xray_spectroscopy_filters_in = tk.BooleanVar(value=True)
        self.checkbutton_xray_spectroscopy_filters_in = tk.Checkbutton(self.fr_parameters_4,
                                                                       text="X-Ray Spectroscopy Filters In",
                                                                       variable=self.xray_spectroscopy_filters_in)
        self.probe_beam_block_in = tk.BooleanVar(value=True)
        self.checkbutton_probe_beam_block_in = tk.Checkbutton(self.fr_parameters_4, text="Probe Beam Block In",
                                                              variable=self.probe_beam_block_in)
        self.driver_beam_block_in = tk.BooleanVar(value=True)
        self.checkbutton_driver_beam_block_in = tk.Checkbutton(self.fr_parameters_4, text="Driver Beam Block In",
                                                               variable=self.driver_beam_block_in)
        self.injector_beam_block_in = tk.BooleanVar(value=True)
        self.checkbutton_injector_beam_block_in = tk.Checkbutton(self.fr_parameters_4, text="Injector Beam Block In",
                                                                 variable=self.injector_beam_block_in)
        self.leak_through_cam = tk.BooleanVar(value=True)
        self.checkbutton_leak_through_cam = tk.Checkbutton(self.fr_parameters_4, text="Leak Through Cam",
                                                           variable=self.leak_through_cam)
        self.laser_polarization_options = ["CP", "LP"]
        self.laser_polarization = tk.StringVar()
        self.laser_polarization.set(self.laser_polarization_options[0])
        self.dropdown_laser_polarization = ttk.Combobox(self.fr_parameters_4, textvariable=self.laser_polarization)
        self.dropdown_laser_polarization['values'] = tuple(self.laser_polarization_options)

        self.checkbutton_espec_1_in.grid(row=0, column=0, sticky=tk.W)
        self.checkbutton_espec_2_in.grid(row=0, column=1, sticky=tk.W)
        self.checkbutton_pointing_cam_filters_in.grid(row=1, column=0, sticky=tk.W)
        self.checkbutton_interferometry_filters_1_in.grid(row=1, column=1, sticky=tk.W)
        self.checkbutton_xray_spectroscopy_filters_in.grid(row=2, column=0, sticky=tk.W)
        self.checkbutton_probe_beam_block_in.grid(row=2, column=1, sticky=tk.W)
        self.checkbutton_driver_beam_block_in.grid(row=3, column=0, sticky=tk.W)
        self.checkbutton_injector_beam_block_in.grid(row=3, column=1, sticky=tk.W)
        self.checkbutton_leak_through_cam.grid(row=4, column=0, sticky=tk.W)
        self.dropdown_laser_polarization.grid(row=4, column=1, sticky=tk.W)

        """ Shot Metrics """
        # Frame 1: x-ray filter thickness/ID, DM1/DM2 actuator voltage
        self.fr_metrics_1 = tk.Frame(self.fr_metrics)
        self.fr_metrics_1.grid(row=0, column=0)

        self.lbl_xray_filter_id = tk.Label(self.fr_metrics_1, text="X-Ray Filter ID")
        self.lbl_xray_filter_thickness = tk.Label(self.fr_metrics_1, text="X-Ray Filter Thickness (mm)")
        self.entry_xray_filter_id = tk.Entry(self.fr_metrics_1, width=int(0.5*total_width))
        self.entry_xray_filter_thickness = tk.Entry(self.fr_metrics_1, width=int(0.5*total_width))
        self.lbl_dm1_actuator_voltage = tk.Label(self.fr_metrics_1, text="DM1 Actuator Voltage (V)")
        self.lbl_dm2_actuator_voltage = tk.Label(self.fr_metrics_1, text="DM2 Actuator Voltage (V)")
        self.entry_dm1_actuator_voltage = tk.Entry(self.fr_metrics_1, width=int(0.5*total_width))
        self.entry_dm2_actuator_voltage = tk.Entry(self.fr_metrics_1, width=int(0.5*total_width))

        self.lbl_xray_filter_id.grid(row=0, column=0)
        self.lbl_xray_filter_thickness.grid(row=0, column=1)
        self.entry_xray_filter_id.grid(row=1, column=0)
        self.entry_xray_filter_thickness.grid(row=1, column=1)
        self.lbl_dm1_actuator_voltage.grid(row=2, column=0)
        self.lbl_dm2_actuator_voltage.grid(row=2, column=1)
        self.entry_dm1_actuator_voltage.grid(row=3, column=0)
        self.entry_dm2_actuator_voltage.grid(row=3, column=1)

        # Frame 2: PMT 1/2/3, Dazzler 2nd/3rd/4th order phase
        self.fr_metrics_2 = tk.Frame(self.fr_metrics)
        self.fr_metrics_2.grid(row=1, column=0)

        self.lbl_pmt_1 = tk.Label(self.fr_metrics_2, text="PMT 1 (V)")
        self.lbl_pmt_2 = tk.Label(self.fr_metrics_2, text="PMT 2 (V)")
        self.lbl_pmt_3 = tk.Label(self.fr_metrics_2, text="PMT 3 (V)")
        self.entry_pmt_1 = tk.Entry(self.fr_metrics_2, width=int(1/3*total_width))
        self.entry_pmt_2 = tk.Entry(self.fr_metrics_2, width=int(1/3*total_width))
        self.entry_pmt_3 = tk.Entry(self.fr_metrics_2, width=int(1/3*total_width))
        self.lbl_dazzler_2nd_order_phase = tk.Label(self.fr_metrics_2, text="Dazzler 2nd Order Phase")
        self.lbl_dazzler_3rd_order_phase = tk.Label(self.fr_metrics_2, text="Dazzler 3rd Order Phase")
        self.lbl_dazzler_4th_order_phase = tk.Label(self.fr_metrics_2, text="Dazzler 4th Order Phase")
        self.entry_dazzler_2nd_order_phase = tk.Entry(self.fr_metrics_2, width=int(1 / 3 * total_width))
        self.entry_dazzler_3rd_order_phase = tk.Entry(self.fr_metrics_2, width=int(1 / 3 * total_width))
        self.entry_dazzler_4th_order_phase = tk.Entry(self.fr_metrics_2, width=int(1 / 3 * total_width))

        self.lbl_pmt_1.grid(row=0, column=0)
        self.lbl_pmt_2.grid(row=0, column=1)
        self.lbl_pmt_3.grid(row=0, column=2)
        self.entry_pmt_1.grid(row=1, column=0)
        self.entry_pmt_2.grid(row=1, column=1)
        self.entry_pmt_3.grid(row=1, column=2)
        self.lbl_dazzler_2nd_order_phase.grid(row=2, column=0)
        self.lbl_dazzler_3rd_order_phase.grid(row=2, column=1)
        self.lbl_dazzler_4th_order_phase.grid(row=2, column=2)
        self.entry_dazzler_2nd_order_phase.grid(row=3, column=0)
        self.entry_dazzler_3rd_order_phase.grid(row=3, column=1)
        self.entry_dazzler_4th_order_phase.grid(row=3, column=2)

        # Frame 3: Dazzler hole pos/width/depth, Dazzler wavelength
        self.fr_metrics_3 = tk.Frame(self.fr_metrics)
        self.fr_metrics_3.grid(row=2, column=0)

        self.lbl_dazzler_hole_position = tk.Label(self.fr_metrics_3, text="Dazzler Hole Position (mm)")
        self.lbl_dazzler_hole_depth = tk.Label(self.fr_metrics_3, text="Dazzler Hole Depth (mm)")
        self.entry_dazzler_hole_position = tk.Entry(self.fr_metrics_3, width=int(0.5 * total_width))
        self.entry_dazzler_hole_depth = tk.Entry(self.fr_metrics_3, width=int(0.5 * total_width))
        self.lbl_dazzler_hole_width = tk.Label(self.fr_metrics_3, text="Dazzler Hole Width (mm)")
        self.lbl_dazzler_central_wavelength = tk.Label(self.fr_metrics_3, text="Dazzler Central Wavelength (mm)")
        self.entry_dazzler_hole_width = tk.Entry(self.fr_metrics_3, width=int(0.5 * total_width))
        self.entry_dazzler_central_wavelength = tk.Entry(self.fr_metrics_3, width=int(0.5 * total_width))

        self.lbl_dazzler_hole_position.grid(row=0, column=0)
        self.lbl_dazzler_hole_depth.grid(row=0, column=1)
        self.entry_dazzler_hole_position.grid(row=1, column=0)
        self.entry_dazzler_hole_depth.grid(row=1, column=1)
        self.lbl_dazzler_hole_width.grid(row=2, column=0)
        self.lbl_dazzler_central_wavelength.grid(row=2, column=1)
        self.entry_dazzler_hole_width.grid(row=3, column=0)
        self.entry_dazzler_central_wavelength.grid(row=3, column=1)

        """ Shot Artifacts """
        self.lbl_comments = tk.Label(self.fr_artifacts, text="Comments")
        self.text_comments = ScrolledText(self.fr_artifacts, width=int(0.765 * total_width),
                                          height=int(0.1 * total_width))
        self.dir_upload = "./"
        self.btn_upload = tk.Button(self.fr_artifacts, text="Select Files", command=lambda: self.select_files())

        self.lbl_comments.grid(row=0, column=0, sticky=tk.W)
        self.text_comments.grid(row=1, column=0)
        self.btn_upload.grid(row=2, column=0, pady=2)

    def select_files(self):
        """ Prompts user to select files to upload """
        self.dir_upload = fd.askopenfilenames(initialdir="./", title="Select Files")

    def get_settings(self):
        """ Data to return """
        shot_id = {
            "exp_name": self.entry_exp_name.get(),
            "shot_num": self.entry_shot_num.get(),
            "shot_date": self.entry_shot_date.get(),
            "shot_time": self.entry_shot_time.get()
        }
        parameters = {
            "driver_beam_energy": self.entry_driver_beam_energy.get(),
            "driver_beam_spot_size": self.entry_driver_beam_spot_size.get(),
            "injector_beam_energy": self.entry_injector_beam_energy.get(),
            "injector_beam_spot_size": self.entry_injector_beam_spot_size.get(),
            "gas_pressure_1": self.entry_gas_pressure_1.get(),
            "gas_pressure_2": self.entry_gas_pressure_2.get(),
            "target_x": self.entry_target_x.get(),
            "target_y": self.entry_target_y.get(),
            "target_z": self.entry_target_z.get(),
            "objective_lens_x": self.entry_objective_lens_x.get(),
            "objective_lens_y": self.entry_objective_lens_y.get(),
            "objective_lens_z": self.entry_objective_lens_z.get(),
            "sample_x": self.entry_sample_x.get(),
            "sample_y": self.entry_sample_y.get(),
            "sample_z": self.entry_sample_z.get(),
            "probe_stage_delay": self.entry_probe_stage_delay.get(),
            "beams_delay": self.entry_beams_delay.get(),
            "xray_filter_materials": self.entry_xray_filter_materials.get(),
            "injector_oap_motor_settings": self.entry_injector_oap_motor_settings.get()
        }
        metrics = {
            "xray_filter_id": self.entry_xray_filter_id.get(),
            "xray_filter_thickness": self.entry_xray_filter_thickness.get(),
            "dm1_actuator_voltage": self.entry_dm1_actuator_voltage.get(),
            "dm2_actuator_voltage": self.entry_dm2_actuator_voltage.get(),
            "pmt_1": self.entry_pmt_1.get(),
            "pmt_2": self.entry_pmt_2.get(),
            "pmt_3": self.entry_pmt_3.get(),
            "dazzler_2nd_order_phase": self.entry_dazzler_2nd_order_phase.get(),
            "dazzler_3rd_order_phase": self.entry_dazzler_3rd_order_phase.get(),
            "dazzler_4th_order_phase": self.entry_dazzler_4th_order_phase.get(),
            "dazzler_hole_position": self.entry_dazzler_hole_position.get(),
            "dazzler_hole_depth": self.entry_dazzler_hole_depth.get(),
            "dazzler_hole_width": self.entry_dazzler_hole_width.get(),
            "dazzler_central_wavelength": self.entry_dazzler_central_wavelength.get(),
        }

        """ Convert numbers: int if possible, then float if possible """
        out = (shot_id, parameters, metrics)
        for dictionary in out:
            for key, value in zip(dictionary.keys(), dictionary.values()):
                try:
                    value = int(value)
                    dictionary.update({key: value})
                except ValueError:
                    try:
                        value = float(value)
                        dictionary.update({key: value})
                    except ValueError:
                        pass
        print(out[0])
        print(out[1])
        print(out[2])
        return out