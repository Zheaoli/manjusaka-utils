import yaml
from scripts.am.config import Route
from scripts.am.validator import convert_to_validator_route
from scripts.am.validator.route import Route as ValidatorRoute
from rich.tree import Tree
from rich import print as rprint


def load_config(config_file_path: str) -> dict:
    with open(config_file_path, "r") as f:
        config = yaml.safe_load(f)
    return config


def alert_rule_parser(config_file_path: str):
    origin_config = load_config(config_file_path)
    if "route" not in origin_config:
        raise ValueError("route is not in config file")
    routes = [Route.model_validate(origin_config["route"])]
    parsed_routes = convert_to_validator_route(routes)
    tree = Tree("root")
    print_tree_view(parsed_routes, tree)
    rprint(tree)


def print_tree_view(routes: list[ValidatorRoute], tree_object: Tree):
    for route in routes:
        new_tree_object = tree_object.add(str(route))
        print_tree_view(route.routes, new_tree_object)
