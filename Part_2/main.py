import subprocess
import os
import sys
import time

def run_script(script_name):
    script_path = os.path.join(os.getcwd(), script_name)
    print(f"Running script: {script_path}")
    process = subprocess.Popen([sys.executable, script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    if output:
        print(output.decode("utf-8"))
    if error:
        print(error.decode("utf-8"))
    print(f"Script {script_name} finished with exit code {process.returncode}")

if __name__ == "__main__":
    print("Starting producer...")
    run_script("producer.py")
    print("Starting consumer...")
    consumer_process = subprocess.Popen([sys.executable, "consumer.py"])
    consumer_process.wait()  # Poczekaj na zakończenie procesu consumer.py
    print("Consumer has finished executing.")
