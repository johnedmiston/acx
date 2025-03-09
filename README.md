# acx
Create an Audacity Nyquist audio plugin using Python or LISP that will adjust audio t omeet  the standard for audiobooks in Amazon Audible
Plugin should be compliant with the following standards: https://help.acx.com/s/article/what-are-the-acx-audio-submission-requirements 
Script should be able to take an MP3 audio file and then make it mono, then elminate the background noise, while leaving some, and adjust volume levels and so on to meet the ACX standards.
The audio software we are suing is Audacity: https://www.audacityteam.org/ and here is a link about dveloping plugins https://plugins.audacityteam.org/contributing/developing-your-own-plugins-and-scripts
And the plugin will be a Nyquist plugin for Audacity and we hope to contribute it to the open-source community under an appropriate license. 



# Resources

Explore plug-in examples and Nyquist programming at [**AudioNyq.com**](https://audionyq.com).

For an existing plugin that checks ACX standards, see the ACX Check at [Audacity Plugin Library](https://plugins.audacityteam.org/analyzers/analysis-plugins#acx-check). This resource is useful for comparing and understanding script configurations for Nyquist plugins.

Explore advanced scripting and tool integration for Audacity with Steve Daulton's work, which includes the enhanced `pipeclient.py`, a Python module for controlling Audacity. This repository offers valuable insights and code that could be instrumental in developing Python scripts for audio processing tasks. Check out the repository [here](https://github.com/SteveDaulton).



# Debugging the Audacity Communication Script

This section details the step-by-step debugging process for the script used to communicate with Audacity via named pipes.

---

## 3/7/2025

### **Problem**
The script was successfully sending the `"Help"` command to Audacity, but it was failing to capture any response. The `get_response()` function kept returning "Empty line received," or the script would hang indefinitely waiting for input.

---

### **Debugging Process**

1. **Initial Verification**:
   - Confirmed that Audacity's `mod-script-pipe` module was enabled in **Preferences → Modules**.
   - Manually tested the pipes by sending a command directly:
     ```bash
     echo "Help" > /tmp/audacity_script_pipe.to.501
     cat /tmp/audacity_script_pipe.from.501
     ```
   - Verified that the correct response was returned manually, indicating that the pipes and Audacity were functional.

2. **Added Debugging Information**:
   - Inserted debug prints to verify the state of `pipe_out`:
     ```python
     print(f"Debug: pipe_out closed? {pipe_out.closed}")
     print(f"Debug: pipe_out mode: {pipe_out.mode}")
     print(f"Debug: pipe_out name: {pipe_out.name}")
     ```
   - Confirmed that `pipe_out` was open, in read mode (`'r'`), and correctly pointing to `/tmp/audacity_script_pipe.from.501`.

3. **Timing Hypothesis**:
   - Suspected that the script was reading the pipe too early before Audacity had finished processing the command.
   - Introduced a delay using `time.sleep(1)` in the `get_response()` function to give Audacity time to respond. However, the script still hung indefinitely.

4. **Monitored the Pipe in Real Time**:
   - Used `tail -f` to monitor `/tmp/audacity_script_pipe.from.501` while running the script:
     ```bash
     tail -f /tmp/audacity_script_pipe.from.501
     ```
   - Observed that the correct response was being written to the pipe by Audacity, but the script was not reading it properly.

5. **Identified the End Marker**:
   - Noted that Audacity’s response always ends with `"BatchCommand finished: OK"`.
   - Determined that the script needed to detect this marker to stop reading and avoid hanging.

6. **Solution Implementation**:
   - Updated the `get_response()` function to detect the `"BatchCommand finished: OK"` marker:
     ```python
     def get_response():
         response = []
         while True:
             line = pipe_out.readline().strip()
             if not line:
                 print("Debug: Empty line received.")
                 continue
             print(f"Debug: Received line -> {line}")
             response.append(line)
             if "BatchCommand finished: OK" in line:
                 print("Debug: End of response detected.")
                 break
         return "\n".join(response)
     ```

7. **Final Test**:
   - Ran the updated script:
     ```bash
     python3 pipclient.py
     ```
   - Verified that the `"Help"` command was successfully sent, and the response was correctly captured and printed without hanging.

---

### **Results**
The script now works as expected:
- Sends the `"Help"` command to Audacity.
- Captures and prints the full response.
- Stops reading once the `"BatchCommand finished: OK"` marker is detected.

Debugging complete!
