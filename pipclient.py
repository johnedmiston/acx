import os
import time

# Define paths for communicating with Audacity via named pipes
pipe_in_path = "/tmp/audacity_script_pipe.to.501"  # Pipe to send commands to Audacity
pipe_out_path = "/tmp/audacity_script_pipe.from.501"  # Pipe to receive responses from Audacity

# Open the communication pipes
pipe_in = open(pipe_in_path, 'w')  # Open the command pipe in write mode
# pipe_out = open(pipe_out_path, 'r')  # Open the response pipe in read mode
pipe_out = open(pipe_out_path, 'r', buffering=1)

#!! added later for debugging purposes:# Add extra debugging for pipe_out
print(f"Debug: pipe_out closed? {pipe_out.closed}")
print(f"Debug: pipe_out mode: {pipe_out.mode}")
print(f"Debug: pipe_out name: {pipe_out.name}")


#!! Function to send commands to Audacity
# def send_command(command):
#     pipe_in.write(command + '\n')  # Write command to the pipe
#     pipe_in.flush()  # Ensure command is sent immediately


def send_command(command):
    print(f"Debug: Sending command -> {command}")  # Debug print
    pipe_in.write(command + '\n')
    pipe_in.flush()


#!! Function to receive responses from Audacity

# def get_response():
#     pipe_out.flush()
#     return pipe_out.readline()  # Read and return the response from Audacity

# def get_response():
#     pipe_out.flush()
#     response = []
#     while True:
#         line = pipe_out.readline().strip()
#         if not line:
#             break
#         response.append(line)
#     return "\n".join(response)

# def get_response():
#     pipe_out.flush()
#     response = []
#     while True:
#         line = pipe_out.readline().strip()
#         if not line:
#             print("Debug: Empty line received.")  # Add debug print
#             break
#         print(f"Debug: Received line -> {line}")  # Add debug print
#         response.append(line)
#     return "\n".join(response)


# Removed flush, added delay in an effort to give audacity time to respond
# def get_response():
#     response = []
#     timeout = time.time() + 2  # Wait up to 2 seconds
#     while time.time() < timeout:
#         line = pipe_out.readline().strip()
#         if line:
#             print(f"Debug: Received line -> {line}")
#             response.append(line)
#         else:
#             print("Debug: Empty line received.")
#             break
#     return "\n".join(response)

# def get_response():
#     time.sleep(1)  # Delay before reading to give Audacity time to respond
#     response = []
#     while True:
#         line = pipe_out.readline().strip()
#         if not line:
#             print("Debug: Empty line received.")
#             break
#         print(f"Debug: Received line -> {line}")
#         response.append(line)
#     return "\n".join(response)

def get_response():
    response = []
    while True:
        line = pipe_out.readline().strip()
        if not line:
            print("Debug: Empty line received.")  # When no new data is available
            continue
        print(f"Debug: Received line -> {line}")
        response.append(line)
        
        # Stop reading when "BatchCommand finished: OK" is found
        if "BatchCommand finished: OK" in line:
            print("Debug: End of response detected.")
            break
    return "\n".join(response)




# Test the setup with a simple command
send_command("Help")
# send_command("GetInfo") #!! crashes app as there is no such command.
print("Response from Audacity:", get_response())  # Debugging output

# Clean up: Close the pipes after communication is complete
pipe_in.close()  # Close the command pipe
pipe_out.close()  # Close the response pipe
