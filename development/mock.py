from typing import Dict, List


class DynamicModule:
    def __init__(self, name: str, id: str):
        self.name = name
        self.id = id


def create_class(class_name: str, attributes: Dict[str, str]) -> type:
    return type(class_name, (DynamicModule,), attributes)


def get_ids(full_path="torch.nn.Module") -> List[str]:
    ids = []
    split = full_path.split(".")
    for i in range(len(split)):
        ids.append(".".join(split[: i + 1]))
    return ids


def create_modules(ids) -> Dict[str, DynamicModule]:
    modules = {}

    for id in ids:
        if id not in modules.keys():
            name = id.split(".")[-1]
            attributes = {
                "id": id,
                "name": name,
            }
            modules[id] = create_class(id, attributes)
    return modules


def collect_children(id, modules: Dict[str, DynamicModule]) -> List[DynamicModule]:
    children = []
    for candidate_id, module in modules.items():
        if candidate_id.startswith(id):
            parent_level = id.count(".")
            candidate_level = candidate_id.count(".")
            if candidate_level - parent_level == 1:
                children.append(module)
    return children


def set_children(parent, children: List[DynamicModule]) -> None:
    for child in children:
        setattr(parent, child.name, child)


def generate_all_ids(full_ids) -> List[str]:
    ids = []
    for full_id in full_ids:
        ids.extend(get_ids(full_id))
    return ids


def generate_module_complete(full_ids):
    ids = generate_all_ids(full_ids)

    modules = create_modules(ids)

    for id, module in modules.items():
        children = collect_children(id, modules)
        set_children(module, children)

    return modules


full_ids = ["torch.nn.Module", "torch.Tensor"]

modules = generate_module_complete(full_ids)

torch = modules["torch"]
