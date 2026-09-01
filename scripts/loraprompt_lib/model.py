import os
import re
import json
from . import util
from . import libdata
from modules import shared

source_filename = "model"

def get_db_models():
    rgx = re.compile(r"\[.*\]")
    output = [""]
    try:
        out_dir = libdata.dreambooth_models_path
        if os.path.exists(out_dir):
            for item in os.listdir(out_dir):
                check_path = os.path.join(out_dir, item)
                if os.path.isdir(check_path) and not rgx.search(item):
                    json_path = os.path.join(check_path, libdata.dreambooth_setting_file_name)
                    if not os.path.isfile(json_path):
                        continue
                    output.append(item)
    except Exception:
        pass
    return output

def get_db_model_setting(model_name):
    try:
        model_path = os.path.join(libdata.dreambooth_models_path, model_name, libdata.dreambooth_setting_file_name)
        return load_model_info(model_path)
    except Exception as e1:
        return

def _cmd_paths(*names):
    paths = []
    for name in names:
        value = getattr(shared.cmd_opts, name, None)
        if not value:
            continue
        if isinstance(value, (list, tuple, set)):
            paths.extend(value)
        else:
            paths.append(value)
    return paths

def _existing_or_default(paths, default_path):
    out = []
    for path in paths:
        if path and os.path.isdir(path) and path not in out:
            out.append(path)
    if default_path and os.path.isdir(default_path) and default_path not in out:
        out.append(default_path)
    return out or [default_path]

def get_custom_model_folder():
    """Load model folders from A1111 / Forge / Forge Neo safely."""
    util.console.log("Get Custom Model Folder (A1111/Forge/Forge Neo compatible)")

    defaults = dict(libdata.folders)

    ti = _existing_or_default(_cmd_paths("embeddings_dir"), defaults["ti"])
    hyper = _existing_or_default(_cmd_paths("hypernetwork_dir"), defaults["hyper"])
    ckp = _existing_or_default(_cmd_paths("ckpt_dirs", "ckpt_dir"), defaults["ckp"])
    lora = _existing_or_default(_cmd_paths("lora_dirs", "lora_dir"), defaults["lora"])
    lyco = _existing_or_default(_cmd_paths("lyco_dir"), defaults["lyco"])

    libdata.set_model_folders("ti", ti)
    libdata.set_model_folders("hyper", hyper)
    libdata.set_model_folders("ckp", ckp)
    libdata.set_model_folders("lora", lora)
    libdata.set_model_folders("lyco", lyco)

    for model_type in ("ti", "hyper", "ckp", "lora", "lyco"):
        util.console.debug(f"Model folders [{model_type}]: {libdata.get_model_folders(model_type)}")

def write_model_info(path, model_info):
    """write model JSON data

    Parameters
    ----------
    path
        file path to write
    model_info
        data to write
    """
    util.console.log("Write model info to file: " + path)
    with open(os.path.realpath(path), 'w') as f:
        f.write(json.dumps(model_info, indent=4))


def load_model_info(path):
    """load model JSON data

    Parameters
    ----------
    path
        file path to load
        
    Returns
    -------
    JSON
        loadded JSON data
    """
    model_info = None
    try:
        with open(os.path.realpath(path), 'r') as f:
            try:
                model_info = json.load(f)
            except Exception as e:
                util.console.error("Selected file is not json: " + path, f"{source_filename}.load_model_info")
                util.console.log(e)
                return
    except Exception as e1:
        util.console.error("file not found: " + path, f"{source_filename}.load_model_info")
        return
    return model_info

