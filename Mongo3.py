import tkinter as tk
from tkinter import ttk
from pymongo import MongoClient
from tkinter import messagebox
from pymongo import DESCENDING, ASCENDING

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

    create_index_button = ttk.Button(frame, text="Create Index", command=lambda: create_index(collection_name))
    create_index_button.grid(row=len(attributes) + 101, column=0, padx=5, pady=5, sticky="e")

    get_indexes_button = ttk.Button(frame, text="Get Indexes", command=lambda: get_indexes(collection_name))
    get_indexes_button.grid(row=len(attributes) + 101, column=1, padx=5, pady=5, sticky="e")

    show_index_button = ttk.Button(frame, text="Show Index",command=lambda: show_index(collection_name))
    show_index_button.grid(row=len(attributes) + 101, column=2, padx=5, pady=5, sticky="e")

    Aggregate_match_then_sort_button = ttk.Button(frame, text="Aggregate(match then sort)",command=lambda: Aggregate_match_then_sort(collection_name))
    Aggregate_match_then_sort_button.grid(row=len(attributes) + 101, column=3, padx=5, pady=5, sticky="e")

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
        messagebox.showerror("Error", "Invalid query syntax. Please enter a valid JSON format.")

# Function to create an index in the collection
def create_index(collection_name):
    
    # Clear the result text
    result_text.delete(1.0, tk.END)

    # Get the query from the query entry field
    query = query_entry.get()
    
    list_query = query.split(",")
    
    index = None

    if list_query[1]=='1':
        index = ASCENDING
    elif list_query[1]=='-1':
        index =  DESCENDING 

    collection = db[collection_name]
    collection.create_index([(list_query[0], index)]) 

    #collection.create_index([("structureId", 1)])  # Create an index on the "structureId" field
    messagebox.showinfo("Success", "Index created successfully.")

# Function to retrieve the indexes in the collection
def get_indexes(collection_name):
    collection = db[collection_name]
    indexes = collection.index_information()
    index_info = "\n".join([f"{index}: {info}" for index, info in indexes.items()])
    result_text.insert(tk.END, index_info + "\n")


# Function to show index in the collection
def show_index(collection_name):
    # Clear the result text
    result_text.delete(1.0, tk.END)

    # Get the query from the query entry field
    query = query_entry.get()
    
    list_query = query.split(",")
    
    index = None

    if list_query[1]=='1':
        index = ASCENDING
    elif list_query[1]=='-1':
        index =  DESCENDING 
    
    collection = db[collection_name]
    results = collection.find().hint([(list_query[0], index)])

    for result in results:
         result_text.insert(tk.END, str(result) + "\n")
    

    
   

# Function to match values then sort 
def Aggregate_match_then_sort(collection_name):
    # Clear the result text
    result_text.delete(1.0, tk.END)

    # Get the query from the query entry field
    query = query_entry.get()
    
    list_query = query.split(",")
    
    idx = None

    if list_query[3]=='1':
        idx = ASCENDING
    elif list_query[3]=='-1':
        idx =  DESCENDING 
    
    pipeline = [
   {
      "$match": {
         list_query[0]:list_query[1]
      }
   }, 
   {
      "$sort": {
         list_query[2]:idx
      }
   }
    ]

    


    collection = db[collection_name]

    # for doc in collection.aggregate(pipeline):
    #      print(doc)
    #      result_text.insert(tk.END, str(doc) + "\n")

    results = collection.aggregate(pipeline)  
    #print(results)
    #messagebox.showinfo("Success", "Aggregate created successfully.")
    
            
    
    #result_text.insert(tk.END, str(results) + "\n")
    
    for value in results:
         result_text.insert(tk.END, str(value) + "\n")
    
    messagebox.showinfo("Success", "Aggregate created successfully.")


    #final_result = "\n".join([value for value in results])
    #result_text.insert(tk.END, results + "\n") 


    

# Function to insert protein_structure without classification attributes
# def insert_protein_without_classification(collection_name):
#     collection = db[collection_name]
#     data = {attribute: entry.get() for attribute, entry in entries.items() if attribute != "classification"}
#     collection.insert_one(data)

#     # Clear the entry fields
#     for entry in entries.values():
#         entry.delete(0, tk.END)

#     # Display success message
#     messagebox.showinfo("Success", "Record entered successfully (without classification).")

# Function to create an index with attributes
# def create_index_with_attributes(collection_name):
#     # Get the input data from entry fields
#     data = {attribute: entry.get() for attribute, entry in entries.items()}

#     # Create an index with the provided attributes
#     collection = db[collection_name]
#     attributes = list(data.values())
#     collection.create_index(attributes)

#     # Clear the entry fields
#     for entry in entries.values():
#         entry.delete(0, tk.END)

#     # Display success message
#     messagebox.showinfo("Success", "Index created successfully with attributes.")

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