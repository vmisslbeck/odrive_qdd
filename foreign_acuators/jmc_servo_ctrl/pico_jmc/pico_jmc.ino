/*
This Program is used to control a JMC Servo Motor with a Raspberry Pi Pico. 

@author: Valentin Misslbeck
@date: 4/2/2024
MM/DD/YYYY
*/


// Pin Definitions

// output pins
const int dir_pin = 2; // Direction Pin
const int pulse_pin = 3; // Pulse Pin
const int ledPin = LED_BUILTIN; // if that does not work use "25" , only optional

// input pins
const int button1_pin = 22;
const int button2_pin = 22; 
const int voltage_pin = 28; // This has to be one of the analog pins, which are the ADC pins, on the Pico: GP26, GP27, GP28

// speed control variables
const int multiplier_interval = 4; // Multiplier is necessary for micros() and has to be 4, for millis() it can be 1
int sensor_value;
float speed;
long interval; // Interval in Microseconds // new consideration: const float interval/4

unsigned long previousMicros = 0; // Time at which the last pulse was sent

// state machine variables
int button1_state = HIGH;
int last_button1_state = LOW;
int dir_state = LOW;
int pulse_state = LOW;
int ledState = LOW;

bool button1_pressed = false;


void setup() {

  pinMode(dir_pin, OUTPUT);
  pinMode(pulse_pin, OUTPUT);
  pinMode(ledPin, OUTPUT);

  pinMode(button1_pin, INPUT);
  pinMode(button2_pin, INPUT); // still unused
  pinMode(voltage_pin, INPUT); // rather unnecessary, but for the sake of completeness

  Serial.begin(9600);
}

void loop() {
  // read potentiometer value to control the speed in percent. 4 = 100 %  and 1023 = 0%
  // that means, that a low value of the potentiometer means a low interval and thus a high speed
  sensor_value = analogRead(voltage_pin);
  //Serial.println(sensor_value);
  speed = (1023/sensor_value); // (1023 / 1023) = 1 , (1023 / 4 ) = 255
  if speed < 10 {
    // then the motor stops
    interval = 0;
  }
  else {
    interval = (speed * multiplier_interval);
  };
  
  // 4 * 0.9961 = 3.9844 , 4 * 0 = 0
  //Serial.println(interval);

  // producing a pulse signal for rotation of the motor:
  unsigned long currentMicros = micros();

  if (currentMicros - previousMicros >= interval) {

    previousMicros = currentMicros;

    // If the pin is HIGH, set it to LOW and vice versa
    if (pulse_state == HIGH) {
      ledState = LOW;
      pulse_state = LOW;
    } else {
      ledState = HIGH;
      pulse_state = HIGH;
    }
    digitalWrite(pulse_pin, pulse_state);
    digitalWrite(ledPin, ledState);
  }

  // Implementation of a state machine for the direction of the motor 
  // (Same could be done for enalbing/disabling the motor)
  button1_state = digitalRead(button1_pin);

  if (button1_state == HIGH && last_button1_state == LOW) {
    // buttton was pressed, but not in the previous loop
    button1_pressed = !button1_pressed;
    Serial.println("direction changed");
  }

  last_button1_state = button1_state; // update last button state

  if (button1_pressed) {
    dir_state = HIGH; // Set direction to HIGH if the button was pressed
  } else {
    dir_state = LOW; // Otherwise the direction stays LOW
  }

  digitalWrite(dir_pin, dir_state);
}