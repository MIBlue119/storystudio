import json
import os


def generate_caption(shots_content, output_dir):
    shots_content = shots_content["shots_content"]
    os.makedirs(output_dir, exist_ok=True)
    # Export to json
    with open(os.path.join(output_dir, "shots_content.json"), "w") as f:
        json.dump(shots_content, f, indent=4)
