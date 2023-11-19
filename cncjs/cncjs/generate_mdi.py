from cncjs.config_models import Config, State, Controller

from jinja2 import Environment, FileSystemLoader


# example object
# {
#     "id": "87401cc7-bd8b-4463-b6e2-e8992e4f3e78",
#     "name": "mycustom command",
#     "command": "the command\nthecommand line 2",
#     "grid": {
#         "xs": 6
#     }
# },

def generate_move_buttons():
    """return a list of mdi objects based on cnc machine outer bounds"""
    # jinja setup
    environment = Environment(loader=FileSystemLoader("cncjs/gcode_templates/"))
    template = environment.get_template("move_to_location.gcode.template")

    lower_bound_x = -3
    upper_bound_x = -800

    lower_bound_y = -3
    upper_bound_y = -800

    buttons_to_render = {
        "Far left": (upper_bound_x, lower_bound_y),
        "Far center": (upper_bound_x / 2, lower_bound_y),
        "Far right": (lower_bound_x, lower_bound_y),
        "Center left": (upper_bound_x, upper_bound_y / 2),
        "Center center": (upper_bound_x / 2, upper_bound_y / 2),
        "Center right": (lower_bound_x, upper_bound_y / 2),
        "Near left": (upper_bound_x, upper_bound_y),
        "Near center": (upper_bound_x / 2, upper_bound_y),
        "Near right": (lower_bound_x, upper_bound_y),
    }
    z_safe_height = -3

    list_of_objects = []

    for button, button_value in buttons_to_render.items():
        command = template.render(
            z_safe_height=z_safe_height, x_loc=button_value[0], y_loc=button_value[1]
        )
        list_of_objects.append({"name": button, "command": command, "grid": {"xl": 4}})

    return list_of_objects

def generate_bitsetter():
    environment = Environment(loader=FileSystemLoader("cncjs/gcode_templates/"))
    initial = environment.get_template("inital_tool_bitsetter.gcode")
    swap  = environment.get_template("swap_tool_bitsetter.gcode")
    
    return [
        {"name": "Initial Tool Setup", "command": initial.render(), "grid": {"lg": 6}},
        {"name": "Swap Tool", "command": swap.render(), "grid": {"lg": 6}},
    ]


c = Config(
    watchDirectory="/home/alan/cnc/watchdir",
    accessTokenLifetime="30d",
    allowRemoteAccess=True,
    state=State(
        checkForUpdates=True, controller=Controller(exception={"ignoreErrors": False})
    ),
    secret="$2a$10$N2H7w.UnG78qCP8swWFeZO",
    macros=[],
    mdi= generate_bitsetter() + generate_move_buttons(),
)


print(c.model_dump_json(indent=2))
