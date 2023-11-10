import tkinter as tk
from tkinter import ttk
from pymongo import MongoClient
from tkinter import messagebox

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017")
db = client["Protein"]

# Create the main window
window = tk.Tk()
window.title("Protein Structure Data Management")
window.geometry("700x700")

# Define global attributes and entries variables
attributes = []
entries = {}
query_entry = None  # Define query_entry variable

# Function to handle collection selection
def handle_collection_selection(event):
    selected_collection = collection_dropdown.get()
    # Implement logic based on the selected collection
    if selected_collection == "CrystallizationMethod":
        attributes = ["_id", "crystallizationMethodName", "crystallizationTemperatureK"]
    elif selected_collection == "ExperimentalTechnique":
        attributes = ["_id", "experimentalTechnique_Name"]
    elif selected_collection == "ProteinStructure":
        attributes = [
            "structureId",
            "classification",
            "macromoleculeType",
            "residueCount",
            "resolution",
            "structureMolecularWeight",
            "crystallizationMethodId",
            "experimentalTechniqueId",
            "densityMatthews",
            "densityPercentSol",
            "pdbxDetails",
            "phValue",
            "publicationYear"
        ]
    clear_frame()
    create_attribute_labels(attributes)
    create_input_entries(attributes)
    create_operation_buttons(selected_collection)

# Function to clear the frame
def clear_frame():
    for widget in frame.winfo_children():
        widget.destroy()

# Function to create labels for attributes
def create_attribute_labels(attributes):
    for i, attribute in enumerate(attributes):
        label = ttk.Label(frame, text=attribute + ":")
        label.grid(row=i, column=0, sticky="e")

# Function to create entry fields for data input
def create_input_entries(attributes):
    entries.clear()
    for i, attribute in enumerate(attributes):
        entry = ttk.Entry(frame)
        entry.grid(row=i, column=1, padx=5, pady=5)
        entries[attribute] = entry

# Function to create buttons for operations
def create_operation_buttons(collection_name):
    enter_button = ttk.Button(frame, text="Enter", command=lambda: perform_enter(collection_name))
    enter_button.grid(row=len(attributes) + 100, column=0, padx=5, pady=5, sticky="e")

    update_button = ttk.Button(frame, text="Update", command=lambda: perform_update(collection_name))
    update_button.grid(row=len(attributes) + 100, column=1, padx=5, pady=5, sticky="e")

    delete_button = ttk.Button(frame, text="Delete", command=lambda: perform_delete(collection_name))
    delete_button.grid(row=len(attributes) + 100, column=2, padx=5, pady=5, sticky="e")

    search_button = ttk.Button(frame, text="Search", command=lambda: perform_search(collection_name))
    search_button.grid(row=len(attributes) + 100, column=3, padx=5, pady=5, sticky="e")

# Function to perform the Enter operation
def perform_enter(collection_name):
    # Get the input data from entry fields
    data = {attribute: entry.get() for attribute, entry in entries.items()}

    # Insert the data into the collection
    collection = db[collection_name]
    collection.insert_one(data)

    # Clear the entry fields
    for entry in entries.values():
        entry.delete(0, tk.END)

    # Display success message
    messagebox.showinfo("Success", "Record entered successfully.")

# Function to perform the Update operation
def perform_update(collection_name):
    # Get the input data from entry fields
    data = {attribute: entry.get() for attribute, entry in entries.items()}

    # Retrieve the structureId value separately
    structure_id = data.pop("structureId", None)

    # Remove the _id field from the data dictionary
    data.pop("_id", None)

    # Update the record in the collection
    collection = db[collection_name]
    result = collection.update_one({"structureId": structure_id}, {"$set": data})

    # Clear the entry fields
    for entry in entries.values():
        entry.delete(0, tk.END)

    # Display success message or update the result_text
    if result.modified_count > 0:
        messagebox.showinfo("Success", "Record updated successfully.")
    else:
        messagebox.showwarning("Error", "Failed to update the record.")

# Function to perform the Delete operation
def perform_delete(collection_name):
    # Get the input data from entry fields
    data = {attribute: entry.get() for attribute, entry in entries.items()}

    # Retrieve the structureId value separately
    structure_id = data.pop("structureId", None)

    # Delete the record from the collection
    collection = db[collection_name]
    result = collection.delete_one({"structureId": structure_id})

    # Clear the entry fields
    for entry in entries.values():
        entry.delete(0, tk.END)

    # Display success message or update the result_text
    if result.deleted_count > 0:
        messagebox.showinfo("Success", "Record deleted successfully.")
    else:
        messagebox.showwarning("Error", "Failed to delete the record.")

# Function to perform the Search operation
import json

# Function to perform the Search operation
def perform_search(collection_name):
    # Get the query from the query entry field
    query = query_entry.get()

    # Clear the result text
    result_text.delete(1.0, tk.END)

    # Search the collection based on the query
    collection = db[collection_name]
    try:
        query_dict = json.loads(query)
        results = collection.find(query_dict)

        # Display the search results in the result text
        for result in results:
            result_text.insert(tk.END, str(result) + "\n")
    except json.JSONDecodeError as e:
        messagebox.showerror("Error", "Invalid query syntax. Please enter a valid JSON format. Make sure to enclose the entire query within double quotes (\"\"), including the attribute names and values. In this query")


# Create a drop-down menu for collection selection
collection_label = ttk.Label(window, text="Select Collection:")
collection_label.pack()

collection_dropdown = ttk.Combobox(window, values=["CrystallizationMethod", "ExperimentalTechnique", "ProteinStructure"])
collection_dropdown.bind("<<ComboboxSelected>>", handle_collection_selection)
collection_dropdown.pack()

# Create a frame to contain the labels, entry fields, and buttons
frame = ttk.Frame(window)
frame.pack(padx=10, pady=10)

# Create a query entry field and Find button
query_label = ttk.Label(window, text="Query:")
query_label.pack()

query_entry = ttk.Entry(window)
query_entry.pack()

# Create a text area for displaying query results
result_text = tk.Text(window, width=80, height=10)
result_text.pack(padx=10, pady=10)

# Run the Tkinter event loop
window.mainloop()