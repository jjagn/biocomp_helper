import pandas as pd
from itertools import combinations
import tkinter as tk
from tkinter import Label, Button, BooleanVar, Frame, Canvas
from tkinter.ttk import Checkbutton, Scrollbar
# Define a struct for the device
class Device:
    def __init__(self, description, catalogue_code, contact_characterization, materials, methods):
        self.description = description
        self.catalogue_code = catalogue_code
        self.contact_characterization = contact_characterization
        self.materials = materials
        self.methods = methods

def main():
    # Load the spreadsheet into a DataFrame
    print("Reading spreadsheet. This can take a little while")
    df = pd.read_excel("H:\Development\_Development Data\Bioengineer projects\Biocompatibility\Biocompatibility Track Sheet.xlsx")

    # Initialize a list to store device structs
    devices = []

    # Process each row in the DataFrame
    for index, row in df.iterrows():
        description = row['Description']
        catalogue_code = row['Catalogue Code']
        contact_characterization = row['Characterisation of Body Contact']
        
        # Split the materials and methods by newline character and create sets
        materials = set()
        materials_raw = set(str(row['Materials']).split('\n'))
        for material in materials_raw:
            materials.add(material.strip())

        methods_raw = set(str(row['Manufacturing Methods']).split('\n'))
        methods = set()
        for method in methods_raw:
            methods.add(method.strip())

        if description == "STOP":
            break
        
        # Create a device struct
        device = Device(description, catalogue_code, contact_characterization, materials, methods)
        
        # Append the device struct to the list
        devices.append(device)

    materials_set = set()
    methods_set = set()

    for device in devices:
        materials_set |= device.materials
        methods_set |= device.methods

    # Create a tkinter GUI for user input
    window = tk.Tk()
    window.title("Select Materials and Methods")

    window.minsize(width=800, height=300)
    window.maxsize(width=800, height=1000)

    selected_materials = set()
    selected_methods = set()

    frame1 = tk.Frame(window)
    frame2 = tk.Frame(window)

    frame1.pack(side=tk.LEFT, padx=10, expand=False, fill="both")
    frame2.pack(side=tk.LEFT, padx=10, expand=False, fill="both")

    frame_height = 500
    frame_width = 800

    canvas1 = tk.Canvas(frame1, width=180)
    canvas2 = tk.Canvas(frame2, width=300)

    canvas1.pack(expand=False, side=tk.LEFT, pady=10, fill="both")
    canvas2.pack(expand=False, side=tk.LEFT, pady=10, fill="both")

    scrollbar1 = tk.Scrollbar(frame1, orient="vertical", command=canvas1.yview)
    scrollbar2 = tk.Scrollbar(frame2, orient="vertical", command=canvas2.yview)

    scrollbar1.pack(side=tk.LEFT, fill="y", pady=10, expand=False)
    scrollbar2.pack(side=tk.LEFT, fill="y", pady=10, expand=False)

    canvas1.config(yscrollcommand=scrollbar1.set)
    canvas2.config(yscrollcommand=scrollbar2.set)

    frame_on_canvas1 = tk.Frame(canvas1, width=100)
    canvas1.create_window(0, 0, window=frame_on_canvas1, anchor='nw')

    frame_on_canvas2 = tk.Frame(canvas2, width=100)
    canvas2.create_window(0, 0, window=frame_on_canvas2, anchor='nw')

    material_boxes = []
    materials_list = []
    for material in materials_set:
        materials_list.append(material)

    print_bold("Materials detected:")
    for material in sorted(materials_list):
        var = BooleanVar()
        var.set(False)
        checkbox = tk.Checkbutton(frame_on_canvas1, text=material, variable=var)
        checkbox.pack(anchor="w")
        material_boxes.append(var)
        print(material)
    print("")

    method_boxes = []
    methods_list = []
    for method in methods_set:
        methods_list.append(method)
    
    print_bold("Methods detected:")
    for method in sorted(methods_list):
        var = BooleanVar()
        var.set(False)
        checkbox = tk.Checkbutton(frame_on_canvas2, text=method, variable=var)
        checkbox.pack(anchor="w")
        method_boxes.append(var)
        print(method)
    print("")

    frame_on_canvas1.bind("<Configure>", lambda e: canvas1.configure(scrollregion=canvas1.bbox("all")))
    frame_on_canvas2.bind("<Configure>", lambda e: canvas2.configure(scrollregion=canvas2.bbox("all")))

    def update_selection():
        selected_methods.clear()
        for checkbox, item in zip(method_boxes, sorted(methods_list)):
            # print(f"{checkbox}, {item}\n")
            if checkbox.get() == 1:
                selected_methods.add(item)

        selected_materials.clear()
        for checkbox, item in zip(material_boxes, sorted(materials_list)):
            if checkbox.get() == 1:
                selected_materials.add(item)
       

    def process_selection():
        update_selection()
        demo_set = selected_materials | selected_methods

        print("=================================================")
        print_bold("Selected Materials:")
        for item in selected_materials:
            print(f"{item}")
        print("")

        print_bold("Selected Methods:")
        for item in selected_methods:
            print(f"{item}")
        print("")
        print("=================================================")

        smallest_device_set = find_smallest_cover(devices, demo_set)
        used_materials = selected_materials
        used_methods = selected_methods

        if len(smallest_device_set) > 0:
            print(f"Smallest set of devices that covers all required items, {len(smallest_device_set)} total:")
            for index, device in enumerate(smallest_device_set):
                print_bold(f"Device {index+1} of {len(smallest_device_set)}")
                print("Description:", device.description)
                print("Catalogue Code:", device.catalogue_code)
                print("Contact Characterization:", device.contact_characterization, "\n")

                print_bold("Device Materials:")
                for material in device.materials:
                    if set([material]).issubset(selected_materials):
                        print_bold(material)
                    else:
                        print(material)

                print("")

                print_bold("Device Methods:")
                for method in device.methods:
                    if set([method]).issubset(selected_methods):
                        print_bold(method)
                    else:
                        print(method)

                print("")

                print_bold("Materials from this device:")
                intersect_materials = used_materials.intersection(set(device.materials))
                if len(intersect_materials) == 0:
                    print("No materials contributed")
                else:
                    for material in intersect_materials:
                        print(material)
                        used_materials.remove(material)
                print("")

                print_bold("Methods from this device:")
                intersect_methods = used_methods.intersection(set(device.methods))
                if len(intersect_methods) == 0:
                    print("No methods contributed")
                else:
                    for method in intersect_methods:
                        print(method)
                        used_methods.remove(method)
                
                print("=================================================")
        else:
            print("No set that covers all the provided items was found")

    calculate_button = tk.Button(window, text="Find Devices", command=process_selection)
    calculate_button.pack(side=tk.LEFT, padx=50, pady=50)
    # calculate_button.grid(row=3, columnspan=2, padx=(50, 10), pady=(50), sticky='w')
    # calculate_button.grid_columnconfigure(0, minsize=200)

    frame_on_canvas1.update_idletasks()
    canvas1.config(scrollregion=canvas1.bbox('all'))

    frame_on_canvas2.update_idletasks()
    canvas2.config(scrollregion=canvas2.bbox('all'))

    # Start the Tkinter main loop
    window.mainloop()

    # Function to process the selected items
    # def process_selection():
    #     demo_set = selected_materials | selected_methods
    #     print(f"Required items to be covered:\n")

    #     print(f"Materials: \n")
    #     for item in selected_materials:
    #         print(f"{item}")

    #     print(f"Methods: \n")
    #     for item in selected_methods:
    #         print(f"{item}")

    #     smallest_device_set = find_smallest_cover(devices, demo_set)

    #     if len(smallest_device_set) > 0:
    #         print(f"Smallest set of devices that covers all required items, {len(smallest_device_set)} total:")
    #         print("\n")
    #         for index, device in enumerate(smallest_device_set):
    #             print(f"Device {index+1} of {len(smallest_device_set)}")
    #             print("Description:", device.description)
    #             print("Catalogue Code:", device.catalogue_code)
    #             print("Contact Characterization:", device.contact_characterization)
    #             print("Materials:\n", device.materials)
    #             print("Methods:\n", device.methods)
    #             print("\n")
    #     else:
    #         print("No set that covers all the provided items was found")

def find_smallest_cover(devices, target_set):
    min_cover = None
    min_length = float('inf')

    for r in range(1, len(devices) + 1):
        # Consider all combinations of 'r' sets from the original sets
        for combo in combinations(devices, r):
            sets = []

            for device in combo:
                sets.append(device.materials)
                sets.append(device.methods)
            combo1 = sets
            union_set = set().union(*combo1)

            if target_set.issubset(union_set):
                if r < min_length:
                    min_cover = combo
                    min_length = r

    return list(min_cover) if min_cover else []

def print_bold(to_print):
    print(f"\033[1m{to_print}\033[0m")

main()
