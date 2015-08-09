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

volatile unsigned int encoder1pos = 0;  // a counter for the dial
volatile unsigned int encoder2pos = 0;  // a counter for the dial
unsigned int lastReported1pos = 1;      // change management
unsigned int lastReported2pos = 1;      // change management
static boolean rotating1 = false;       // debounce management
static boolean rotating2 = false;       // debounce management

// interrupt service routine vars
boolean A1_set = false;
boolean B1_set = false;
boolean A2_set = false;
boolean B2_set = false;


void setup() {

   pinMode(encoder1pinA, INPUT);
   pinMode(encoder1pinB, INPUT);
   pinMode(clear1button, INPUT);

   pinMode(encoder2pinA, INPUT);
   pinMode(encoder2pinB, INPUT);
   pinMode(clear2button, INPUT);

 // turn on pullup resistors
   digitalWrite(encoder1pinA, HIGH);
   digitalWrite(encoder1pinB, HIGH);
   digitalWrite(clear1button, HIGH);
   digitalWrite(encoder2pinA, HIGH);
   digitalWrite(encoder2pinB, HIGH);
   digitalWrite(clear2button, HIGH);

/*
// encoder pin on interrupt 0 (pin 2)
   attachInterrupt(0, doEncoderA1, CHANGE);
// encoder pin on interrupt 1 (pin 3)
   attachInterrupt(1, doEncoderB1, CHANGE);
*/

/*
// encoder pin on interrupt 2 (pin 21)
   attachInterrupt(2, doEncoderB2, CHANGE);
// encoder pin on interrupt 3 (pin 20)
   attachInterrupt(3, doEncoderA2, CHANGE);
*/ 

// encoder pin on interrupt 4 (pin 19)
   attachInterrupt(4, doEncoderB2, CHANGE);
// encoder pin on interrupt 5 (pin 18)
   attachInterrupt(5, doEncoderA2, CHANGE);

   Serial.begin(9600);  // output
   Serial.println("hello.");
}

// main loop, work is done by interrupt service routines, this one only prints stuff
void loop() {
   rotating1 = true;  // reset the debouncer
   rotating2 = true;  // reset the debouncer

   if (lastReported1pos != encoder1pos) {
      Serial.print("Index 1:");
      Serial.println(encoder1pos, DEC);
      lastReported1pos = encoder1pos;
   }
   if (lastReported2pos != encoder2pos) {
      Serial.print("Index 2:");
      Serial.println(encoder2pos, DEC);
      lastReported2pos = encoder2pos;
   }
   if (digitalRead(clear1button) == LOW )  {
      encoder1pos = 0;
   }
   if (digitalRead(clear2button) == LOW )  {
      encoder2pos = 0;
   }
}

// Interrupt on A changing state
void doEncoderA1(){
   if ( rotating1 ) delay (1);  // wait a little until the bouncing is done
   // Test transition, did things really change?
   if( digitalRead(encoder1pinA) != A1_set ) {  // debounce once more
      A1_set = !A1_set;
      if ( A1_set && !B1_set )      // adjust counter + if A leads B
         encoder1pos += 1;
      rotating1 = false;  // no more debouncing until loop() hits again
   }
}
// Interrupt on A changing state
void doEncoderA2(){
   if ( rotating2 ) delay (1);  // wait a little until the bouncing is done
   // Test transition, did things really change?
   if( digitalRead(encoder2pinA) != A2_set ) {  // debounce once more
      A2_set = !A2_set;
      if ( A2_set && !B2_set )      // adjust counter + if A leads B
         encoder2pos += 1;
      rotating2 = false;  // no more debouncing until loop() hits again
   }
}


// Interrupt on B changing state, same as A above
void doEncoderB1(){
   if ( rotating1 ) delay (1);
   if( digitalRead(encoder1pinB) != B1_set ) {
      B1_set = !B1_set;
      //  adjust counter - 1 if B leads A
      if( B1_set && !A1_set )
         encoder1pos -= 1;

      rotating1 = false;
   }
}
// Interrupt on B changing state, same as A above
void doEncoderB2(){
   if ( rotating2 ) delay (1);
   if( digitalRead(encoder2pinB) != B2_set ) {
      B2_set = !B2_set;
      //  adjust counter - 1 if B leads A
      if( B2_set && !A2_set )
         encoder2pos -= 1;
      rotating2 = false;
   }
}



