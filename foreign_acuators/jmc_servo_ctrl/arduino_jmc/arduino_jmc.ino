//pin-Belegung
  //-->const int ena_pin = 11;
const int dir_pin = 10; // Direction Pin
const int pulse_pin = 9; //eingebauter Digital Pin
const int button1_pin = 7; // Input Pin für Button1
const int button2_pin = 8; // Input Pin für Button2 
const int ledPin = LED_BUILTIN; // nur optional

const int multiplier_interval = 4; // Multiplier ist bei micros() notwendig und muss 4 sein, bei millis() kann es 1 sein
const long interval = multiplier_interval * 10000; // Intervall in Microsekunden // neue Überlegung const float Intervall/4

unsigned long previousMicros = 0; // Speicher für den letzten Wechsel

int button1_state = HIGH;
int last_button1_state = LOW; // Zustand des vorherigen Schleifendurchlaufs
int dir_state = LOW;
  //-->int ena_state = HIGH;
int pulse_state = LOW;
int ledState = LOW; // nur optional

bool button_pressed = false; // Variable zur Verfolgung, ob der Knopf gedrückt wurde


void setup() {

  pinMode(dir_pin, OUTPUT);
  pinMode(pulse_pin, OUTPUT);
  pinMode(ledPin, OUTPUT); // nur optional

  // initialisiere die Knöpfe-Pins als Input:
  pinMode(button1_pin, INPUT);
  pinMode(button2_pin, INPUT);
}

void loop() {
  // Erzeugung eines Pulssignal für Drehung des Motors:
  unsigned long currentMicros = micros();
  
  if (currentMicros - previousMicros >= interval) {
    // Wenn das Intervall vergangen ist
    previousMicros = currentMicros;

    // Wenn der Pin HIGH ist, setze ihn auf LOW und umgekehrt
    if (pulse_state == HIGH) {
      ledState = LOW; // nur optional
      pulse_state = LOW;
    } else {
      ledState = HIGH; // nur optional
      pulse_state = HIGH;
    }
    digitalWrite(pulse_pin, pulse_state);
    digitalWrite(ledPin, ledState); // nur optional
  }

  //
  button1_state = digitalRead(button1_pin);

  if (button1_state == HIGH && last_button1_state == LOW) {
    // Knopf wurde gedrückt, aber nicht im vorherigen Schleifendurchlauf
    button_pressed = !button_pressed; // Invertiere den Status der Knopfdrückung
  }

  last_button1_state = button1_state; // Aktualisiere den letzten Zustand des Knopfs

  if (button_pressed) {
    dir_state = HIGH; // Setze Richtung auf HIGH, wenn der Knopf gedrückt wurde
  } else {
    dir_state = LOW; // Andernfalls bleibt die Richtung auf LOW
  }

  digitalWrite(dir_pin, dir_state);
}
  
  
  