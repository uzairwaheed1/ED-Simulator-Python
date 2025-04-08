import streamlit as st
import numpy as np
import time

# Set the title of the app
st.title("ED Hospital Simulation (Real-Time Prototype)")

# Input fields for simulation parameters
arrival_rate = st.number_input("Arrival Rate (λ)", min_value=0.1, value=1.0, step=0.1)
service_rate = st.number_input("Service Rate (μ)", min_value=0.1, value=1.0, step=0.1)
sim_time = st.number_input("Simulation Duration (in seconds)", min_value=1, value=30)

# Store patients in session state so that data persists over reruns
if "patients" not in st.session_state:
    st.session_state.patients = []

# Placeholders for real-time simulation status and table
sim_status_placeholder = st.empty()
table_placeholder = st.empty()

# Placeholder for the sorted (priority-based) table display
sorted_table_placeholder = st.empty()

# Function to generate a new patient with whole number times
def add_new_patient():
    # Generate inter_arrival as a whole number between 1 and 5 seconds
    inter_arrival = np.random.randint(1, 6)
    
    # Calculate arrival time relative to the last patient, or 0 for the first patient
    if st.session_state.patients:
        last_arrival = st.session_state.patients[-1]["arrival_time"]
    else:
        last_arrival = 0
    arrival_time = last_arrival + inter_arrival
    
    # Generate a whole number service time between 1 and 5 seconds
    service_time = np.random.randint(1, 6)
    
    # Random priority: 1 (highest), 2, or 3 (lowest)
    priority = int(np.random.choice([1, 2, 3]))
    
    # Create a new patient dictionary
    new_patient = {
        "id": len(st.session_state.patients) + 1,
        "inter_arrival": inter_arrival,
        "arrival_time": arrival_time,
        "service_time": service_time,
        "priority": priority
    }
    st.session_state.patients.append(new_patient)

# When the simulation starts, run the real-time simulation loop
if st.button("Start Simulation"):
    # Clear any previously generated patients
    st.session_state.patients = []
    
    # Clear previous sorted table if any.
    sorted_table_placeholder.empty()
    
    # Initialize simulation timing variables
    simulation_duration = int(sim_time)  # total simulation duration in seconds
    start_time = time.time()
    remaining = simulation_duration

    # Run simulation until the remaining time is 0
    while remaining > 0:
        # Update elapsed time and compute remaining time
        current_time = time.time()
        elapsed = int(current_time - start_time)
        remaining = simulation_duration - elapsed
        
        # With a fixed probability, add a new patient (50% chance per iteration)
        if np.random.random() < 0.5:
            add_new_patient()
        
        # Update the simulation status (timer display)
        sim_status_placeholder.write(f"Time Remaining: {remaining} seconds")
        
        # Prepare table data from patients list for proper header alignment 
        if st.session_state.patients:
            table_data = [
                [p["id"], p["inter_arrival"], p["arrival_time"], p["service_time"], p["priority"]]
                for p in st.session_state.patients
            ]
            headers = ["ID", "Inter-Arrival", "Arrival Time", "Service Time", "Priority"]
            table_dict = [dict(zip(headers, row)) for row in table_data]
            table_placeholder.table(table_dict)
        else:
            table_placeholder.write("No patients generated yet.")
        
        # Sleep for one second to simulate real time passing
        time.sleep(1)
    
    # Indicate that the simulation has ended.
    sim_status_placeholder.write("Simulation Ended.")
    
    # --- New Part: Sorting the Data by Priority ---
    # Sort patients first by priority (ascending: 1, 2, 3).  
    # Optionally, sort by arrival time if priorities are equal.
    sorted_patients = sorted(
        st.session_state.patients,
        key=lambda p: (p["priority"], p["arrival_time"])
    )
    
    # Prepare sorted table data
    sorted_table_data = [
        [p["id"], p["inter_arrival"], p["arrival_time"], p["service_time"], p["priority"]]
        for p in sorted_patients
    ]
    headers_sorted = ["ID", "Inter-Arrival", "Arrival Time", "Service Time", "Priority"]
    sorted_table_dict = [dict(zip(headers_sorted, row)) for row in sorted_table_data]
    
    # Display the sorted table
    sorted_table_placeholder.subheader("Patients Sorted by Priority")
    sorted_table_placeholder.table(sorted_table_dict)
