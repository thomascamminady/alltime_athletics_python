from dataclasses import dataclass


@dataclass
class Event:
    name: str
    distance: float
    is_track: bool
    has_hurdles: bool
    distance_type: str


event_list: list[Event] = [
    Event("60 metres", 60, True, False, "sprint"),
    Event("100 metres", 100, True, False, "sprint"),
    Event("100m hurdles", 100, True, True, "sprint"),
    Event("100 yards", 91.44, True, False, "sprint"),
    Event("110m hurdles", 110, True, True, "sprint"),
    Event("200 metres", 200, True, False, "sprint"),
    Event("200m hurdles", 200, True, True, "sprint"),
    Event("300 metres", 300, True, False, "sprint"),
    Event("400 metres", 400, True, False, "sprint"),
    Event("400m hurdles", 400, True, True, "sprint"),
    Event("600 metres", 600, True, False, "middle distance"),
    Event("800 metres", 800, True, False, "middle distance"),
    Event("1000 metres", 1000, True, False, "middle distance"),
    Event("1500 metres", 1500, True, False, "middle distance"),
    Event("1 Mile", 1609, True, False, "middle distance"),
    Event("2 Miles", 2 * 1609, True, False, "middle distance"),
    Event("2000 metres", 2000, True, False, "middle distance"),
    Event("2000m steeplechase", 2000, True, True, "middle distance"),
    Event("3000 metres", 3000, True, False, "middle distance"),
    Event("3000m steeplechase", 3000, True, True, "middle distance"),
    Event("5000 metres", 5000, True, False, "long distance"),
    Event("10km road", 10000, False, False, "long distance"),
    Event("10 km race walk", 10000, False, False, "long distance"),
    Event("10000 metres", 10000, True, False, "long distance"),
    Event("10000 meters track walk", 10000, True, False, "long distance"),
    Event("15km road", 15000, False, False, "long distance"),
    Event("20km road", 20000, False, False, "long distance"),
    Event("20 km race walk", 20000, False, False, "long distance"),
    Event("25 000m track", 25000, True, False, "long distance"),
    Event("30 000m track", 30000, True, False, "long distance"),
    Event("30km road", 30000, False, False, "long distance"),
    Event("half-marathon", 21097.5, False, False, "long distance"),
    Event("marathon", 42195, False, False, "long distance"),
    Event("50 km race walk", 50000, False, False, "long distance"),
    Event("100km road", 100000, False, False, "long distance"),
    Event("One hour run", 3600, True, False, "long distance"),
    Event("5000 metres track walk", 5000, True, False, "long distance"),
]
