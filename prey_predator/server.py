from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.UserParam import UserSettableParameter

from prey_predator.agents import Wolf, Sheep, GrassPatch
from prey_predator.model import WolfSheep


def wolf_sheep_portrayal(agent):

    portrayal = {"Filled": "true"}

    if type(agent) is Sheep:

        portrayal["Color"] = "#FFFFFF"
        portrayal["Shape"] = "circle"
        portrayal["r"] = 0.5
        portrayal["Layer"] = 1

    elif type(agent) is Wolf:

        portrayal["Color"] = "#f00020"
        portrayal["Shape"] = "rect"
        portrayal["w"] = 0.5
        portrayal["h"] = 0.5
        portrayal["Layer"] = 2
        

    elif type(agent) is GrassPatch:
        if agent.fully_grown:
            portrayal["Color"] = "#008000"
        else:
            portrayal["Color"] = "#98FB98"
        portrayal["Shape"] = "rect"
        portrayal["w"] = 0.9
        portrayal["h"] = 0.9
        portrayal["Layer"] = 0

    return portrayal


canvas_element = CanvasGrid(wolf_sheep_portrayal, 20, 20, 500, 500)
chart_element = ChartModule(
    [{"Label": "Wolves", "Color": "#f00020"}, {"Label": "Sheep", "Color": "#000000"}]
)

model_params = {
    "grass_regrowth_time": UserSettableParameter(
        "slider", "Grass Regrowth Time", 10, 1, 20
    ),
    "initial_sheep": UserSettableParameter(
        "slider", "Initial Sheep Population", 100, 1, 200
    ),
    "initial_wolves": UserSettableParameter(
        "slider", "Initial Wolf Population", 10, 1, 100
    ),
    "sheep_reproduce": UserSettableParameter(
        "slider", "Sheep Reproduction Rate", 0.05, 0.01, 1.0, 0.01
    ),
    "wolf_reproduce": UserSettableParameter(
        "slider", "Wolf Reproduction Rate", 0.05, 0.01, 1.0, 0.01,
    ),
    "sheep_gain_from_food": UserSettableParameter(
        "slider", "Sheep Gain From Food", 5, 1, 10
    ),
    "wolf_gain_from_food": UserSettableParameter(
        "slider", "Wolf Gain From Food Rate", 25, 1, 50
    )
}

server = ModularServer(
    WolfSheep, [canvas_element, chart_element], "Prey Predator Model", model_params
)
server.port = 8521
