import requests
import sys
import json

# AWS metadata base URL
METADATA_URL = "http://169.254.169.254/latest/meta-data/"

def get_metadata(key=None):
    """
    Fetches metadata for the EC2 instance. If a key is provided, fetch only that key's data.
    :param key: Specific metadata key to retrieve (optional).
    :return: Metadata as a dictionary or specific key value.
    """
    try:
        if key:
            response = requests.get(METADATA_URL + key, timeout=5)
            response.raise_for_status()
            return {key: response.text}
        else:
            # Fetch all metadata keys
            keys_response = requests.get(METADATA_URL, timeout=5)
            keys_response.raise_for_status()
            keys = keys_response.text.splitlines()

            # Fetch metadata for each key
            metadata = {}
            for k in keys:
                try:
                    value_response = requests.get(METADATA_URL + k, timeout=5)
                    value_response.raise_for_status()
                    metadata[k] = value_response.text
                except requests.exceptions.RequestException:
                    metadata[k] = "Unable to retrieve"
            return metadata
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

if __name__ == "__main__":
    # Check if a specific key was passed as an argument
    key_to_retrieve = sys.argv[1] if len(sys.argv) > 1 else None

    # Get metadata
    metadata = get_metadata(key_to_retrieve)

    # Print the metadata in JSON format
    print(json.dumps(metadata, indent=4))
