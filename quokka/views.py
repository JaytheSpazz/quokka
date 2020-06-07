from quokka import app
from flask import request

from quokka.controller.device_info import get_device_info
from quokka.models.apis import get_all_devices, import_devices, export_devices, get_all_hosts, get_all_services


@app.route("/devices", methods=["GET", "POST"])
def devices():

    to_file = request.args.get("export_to")
    from_file = request.args.get("import_from")

    if request.method == "GET":
        return {"devices": get_all_devices()}

    elif request.method == "POST":

        if to_file and from_file:
            return "Specify only 'export_to' or 'import_from' on POST devices, not both."

        if to_file:
            return export_devices(to_file, 'json')
        elif from_file:
            return import_devices(from_file, 'json')

        else:
            return "Must specify either 'export_to' or 'import_from' on POST devices"

    else:
        return "Invalid request method"


@app.route("/device", methods=["GET"])
def device():

    if request.method == "GET":

        device_name = request.args.get("device")
        requested_info = request.args.get("info")
        live = request.args.get("live")

        if not device_name or not requested_info:
            return "Must provide device and info", 400
        if not live:
            get_live_info = False
        else:
            if live.lower() not in {"true", "false"}:
                return "Value of 'live', if specified, must be 'true' or 'false'"
            else:
                get_live_info = bool(live)

        status, result_info = get_device_info(device_name, requested_info, get_live_info)
        if status == "success":
            return result_info, 200
        else:
            return result_info, 406


@app.route("/hosts", methods=["GET"])
def hosts():

    if request.method == "GET":
        return {"hosts": get_all_hosts()}

    else:
        return "Invalid request method"


@app.route("/services", methods=["GET"])
def services():

    if request.method == "GET":
        return {"services": get_all_services()}

    else:
        return "Invalid request method"
