/* interrupt routine for Rotary Encoders

   from RAF at http://playground.arduino.cc/Main/RotaryEncoders
   the interrupt-pin mapping is here: https://www.arduino.cc/en/Reference/AttachInterrupt
   extended to a second encoder by PB (what an ugly hack it is)

    The rotary encoder has three pins, seen from front: A C B
    Clockwise rotation A(on)->B(on)->A(off)->B(off)
    CounterCW rotation B(on)->A(on)->B(off)->A(off)

   in The Mirror, these are:
      encoder 1: A(blue) B(purple)  switch(grey) pins 19,18,17
      encoder 2: A(yellow) B(green) switch(orange) pins 2,3,4
      
   current status (9 Aug 2015 15:31 PDT): 
    - encoder1 works fine, reports it's relative position accurately.
    - encoder2 will turn one dedent in each direction, then hangs. 

*/

// usually the rotary encoders three pins have the ground pin in the middle
enum PinAssignments {
   encoder1pinA = 2,   // right
   encoder1pinB = 3,   // left
   clear1button = 4,    // switch
   encoder2pinA = 19,  // right
   encoder2pinB = 18,   // left
   clear2button = 17    // switch
};

const int DEBOUNCE = 10;

enum Event {
  dec,
  inc,
  up,
  down,
};

class Knob {
  int id;
  int aInt;
  int bInt;
  int aPin;
  int bPin;
  int buttonPin;
  int a;
  int b;
  bool button;

public:
  Knob(int id, int aPin, int bPin, int buttonPin)
  : id(id), aPin(aPin), bPin(bPin), buttonPin(buttonPin) {
  }

  void printState(Event event) {
      Serial.print("{\"id\":");
      Serial.print(id, DEC);
      Serial.print(", \"event\":");
      switch (event) {
        case inc: Serial.print("\"inc\""); break;
        case dec: Serial.print("\"dec\""); break;
        case up: Serial.print("\"up\""); break;
        case down: Serial.print("\"down\""); break;
      }
      Serial.print(", \"button\":");
      if (digitalRead(buttonPin) == LOW) {
        Serial.print("true");
      } else {
        Serial.print("false");
      }
      Serial.println("}");
  }

  void setup() {
   pinMode(aPin, INPUT);
   pinMode(bPin, INPUT);
   pinMode(buttonPin, INPUT);
   digitalWrite(aPin, HIGH);
   digitalWrite(bPin, HIGH);
   digitalWrite(buttonPin, HIGH);
  }

  void loop() {
    bool val = digitalRead(buttonPin) == LOW;
    if (val != button) {
      button = val;
      printState((val == true) ? down : up);
    }
  }

  void doA() {
    delay(DEBOUNCE);
    int val = digitalRead(aPin);
    if (val == HIGH && a == LOW) {
      int b = digitalRead(bPin);
      if (b == LOW) {
        printState(inc);
      } else {
        printState(dec);
      }
    }
    a = val;
  }

  void doB() {
  }
};

Knob k1(1, encoder1pinA, encoder1pinB, clear1button);
Knob k2(2, encoder2pinA, encoder2pinB, clear2button);

void setup() {
  k1.setup();
  k2.setup();

// encoder pin on interrupt 0 (pin 2)
   attachInterrupt(0, doEncoderA1, CHANGE);
// encoder pin on interrupt 1 (pin 3)
   attachInterrupt(1, doEncoderB1, CHANGE);

// encoder pin on interrupt 4 (pin 19)
   attachInterrupt(4, doEncoderB2, CHANGE);
// encoder pin on interrupt 5 (pin 18)
   attachInterrupt(5, doEncoderA2, CHANGE);

   Serial.begin(9600);  // output
   Serial.println("Knobs initialized");
}

void loop() {
  k1.loop();
  k2.loop();
}

void doEncoderA1() {
  k1.doA();
}

void doEncoderB1() {
  k1.doB();
}

void doEncoderA2() {
  k2.doA();
}

void doEncoderB2() {
  k2.doB();
}


