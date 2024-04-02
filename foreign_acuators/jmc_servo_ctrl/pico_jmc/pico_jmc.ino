/*
This Program is used to control a JMC Servo Motor with a Raspberry Pi Pico. 

@author: Valentin Misslbeck
@date: 4/2/2024
*/


// Pin Definitions

//-->const int ena_pin = 11;
const int dir_pin = 2; // Direction Pin
const int pulse_pin = 3; // Pulse Pin
const int ledPin = LED_BUILTIN; // if that does not work use "25" , only optional

// input pins
const int button1_pin = 22;
const int button2_pin = 22; 
const int voltage_pin = 28; // This has to be one of the analog pins, which are the ADC pins, on the Pico: GP26, GP27, GP28

const int multiplier_interval = 4; // Multiplier ist bei micros() notwendig und muss 4 sein, bei millis() kann es 1 sein
int sensor_value;
float speed;
long interval; //= multiplier_interval * speed; // Intervall in Microsekunden // neue Überlegung const float Intervall/4

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
  pinMode(button2_pin, INPUT); // still unused
  Serial.begin(9600);
}

void loop() {
  // Lese Potentiometerwert ein um Prozentual die Geschwindigkeit zu steuern. 4 = 0% und 1023 = 100% der Geschwindigkeit
  sensor_value = analogRead(voltage_pin);
  Serial.println(sensor_value);
  speed = sensor_value / 10.23; // Geschwindigkeit in Prozent
  interval = multiplier_interval * speed; // Intervall in Microsekunden

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
    Serial.println("direction changed");
  }

  last_button1_state = button1_state; // Aktualisiere den letzten Zustand des Knopfs

  if (button_pressed) {
    dir_state = HIGH; // Setze Richtung auf HIGH, wenn der Knopf gedrückt wurde
  } else {
    dir_state = LOW; // Andernfalls bleibt die Richtung auf LOW
  }

  digitalWrite(dir_pin, dir_state);
}
  
  
  