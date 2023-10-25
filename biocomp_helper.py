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
    df = pd.read_excel("H:\Development\Bioengineer projects\Biocompatibility\Biocompatibility Track Sheet.xlsx")

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

    # print(f"Materials detected: \n")
    # print(f"Methods detected: \n {methods_set}")

    # print("\n")

    # Create a tkinter GUI for user input
    window = tk.Tk()
    window.title("Select Materials and Methods")

    window.minsize(width=800, height=300)
    window.maxsize(width=800, height=1000)

    selected_materials = set()
    selected_methods = set()

    # Create scrollable frames for the sets
    frame1 = tk.Frame(window)
    frame2 = tk.Frame(window)

    # frame1.grid(row=0, column=0, padx=10, sticky='ns')
    # frame2.grid(row=0, column=1, padx=10, sticky='ns')

    frame1.pack(side=tk.LEFT, padx=10, expand=False, fill="both")
    frame2.pack(side=tk.LEFT, padx=10, expand=False, fill="both")
    # frame3.pack(side=tk.LEFT, padx=10, expand=True, fill="both")

    frame_height = 500
    frame_width = 800

    canvas1 = tk.Canvas(frame1, width=180)
    canvas2 = tk.Canvas(frame2, width=300)

    canvas1.pack(expand=False, side=tk.LEFT, pady=10, fill="both")
    canvas2.pack(expand=False, side=tk.LEFT, pady=10, fill="both")

    # canvas1.grid(row=0, column=0, sticky='ns')
    # canvas2.grid(row=0, column=0, sticky='ns')

    scrollbar1 = tk.Scrollbar(frame1, orient="vertical", command=canvas1.yview)
    scrollbar2 = tk.Scrollbar(frame2, orient="vertical", command=canvas2.yview)

    scrollbar1.pack(side=tk.LEFT, fill="y", pady=10, expand=False)
    scrollbar2.pack(side=tk.LEFT, fill="y", pady=10, expand=False)

    # scrollbar1.grid(row=0, column=1, sticky='ns')
    # scrollbar2.grid(row=0, column=1, sticky='ns')

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

    # # Create a label to display the selected items
    # result_text = tk.Label(window, text="Selected Items: ")
    # # result_text.pack(padx=50, expand=False)
    # result_text.grid(row=1, columnspan=2, padx=(10), sticky='w')

    # result_text.grid_columnconfigure(0, minsize=200)

    def update_selection():
        # selected_methods = set()
        selected_methods.clear()
        for checkbox, item in zip(method_boxes, sorted(methods_list)):
            print(f"{checkbox}, {item}\n")
            if checkbox.get() == 1:
                # print(f"item {item} selected")
                selected_methods.add(item)
                # print(selected_methods)
        # result_text.config(text="Selected Items: " + ", ".join(selected_methods))

        selected_materials.clear()
        for checkbox, item in zip(material_boxes, sorted(materials_list)):
            # print(f"{checkbox}, {item}\n")
            if checkbox.get() == 1:
                selected_materials.add(item)
        # result_text.config(text="Selected Items: " + ", ".join([selected_methods, selected_materials]))

    # # Create a button to update the result
    # update_button = tk.Button(window, text="Update Selection", command=update_selection)
    # # update_button.pack()
    # update_button.grid(row=2, columnspan=2, padx=(50, 10), sticky='w')
    # update_button.grid_columnconfigure(0, minsize=200)

    def process_selection():
        update_selection()
        # print(selected_materials)
        # print(selected_methods)
        demo_set = selected_materials | selected_methods

        # for item in demo_set:
        #     print(item)

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

        if len(smallest_device_set) > 0:
            print(f"Smallest set of devices that covers all required items, {len(smallest_device_set)} total:")
            for index, device in enumerate(smallest_device_set):
                print_bold(f"Device {index+1} of {len(smallest_device_set)}")
                print("Description:", device.description)
                print("Catalogue Code:", device.catalogue_code)
                print("Contact Characterization:", device.contact_characterization, "\n")
                print("Materials:")
                for material in device.materials:
                    if set(material).issubset(selected_materials):
                        print_bold(material)
                    else:
                        print(material)

                print("")

                print("Methods:")
                for method in device.methods:
                    if set(method).issubset(selected_methods):
                        print_bold(method)
                    print(method)
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

    # materials_label = Label(root, text="Select Materials:")
    # materials_frame = Frame(root)
    # materials_frame.pack()

    # materials_canvas = Canvas(materials_frame, borderwidth=0)
    # materials_scrollbar = Scrollbar(materials_frame, orient="vertical", command=materials_canvas.yview)
    
    # materials_frame_inner = Frame(materials_canvas)
    # materials_canvas.create_window((0, 0), window=materials_frame_inner, anchor="nw")
    
    # materials_canvas.configure(yscrollcommand=materials_scrollbar.set)
    
    # materials_scrollbar.pack(side="right", fill="y")
    # materials_canvas.pack(side="left", fill="both", expand=True)
    # materials_frame_inner.bind("<Configure>", lambda event, canvas=materials_canvas: canvas.configure(scrollregion=canvas.bbox("all")))
    
    # for material in materials_set:
    #     var = BooleanVar()
    #     var.set(False)  # Set the initial state to deselected
    #     cb = Checkbutton(materials_frame_inner, text=material, variable=var)
    #     cb.pack(anchor="w")
    #     var.trace("w", lambda *_: update_selection(selected_materials, var, material)) 
    
    # methods_label = Label(root, text="Select Methods:")
    # methods_frame = Frame(root)
    # methods_frame.pack()

    # methods_canvas = Canvas(methods_frame, borderwidth=0)
    # methods_scrollbar = Scrollbar(methods_frame, orient="vertical", command=methods_canvas.yview)
    
    # methods_frame_inner = Frame(methods_canvas)
    # methods_canvas.create_window((0, 0), window=methods_frame_inner, anchor="nw")
    
    # methods_canvas.configure(yscrollcommand=methods_scrollbar.set)
    
    # methods_scrollbar.pack(side="right", fill="y")
    # methods_canvas.pack(side="left", fill="both", expand=True)
    # methods_frame_inner.bind("<Configure>", lambda event, canvas=methods_canvas: canvas.configure(scrollregion=canvas.bbox("all")))
    
    # for method in methods_set:
    #     var = BooleanVar()
    #     var.set(False)  # Set the initial state to deselected
    #     cb = Checkbutton(methods_frame_inner, text=method, variable=var)
    #     cb.pack(anchor="w")
    #     var.trace("w", lambda *_: update_selection(selected_methods, var, method))

    

    # # Function to update selected items
    # def update_selection(selected_set, var, item):
    #     selected_set.clear()
    #     for child in materials_frame_inner.winfo_children():
    #         if child.cget("variable").get():
    #             selected_set.add(child.cget("text"))
    #     for child in methods_frame_inner.winfo_children():
    #         if child.cget("variable").get():
    #             selected_set.add(child.cget("text"))

    # Function to process the selected items
    def process_selection():
        demo_set = selected_materials | selected_methods
        print(f"Required items to be covered:\n")

        print(f"Materials: \n")
        for item in selected_materials:
            print(f"{item}")

        print(f"Methods: \n")
        for item in selected_methods:
            print(f"{item}")

        smallest_device_set = find_smallest_cover(devices, demo_set)

        if len(smallest_device_set) > 0:
            print(f"Smallest set of devices that covers all required items, {len(smallest_device_set)} total:")
            print("\n")
            for index, device in enumerate(smallest_device_set):
                print(f"Device {index+1} of {len(smallest_device_set)}")
                print("Description:", device.description)
                print("Catalogue Code:", device.catalogue_code)
                print("Contact Characterization:", device.contact_characterization)
                print("Materials:\n", device.materials)
                print("Methods:\n", device.methods)
                print("\n")
        else:
            print("No set that covers all the provided items was found")

    # process_button = Button(root, text="Process Selection", command=process_selection)
    # process_button.pack()

    # root.mainloop()

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
