class Planet:
    def __init__(self, id, name, description, distance_from_sun):
        self.id = id
        self.name = name
        self.description = description
        self.distance_from_sun = distance_from_sun

    def __repr__(self):
        return f"Planet(name={self.name}, description={self.description}, distance_from_sun={self.distance_from_sun})"

planets = [
        Planet(1, "Mercury", "The smallest planet in our solar system and closest to the Sun.", 57.9),
        Planet(2, "Venus", "The second planet from the Sun and has a thick atmosphere.", 108.2),
        Planet(3, "Earth", "The third planet from the Sun and the only known planet to support life.", 149.6),
    ]