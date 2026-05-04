from .yolo_model import predict

class UIState:
    def __init__(self):
        self.hp_box = None
        self.stamina_box = None
        self.death_box = None
        self.hp_percent = None
        self.stamina_precent = None
        self.player_dead = False

def detect_ui(frame, tracker):
    result = predict(frame, conf=0.50)
    state = UIState()

    for box in result.boxes:
        cls = int(box.cls[0])
        x1,y1,x2,y2 = map(int, box.xyxy[0])

        if cls == 0:  # HP_BAR
            state.hp_box = (x1,y1,x2,y2)

        elif cls == 1:  # STAMINA_BAR
            state.stamina_box = (x1,y1,x2,y2)

        elif cls == 2:  # YOU_DIED
            state.death_box = (x1,y1,x2,y2)
            state.player_dead = True

        conf = float(box.conf[0])
        print(cls, conf, (x1,y1,x2,y2))

    state.hp_box = tracker.stabilize_hp_box(state.hp_box)
    state.stamina_box = tracker.stabilize_stamina_box(state.stamina_box)

    if state.hp_box:
        from .extract_bar_strict import extract_bar_strip
        from .hp_analyzer import calculate_hp       

        strict = extract_bar_strip(frame, state.hp_box)
        state.hp_percent = calculate_hp(strict)

    if state.stamina_box:
        from .extract_bar_strict import extract_bar_strip
        from .stamina_analyzer import calculate_stamina       

        strict = extract_bar_strip(frame, state.stamina_box)
        state.stamina_precent = calculate_stamina(strict)

    return state
