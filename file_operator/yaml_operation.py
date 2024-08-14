import yaml


def yaml_dump(instance_dict: dict) -> str:
    """same as yaml.dump

    Args:
        instance_dict (dict): _description_

    Returns:
        str: _description_
    """
    return yaml.dump(instance_dict)


def read_yaml(path: str) -> None:
    """
    Reads a YAML file and returns its contents as a dictionary.

    Args:
        path (str): Path to the YAML file.

    Returns:
        dict: Contents of the YAML file.
    """
    with open(path, "r") as yml:
        res = yaml.safe_load(yml)
    return res
