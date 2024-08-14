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
    with open(path, "r") as yml:
        res = yaml.safe_load(yml)
    return res