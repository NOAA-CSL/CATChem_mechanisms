import os
import json
import subprocess
import sys

def test_mechanism(mech_dir):
    print(f"Testing mechanism in {mech_dir}...")
    config_yaml_path = os.path.join(mech_dir, "config.yaml")
    if not os.path.exists(config_yaml_path):
        print(f"No config.yaml found in {mech_dir}")
        return False

    music_box_config = {
        "box model options": {
            "grid": "box",
            "chemistry time step [min]": 1.0,
            "output time step [min]": 1.0,
            "simulation length [day]": 0.001
        },
        "initial conditions": {},
        "environmental conditions": {
            "temperature": {
                "initial value [K]": 298.15
            },
            "pressure": {
                "initial value [Pa]": 101325.0
            }
        },
        "model components": [
            {
                "type": "CAMP",
                "configuration file": "config.yaml"
            }
        ]
    }

    config_file_path = os.path.join(mech_dir, "music_box_config_temp.json")
    with open(config_file_path, 'w') as f:
        json.dump(music_box_config, f)

    try:
        result = subprocess.run(
            ["music_box", "-c", "music_box_config_temp.json"],
            cwd=mech_dir,
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            print(f"Error running music-box for {mech_dir}:")
            print(result.stderr)
            print(result.stdout)
            return False
        else:
            print(f"Successfully ran mechanism in {mech_dir}")
            return True
    except Exception as e:
        print(f"Exception while testing {mech_dir}: {e}")
        return False
    finally:
        if os.path.exists(config_file_path):
            os.remove(config_file_path)

def main():
    mech_root = "mech"
    if not os.path.exists(mech_root):
        print(f"Mechanism root directory '{mech_root}' not found.")
        sys.exit(1)

    success = True
    mechanisms_found = 0
    for entry in os.listdir(mech_root):
        mech_dir = os.path.join(mech_root, entry)
        if os.path.isdir(mech_dir):
            mechanisms_found += 1
            if not test_mechanism(mech_dir):
                success = False

    if mechanisms_found == 0:
        print("No mechanisms found to test.")
        sys.exit(1)

    if not success:
        print("Some mechanisms failed to run.")
        sys.exit(1)
    else:
        print("All mechanisms passed.")

if __name__ == "__main__":
    main()
