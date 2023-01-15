from dataclasses import dataclass
from enum import Enum
from typing import Union, NamedTuple, List
from flask import Flask, request    # type: ignore

# SpaceCowboy models a cowboy in our super amazing system
@dataclass
class SpaceCowboy:
    name: str
    lassoLength: int

# SpaceAnimal models a single animal in our amazing system
@dataclass
class SpaceAnimal:
    # SpaceAnimalType is an enum of all possible space animals we may encounter
    class SpaceAnimalType(Enum):
        PIG = "pig"
        COW = "cow"
        FLYING_BURGER = "flying_burger"

    type: SpaceAnimalType

# SpaceEntity models an entity in the super amazing (ROUND UPPER 100) system
@dataclass
class SpaceEntity:
    class Location(NamedTuple):
        x: int
        y: int

    metadata: Union[SpaceCowboy, SpaceAnimal]
    location: Location

# ==== HTTP Endpoint Stubs ====
app = Flask(__name__)
space_database: List[SpaceEntity] = []

# ==== Note ====
# isinstance did not work when comparing between dataclasses (e.g. SpaceEntity) and a dictionary object
# assumes inputs in the form of (for example):
# {
#     "entities": [
#         {
#             "type": "space_cowboy",
#             "metadata": { "name": "Buckaroo Banzai", "lassoLength": 10 },
#             "location": { "x": 1, "y": 2 }
#         },
#         {
#             "type": "space_animal",
#             "metadata": { "type": "flying_burger" },
#             "location": { "x": 3, "y": 4 }
#         }
#     ]
# }

# ==== Helper Functions ====
def isCowboyType(entity):
    if "type" in entity.keys():
        if entity["type"] == "space_cowboy":
            return True
        else:
            return False

def isCowboyMetadata(entity):
    if "metadata" in entity.keys():
        if isinstance(entity["metadata"]["name"], str) and isinstance(entity["metadata"]["lassoLength"], int):
            return True
        else:
            return False

def isLocation(entity):
    if "location" in entity.keys():
        if isinstance(entity["location"]["x"], int) and isinstance(entity["location"]["y"], int):
            return True
        else:
            return False

def isAnimalType(entity):
    if "type" in entity.keys():
        if entity["type"] == "space_animal":
            return True
        else:
            return False

def isAnimalMetadata(entity):
    if "metadata" in entity.keys():
        if entity["metadata"]["type"] in ["pig", "cow", "flying_burger"]:
            return True
        else:
            return False

# checking if the entity is a space entity! (part 1)
def isSpaceEntity(entity):
    # check that the metadata fits either SpaceCowboy or SpaceAnimal type
    if isCowboyType(entity):
        if isCowboyMetadata(entity):
            if isLocation(entity):
                return True
    elif isAnimalType(entity):
        if isAnimalMetadata(entity):
            if isLocation(entity):
                return True
    else:
        return False

# ==== Endpoints ====
# the POST /entity endpoint adds an entity to your global space database
@app.route('/entity', methods=['POST'])
def create_entity():
    info = request.get_json()
    entities = info["entities"]

    for entity in entities:
        if isSpaceEntity(entity):
            # appending SpaceEntities
            space_database.append({
                "type": entity["type"],
                "metadata": entity["metadata"],
                "location": entity["location"]
            })
    return {}

# lasooable returns all the space animals a space cowboy can lasso given their name
@app.route('/lassoable', methods=['GET'])
def lassoable():
    # TODO: implement me
    pass


# DO NOT TOUCH ME, thanks :D
if __name__ == '__main__':
    app.run(debug=True, port=8080)
