import os
import requests
from . import libdata
from . import util
from . import model
from . import localization

source_filename = "loraprompttool"

def _clean_relative_model_path(model_path):
    path = str(model_path or "")
    if os.path.isabs(path):
        return path
    return path.lstrip("/\\")

def _candidate_model_paths(model_type, model_path, extensions=("",)):
    clean = _clean_relative_model_path(model_path)
    if os.path.isabs(clean):
        for ext in extensions:
            yield clean + ext
        return
    for folder in libdata.get_model_folders(model_type):
        for ext in extensions:
            yield os.path.join(folder, clean) + ext

def _find_model_file(model_type, model_path, extensions=("",)):
    first = None
    for path in _candidate_model_paths(model_type, model_path, extensions):
        if first is None:
            first = path
        if os.path.isfile(path):
            return path
    return None

def _info_bases(model_type, model_path):
    base, _ = os.path.splitext(_clean_relative_model_path(model_path))
    if os.path.isabs(base):
        yield base
        return
    for folder in libdata.get_model_folders(model_type):
        yield os.path.join(folder, base)

def load_model_bundle_model_path(model_type, model_path):
    """load model bundle embeding by model path

    Parameters
    ----------
    model_type
        model type, you can choose between Checkpoint, TextualInversion, Hypernetwork and LORA
    model_path
        model path
        
    Returns
    -------
    JSON
        a set contains model bundle embeding
    """
    util.console.debug(f"Load model bundle embeding of {model_path} in {model_type}")
    if model_type not in libdata.folders.keys():
        util.console.error("unknow model type: " + model_type, f"{source_filename}.load_model_info_by_model_path")
        return
    
    base, ext = os.path.splitext(model_path)
    model_info_base = base
    if base[:1] == "\\" or base[:1] == "/":
        model_info_base = base[1:]

    model_safetensor_path = _find_model_file(model_type, f"{model_info_base}.safetensors")
    enb_names = set()
    if model_safetensor_path and os.path.isfile(model_safetensor_path):
        import torch
        import safetensors
        with safetensors.safe_open(model_safetensor_path, framework="pt", device="cpu") as f:
            for key in f.keys():
                if key.split(".", 1)[0] == 'bundle_emb':
                    enb_names.add(key.split(".")[1])
    return enb_names


def load_model_info_by_model_path(model_type, model_path):
    """load model information JSON file by model path

    Parameters
    ----------
    model_type
        model type, you can choose between Checkpoint, TextualInversion, Hypernetwork and LORA
    model_path
        model path
        
    Returns
    -------
    JSON
        model information JSON file content
    """
    util.console.debug(f"Load model info of {model_path} in {model_type}")
    if model_type not in libdata.folders.keys():
        util.console.error("unknow model type: " + model_type, f"{source_filename}.load_model_info_by_model_path")
        return
    
    # model_path = subfolderpath + model name + ext. And it always start with a / even there is no sub folder
    base, ext = os.path.splitext(model_path)
    model_info_base = base
    if base[:1] == "\\" or base[:1] == "/":
        model_info_base = base[1:]

    first_path = ""
    for info_base in _info_bases(model_type, model_path):
        for info_ext in libdata.info_ext:
            model_info_filepath = info_base + info_ext
            if not first_path:
                first_path = model_info_filepath
            if os.path.isfile(model_info_filepath):
                return model.load_model_info(model_info_filepath)
    util.console.log("Can not find model info file: " + first_path)
    return

def check_model_state(model_info):
    if model_info is None:
        return "empty"
    if "loading state" in model_info.keys():
        return model_info["loading state"]
    return "ok"

def get_model_error_message(model_info):
    model_state = check_model_state(model_info)
    if model_state == "ok":
        return localization.get_localize_message("Load Successful")
    elif model_state == "error":
        if "message" in model_info.keys():
            if model_info["message"] == "HTTP ERROR":
                status_code = int(model_info["status code"])
                return localization.get_localize_message("HTTP ERROR") + " : " +\
                    status_code + " " +\
                    localization.get_localize_message(libdata.http_state_codes[status_code])
            if model_info["message"] == "fail to load data":
                return localization.get_localize_message(model_info["message"]) + "\n" +\
                    localization.get_localize_message("response") + ":\n" +\
                    model_info["response"]
            return localization.get_localize_message(model_info["message"])
        return localization.get_localize_message("Error")
    return localization.get_localize_message("unknown")

def sent_cors_request(url):
    r : requests.Response
    try:
        r = requests.get(url, headers=libdata.def_headers, proxies=libdata.proxies)
    except Exception as e:
        return {
            "loading state":"error",
            "message": "error, Can not connect to url."
        }
    if not r.ok:
        util.console.error("Get error code: " + str(r.status_code), f"{source_filename}.sent_cors_request")
        util.console.log(r.text)
        return {
            "loading state":"error",
            "message": "HTTP ERROR",
            "status code": r.status_code
        }
    return {
        "loading state":"ok",
        "message": r.text
    }

def get_model_info_by_hash(hash:str):
    """using the model hash to find model information, this will connect to civitAI

    Parameters
    ----------
    hash : str
        the model hash

    Returns
    -------
    JSON
        model information JSON file content
    """
    if not hash:
        util.console.error("hash is empty", f"{source_filename}.get_model_info_by_hash")
        return {
            "loading state":"error",
            "message": "hash calculate failed"
        }
    r : requests.Response
    try:
        r = requests.get(libdata.civitai_apis["hash"]+hash, headers=libdata.def_headers, proxies=libdata.proxies)
    except Exception as e:
        return {
            "loading state":"error",
            "message": "error, Can not connect to CivitAI."
        }
    if not r.ok:
        if r.status_code == 404:
            # this is not a civitai model
            util.console.log("Civitai does not have this model")
            return {
                "loading state":"error",
                "message": "CivitAI does not have this model, or it has been taken down."
            }
        else:
            util.console.error("Get error code: " + str(r.status_code), f"{source_filename}.get_model_info_by_hash")
            util.console.log(r.text)
            return {
                "loading state":"error",
                "message": "HTTP ERROR",
                "status code": r.status_code
            }

    # try to get content
    content = None
    try:
        content = r.json()
    except Exception as e:
        util.console.error("Parse response json failed", f"{source_filename}.get_model_info_by_hash")
        util.console.log(str(e))
        util.console.log("response:")
        util.console.log(r.text)
        return {
            "loading state":"error",
            "message": "fail to load data",
            "response": r.text
        }
    
    if not content:
        util.console.error("error, content from civitai is None", f"{source_filename}.get_model_info_by_hash")
        return {
            "loading state":"error",
            "message": "error, content from CivitAI is None"
        }
    
    return content

def load_model_info_from_Civitai(model_type, model_path):
    """load model information from CivitAI

    Parameters
    ----------
    model_type
        model type, you can choose between Checkpoint, TextualInversion, Hypernetwork and LORA
    model_path
        model path

    Returns
    -------
    JSON
        model information JSON file content
    """
    util.console.debug(f"Load model info of {model_path} in {model_type}")
    if model_type not in libdata.folders.keys():
        util.console.error("unknow model type: " + model_type, f"{source_filename}.load_model_info_from_Civitai")
        return

    model_exts = ("",)
    if f"{model_path}".find(".") < 0:
        model_exts = libdata.exts

    model_base = model_path
    if model_path[:1] == "/" or model_path[:1] == "\\":
        model_base = model_path[1:]

    model_filepath = _find_model_file(model_type, model_base, model_exts)
    if not model_filepath:
        util.console.debug("Can not find model file: " + str(model_path))
        return
    hash = util.gen_file_sha256(model_filepath)
    return get_model_info_by_hash(hash)


def save_model_info_by_model_path(model_info, model_type, model_path):
    """save model information JSON file by model path

    Parameters
    ----------
    model_type
        model type, you can choose between Checkpoint, TextualInversion, Hypernetwork and LORA
    model_path
        model path
    """
    util.console.debug(f"Write model info of {model_path} in {model_type}")
    if model_type not in libdata.folders.keys():
        util.console.error("unknow model type: " + model_type, f"{source_filename}.save_model_info_by_model_path")
        return
    
    # model_path = subfolderpath + model name + ext. And it always start with a / even there is no sub folder
    base, ext = os.path.splitext(model_path)
    model_info_base = base
    if base[:1] == "/" or base[:1] == "\\":
        model_info_base = base[1:]

    # Keep Civitai Helper metadata untouched.  Store this extension's edits in
    # .json (or an existing legacy .info) next to the actual model file.
    target_base = None
    actual_model = _find_model_file(model_type, model_path, ("",) if os.path.splitext(model_path)[1] else libdata.exts)
    if actual_model:
        target_base = os.path.splitext(actual_model)[0]
    else:
        target_base = next(_info_bases(model_type, model_path), None)
    if not target_base:
        util.console.error("Can not resolve model path: " + str(model_path), f"{source_filename}.save_model_info_by_model_path")
        return

    legacy_info = target_base + ".info"
    json_info = target_base + ".json"
    model_info_filepath = legacy_info if os.path.isfile(legacy_info) and not os.path.isfile(json_info) else json_info
    model.write_model_info(model_info_filepath, model_info)