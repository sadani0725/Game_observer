#Base imports---------------------------------------------
import time
import cv2
import keyboard
import time
from capture.screen_capture import capture_frame
from logger.logger_util import log_event
from models.LLM.LLMClient import LLMClient

#System startup-------------------------------------------
print("Starting system...")

#Detection mode-------------------------------------------
DETECTION_MODE = "AI"   # "STATIC" vagy "AI"

#Dependent imports----------------------------------------
if DETECTION_MODE == "STATIC":
    from static_detection.hp_detector_static import detect_hp_ratio
    from static_detection.you_died_detector_static import detect_you_died
else:
    from ai_detection.ui_detector import detect_ui
    from ai_detection.ui_tracker import UIStateTracker

    tracker = UIStateTracker()
    llm = LLMClient()

#Check if LLM is up---------------------------------------
if llm.is_available():
    print("LLM connected ✔")
else:
    print("LLM not running → starting fallback mode (no AI)")

#Set startup parameters-----------------------------------
running = False

#Base functions-------------------------------------------
def start_recording():
    global running 
    global prev_hp
    global prev_stamina

    if not running:
        log_event("🟢 Game observer started.")

        prev_hp = 1.0
        prev_stamina = 1.0
        running = True
    else:
        print("⚠️ Already running.")

def stop_recording():
    global running 

    if running:
        log_event("🛑 Game observer stopped.")

        running = False

        if llm.is_available():

            log_text = process_log_file()
            result = llm.analyze(log_text)
            log_event("🤖 AI ANALYSIS:\n" + result)
    else:
        print("⚠️ Already stopped.")

def process_log_file():
    with open("game_log.txt", "r", encoding="utf-8") as f:
        log_text = f.read()
        return log_text

#Main----------------------------------------------------
def main():
    global running 
    global prev_hp
    global prev_stamina
    
    prev_hp = 1.0
    prev_stamina = 1.0
    dead = False
    died = False   

    keyboard.add_hotkey("+", start_recording)
    keyboard.add_hotkey("-", stop_recording)

    while True:

        if running:

            frame = capture_frame()

            if DETECTION_MODE == "STATIC":
                hp = detect_hp_ratio(frame)
                died = detect_you_died(frame)

            else:
                ui_data = detect_ui(frame, tracker)
                hp = ui_data.hp_percent
                stamina = ui_data.stamina_precent
                died = ui_data.player_dead

            if hp is not None:

                # Újraéledés után reset
                if hp > 0.4 and dead:
                    log_event("💫 Revived.")
                    dead = False
                    hp = 1
                    prev_hp = 1
                    stamina = 1
                    prev_stamina = 1

                # HP detektálás
                if hp < prev_hp - 0.05:  # ha 5%-nál többet csökkent
                    log_event(f"⚠️ HP decreased: {prev_hp:.2f} → {hp:.2f}")
                    prev_hp = hp
                
                if hp > prev_hp + 0.10:  # ha 10%-nál többet nőtt
                    log_event(f"💚 HP increased: {prev_hp:.2f} → {hp:.2f}")
                    prev_hp = hp

            if stamina is not None:

                # Stamina detektálás
                if stamina < prev_stamina - 0.05:  # ha 5%-nál többet csökkent
                    log_event(f"🔻 Stamina decreased: {prev_stamina:.2f} → {stamina:.2f}")
                    prev_stamina = stamina
                
                if stamina > prev_stamina + 0.05:  # ha 5%-nál többet nőtt
                    log_event(f"🔺 Stamina increased: {prev_stamina:.2f} → {stamina:.2f}")
                    prev_stamina = stamina

            # "You Died" detektálás
            if died and not dead:
                log_event("💀 YOU DIED detected.")
                dead = True

            # megjelenítés (debug)
            cv2.imshow("Game Observer", frame)

            time.sleep(0.3)  

        else: 
            cv2.destroyAllWindows()

if __name__ == "__main__":
    main()