import json
import os


def remove_result_key(folder_path):
    """
    Remove the "result" key from all JSON files in a specified folder.

    Args:
        folder_path (str): Path to the folder containing JSON files.

    Returns:
        None
    """
    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, "r+") as file:
                data = json.load(file)
                for query in data["queries"]:
                    if "result" in query["answer"]:
                        del query["answer"]["result"]
                file.seek(0)
                json.dump(data, file, indent=4)
                file.truncate()


# Example usage:
folder_path = "es_instruct/dump_json_copy"
remove_result_key(folder_path)
