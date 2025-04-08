import streamlit as st
import numpy as np
import time

# Set the title of the app
st.title("ED Hospital Simulation (Real-Time Prototype)")

# Input fields for simulation parameters
arrival_rate = st.number_input("Arrival Rate (λ)", min_value=0.1, value=1.0, step=0.1)
service_rate = st.number_input("Service Rate (μ)", min_value=0.1, value=1.0, step=0.1)
sim_time = st.number_input("Simulation Duration (in seconds)", min_value=1, value=30)

# We'll store our patients list in session state so that it persists between reruns
if "patients" not in st.session_state:
    st.session_state.patients = []

# Placeholders for updating simulation information and table in real-time
sim_status_placeholder = st.empty()
table_placeholder = st.empty()

# Function to generate a new patient with whole number times
def add_new_patient():
    # For whole numbers, we use randint
    # For inter_arrival, let’s assume a random value between 1 and 5 seconds:
    inter_arrival = np.random.randint(1, 6)
    
    # The arrival time is computed relative to the last patient (or 0 for first)
    if st.session_state.patients:
        last_arrival = st.session_state.patients[-1]["arrival_time"]
    else:
        last_arrival = 0
    arrival_time = last_arrival + inter_arrival
    
    # Service time, similarly, is a random whole number between 1 and 5 seconds
    service_time = np.random.randint(1, 6)
    
    # Randomly assign priority (1 is highest, 3 is lowest)
    priority = int(np.random.choice([1, 2, 3]))
    
    # Build a patient dictionary
    new_patient = {
        "id": len(st.session_state.patients) + 1,
        "inter_arrival": inter_arrival,
        "arrival_time": arrival_time,
        "service_time": service_time,
        "priority": priority
    }
    st.session_state.patients.append(new_patient)

# When the simulation starts, run the real-time simulation loop.
if st.button("Start Simulation"):
    # Clear previous patient list if any
    st.session_state.patients = []
    
    # Initialize timing
    simulation_duration = int(sim_time)  # simulation duration in seconds (whole number)
    start_time = time.time()
    remaining = simulation_duration

    # Run simulation in a loop until timer runs out
    while remaining > 0:
        # Update the countdown timer (in seconds)
        current_time = time.time()
        elapsed = int(current_time - start_time)
        remaining = simulation_duration - elapsed
        
        # With a fixed probability, add a new patient
        # (You can adjust this probability or use your own arrival logic)
        if np.random.random() < 0.5:  # 50% chance to add a patient at each iteration
            add_new_patient()
        
        # Update our placeholders:
        sim_status_placeholder.write(f"Time Remaining: {remaining} seconds")
        # Use st.table which auto aligns headers. We build a list of lists for display.
        if st.session_state.patients:
            table_data = [
                [p["id"], p["inter_arrival"], p["arrival_time"], p["service_time"], p["priority"]]
                for p in st.session_state.patients
            ]
            # Define headers for clarity
            headers = ["ID", "Inter-Arrival", "Arrival Time", "Service Time", "Priority"]
            # We create a new data structure (list of dicts) so the table shows headers correctly.
            table_dict = [dict(zip(headers, row)) for row in table_data]
            table_placeholder.table(table_dict)
        else:
            table_placeholder.write("No patients generated yet.")
        
        # Sleep for 1 second to control the update rate (simulate the passing of time)
        time.sleep(1)
    
    sim_status_placeholder.write("Simulation Ended.")
