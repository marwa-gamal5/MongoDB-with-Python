from tkinter import *
from PIL import ImageTk, Image
import tkinter as tk
from tkinter import ttk
from pymongo import MongoClient
from tkinter import messagebox
from pymongo import DESCENDING, ASCENDING
#from tkinter import *
#from PIL import Image, ImageTk



# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017")
db = client["Cancer"]

# Create the main window
window = tk.Tk()
window.title("Breast Cancer Data Management")
window.geometry("700x700")
# Open the image file
image = Image.open("image2.gif")
# Resize the image
resized_image = image.resize((700, 700))
# Save the resized image
resized_image.save("resized_image.gif")

# Use the resized image in your Tkinter application
background_image = tk.PhotoImage(file="resized_image.gif")
background_label = tk.Label(window, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Define global attributes and entries variables
attributes = []
entries = {}
query_entry = None  # Define query_entry variable

# Function to handle collection selection
def handle_collection_selection(event):
    global attributes  # Add this line to access the global 'attributes' variable
    selected_collection = collection_dropdown.get()
    # Implement logic based on the selected collection
    if selected_collection == "Patients":
        attributes = ["patient_id", "age_at_diagnosis", "inferred_menopausal_state","death_from_cancer","overall_survival"]
    elif selected_collection == "Tumor_Information":
        attributes = ["patient_id", "cancer_type","cellularity","primary_tumor_laterality","mutation_count","tumor_size","tumor_stage"]
    elif selected_collection == "Treatment_Information":
        attributes = ["patient_id", "type_of_breast_surgery","chemotherapy","er_status_measured_by_ihc","hormone_therapy","pr_status","radio_therapy"]
    
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
        label = ttk.Label(frame, text=attribute + ":",style="CustomLabel.TLabel")
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
    # Configure the button's background color
    enter_button.configure(style="Phoshia.TButton")

    # Create a custom style for the button
    style = ttk.Style()
    style.configure("Phoshia.TButton", background="#FF00FF")  # Fuchsia color

    update_button = ttk.Button(frame, text="Update", command=lambda: perform_update(collection_name))
    update_button.grid(row=len(attributes) + 100, column=1, padx=5, pady=5, sticky="e")
    update_button.configure(style="Phoshia.TButton")


    delete_button = ttk.Button(frame, text="Delete", command=lambda: perform_delete(collection_name))
    delete_button.grid(row=len(attributes) + 100, column=2, padx=5, pady=5, sticky="e")
    delete_button.configure(style="Phoshia.TButton")

    search_button = ttk.Button(frame, text="Search", command=lambda: perform_search(collection_name))
    search_button.grid(row=len(attributes) + 100, column=3, padx=5, pady=5, sticky="e")
    search_button.configure(style="Phoshia.TButton")

    create_index_button = ttk.Button(frame, text="Create Index", command=lambda: create_index(collection_name))
    create_index_button.grid(row=len(attributes) + 101, column=0, padx=5, pady=5, sticky="e")
    create_index_button.configure(style="Phoshia.TButton")

    get_indexes_button = ttk.Button(frame, text="Get Indexes", command=lambda: get_indexes(collection_name))
    get_indexes_button.grid(row=len(attributes) + 101, column=1, padx=5, pady=5, sticky="e")
    get_indexes_button.configure(style="Phoshia.TButton")

    show_index_button = ttk.Button(frame, text="Show Index",command=lambda: show_index(collection_name))
    show_index_button.grid(row=len(attributes) + 101, column=2, padx=5, pady=5, sticky="e")
    show_index_button.configure(style="Phoshia.TButton")

    Aggregate_match_then_sort_button = ttk.Button(frame, text="Aggregate(match then sort)",command=lambda: Aggregate_match_then_sort(collection_name))
    Aggregate_match_then_sort_button.grid(row=len(attributes) + 101, column=3, padx=5, pady=5, sticky="e")
    Aggregate_match_then_sort_button.configure(style="Phoshia.TButton")

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
    patientid = data.pop("patient_id", None)

    # Remove the _id field from the data dictionary
    data.pop("_id", None)

    # Update the record in the collection
    collection = db[collection_name]
    result = collection.update_one({"patient_id": patientid}, {"$set": data})

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
    patientid = data.pop("patient_id", None)

    # Delete the record from the collection
    collection = db[collection_name]
    result = collection.delete_one({"patient_id": patientid})

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
    # Clear the result text
    result_text.delete(1.0, tk.END)

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

# Create a style object
style = ttk.Style()
# Configure the style to set the foreground color (text color)
style.configure("CustomLabel.TLabel", foreground="#FF00FF")

# Create a drop-down menu for collection selection
collection_label = ttk.Label(window, text="Select Collection:",style="CustomLabel.TLabel")
collection_label.pack()

collection_dropdown = ttk.Combobox(window, values=["Patients", "Tumor_Information", "Treatment_Information"])
collection_dropdown.bind("<<ComboboxSelected>>", handle_collection_selection)
collection_dropdown.pack()

# Create a frame to contain the labels, entry fields, and buttons
frame = ttk.Frame(window)
frame.pack(padx=10, pady=10)

# Create a query entry field and Find button
query_label = ttk.Label(window, text="Query:",style="CustomLabel.TLabel")
query_label.pack()

query_entry = ttk.Entry(window)
query_entry.pack()

# Create a scrollbar
scrollbar = tk.Scrollbar(window)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Create a text area for displaying query results
result_text = tk.Text(window, width=80, height=20)
result_text.pack(padx=10, pady=10)

# Attach the scrollbar to the result text box
result_text.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=result_text.yview)

#BackGround Photo
# root = Tk()
# root.geometry("600x400")

# image = Image.open("image_file_path.png")
# photo = ImageTk.PhotoImage(image)

# label = Label(root, image=photo)
# label.pack()

# Run the Tkinter event loop
window.mainloop()