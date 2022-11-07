import os

"""
map columns from XML file ( Text element ) to Storage fields
"""
columns = {
    "coolant temperature": "m001",
    "vehicle speed": "m002",
    "gear": "m003",
    "accelerator pedal position": "m004",
    "engine speed": "m005",
    "throttle valve position": "m006",
    "charge air pressure": "m007",
    "intake air temperature": "m008",
    "rail pressure": "m009",
    "ambient pressure": "m010",
    "fuel temperature": "m011",
    "lambda signal before catalytic converter": "m012",
    "status synchronisation camshaft-crankshaft": "m013",
    "operating mode": "m014",
    "engine status": "m015",
    "actuation rate wastegate": "m016",
    "rough running cylinder 1": "m017",
    "rough running cylinder 2": "m018",
    "rough running cylinder 3": "m019",
    "rough running cylinder 4": "m020",
    "rough running cylinder 5": "m021",
    "rough running cylinder 6": "m022",
    "rough running cylinder 7": "m023",
    "rough running cylinder 8": "m024",
    "rough running cylinder 9": "m025",
    "rough running cylinder 10": "m026",
    "rough running cylinder 11": "m027",
    "rough running cylinder 12": "m028",
    "misfire cylinder 1": "m029",
    "misfire cylinder 2": "m030",
    "misfire cylinder 3": "m031",
    "misfire cylinder 4": "m032",
    "misfire cylinder 5": "m033",
    "misfire cylinder 6": "m034",
    "misfire cylinder 7": "m035",
    "misfire cylinder 8": "m036",
    "misfire cylinder 9": "m037",
    "misfire cylinder 10": "m038",
    "misfire cylinder 11": "m039",
    "misfire cylinder 12": "m040",
    "combustion period cylinder 1": "m041",
    "combustion period cylinder 2": "m042",
    "combustion period cylinder 3": "m043",
    "combustion period cylinder 4": "m044",
    "combustion period cylinder 5": "m045",
    "combustion period cylinder 6": "m046",
    "combustion period cylinder 5": "m047",
    "combustion period cylinder 6": "m048",
    "combustion period cylinder 7": "m049",
    "combustion period cylinder 8": "m050",
    "combustion period cylinder 7": "m051",
    "combustion period cylinder 8": "m052",
    "combustion period cylinder 9": "m053",
    "combustion period cylinder 10": "m054",
    "combustion period cylinder 11": "m055",
    "combustion period cylinder 12": "m056",
    "oil temperature": "m057",
    "ambient temperature": "m058",
    "setpoint rail pressure": "m059",
    "setpoint fuel delivery period of quantity control valve": "m060",
    "fuel delivery period of quantity control valve": "m061",
    "duty cycle fuel pump control electronics": "m062",
    "faultbit fuel pump control electronics": "m063",
    "fuel tank level right": "m064",
    "fuel tank level left": "m065",
    "fuel tank level": "m066",
    "differential pressure gasoline particulate filter": "m067",
    "exhaust temperature befor gasoline particulate filter": "m068",
    "exhaust temperature befor gasoline particulate filter 2": "m069",
    "exhaust temperature in gasoline particulate filter": "m070",
    "exhaust temperature in gasoline particulate filter 2": "m071",
    "carbon black mass in gasoline particulate filter": "m072",
    "carbon black mass in gasoline particulate filter 2": "m073",
    "carbon black mass and soot load in gasoline particulate filter 2": "m074",
    "differential pressure gasoline particulate filter 2": "m075"
}


def column_by_value(find_value):
    if find_value == 'time':
        return "time"
    for key, value in columns.items():
        if value == find_value:
            return key
    return None


def move_file(source_file, folder):
    """ move file from [source_file] to [folder] """
    if folder:
        file = os.path.join(folder, os.path.basename(source_file))
        if os.path.exists(source_file):
            os.rename(source_file, file)
    else:
        os.remove(source_file)
