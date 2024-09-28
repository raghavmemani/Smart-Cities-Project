
const int LED_PIN = 9;
// #include <SoftwareSerial.h>

// SoftwareSerial portOne(3, 4);
int d=0;

void setup() {
  // put your setup code here, to run once:
  pinMode(LED_PIN, OUTPUT);
  Serial.begin(9600);
  

}

void loop() {
  // put your main code here, to run repeatedly:
  // if(Serial.available() > 0) {
    int d = Serial.read();

    if(d == 'p') {
      digitalWrite(LED_PIN, HIGH);
      delay(5000);
    } 
    else {
      digitalWrite(LED_PIN, LOW);
      // delay(2000);
    }
  // }
  // digitalWrite(LED_PIN, HIGH);
  // digitalWrite(LED_PIN, LOW);
  // delay(2000);
}
