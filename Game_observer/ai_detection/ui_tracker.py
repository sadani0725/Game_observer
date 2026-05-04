class UIStateTracker:
    def __init__(self):
        self.last_hp_box = None
        self.last_stamina_box = None

    def stabilize_hp_box(self, new_box):
        if new_box is None:
            return self.last_hp_box

        if self.last_hp_box is None:
            self.last_hp_box = new_box
            return new_box

        x1 = int((self.last_hp_box[0] + new_box[0]) / 2)
        y1 = int((self.last_hp_box[1] + new_box[1]) / 2)
        x2 = int((self.last_hp_box[2] + new_box[2]) / 2)
        y2 = int((self.last_hp_box[3] + new_box[3]) / 2)

        stabilized = (x1, y1, x2, y2)
        self.last_hp_box = stabilized

        return stabilized
    
    def stabilize_stamina_box(self, new_box):
        if new_box is None:
            return self.last_stamina_box

        if self.last_stamina_box is None:
            self.last_stamina_box = new_box
            return new_box

        x1 = int((self.last_stamina_box[0] + new_box[0]) / 2)
        y1 = int((self.last_stamina_box[1] + new_box[1]) / 2)
        x2 = int((self.last_stamina_box[2] + new_box[2]) / 2)
        y2 = int((self.last_stamina_box[3] + new_box[3]) / 2)

        stabilized = (x1, y1, x2, y2)
        self.last_stamina_box = stabilized

        return stabilized