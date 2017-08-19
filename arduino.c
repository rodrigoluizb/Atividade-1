#define THERMISTORPIN A0    // Analog pin which thermistor is connected to
#define ONVOLT 6            // Pin used to turn the thermistor on
#define VINIT 2.08          // Voltage @ 0oC
#define V35 0.5             // Voltage @ 35oC
#define ACT 9               // Pin connected to optocoupler
#define NUMSAMPLES 5        // Number of samples, for a oversampling.
#define ledPin 2

uint16_t samples[NUMSAMPLES];

char oper;                  // Char that will receive either w (receive setpoint from python) or r (to read the temperature from thermistor)
String setPointS = "";      // Auxiliar string
float setPointF = 30.0;      // Setpoint value
float average = 0.0;

void setup() {
  Serial.begin(9600);       // Initialize serial port with baud rate = 9600
  pinMode(ledPin, OUTPUT);  // Alarm led pin as output
  pinMode(THERMISTORPIN,INPUT);  //Thermistor analog pin as input
  pinMode(ONVOLT,OUTPUT);       // Pin that turn the thermistor on as output
  pinMode(ACT,OUTPUT);          // Pin that control the actuator as output

  digitalWrite(ONVOLT,LOW);     // Initialize the thermistor as OFF
  digitalWrite(ACT,LOW);        // Initialize the actuator as OFF
  digitalWrite(ledPin, LOW);    // Initialize the led as OFF
}

void loop() {
  while(!Serial.available());   //Read operation character
  oper = Serial.read();
  if (oper == 'r'){
    uint8_t i;
    average = 0.0;
    // take N samples in a row, with a slight delay
    for (i=0; i< NUMSAMPLES; i++) {
      digitalWrite(ONVOLT,HIGH);
      samples[i] = analogRead(THERMISTORPIN);
      average += samples[i];
      delay(10);
      }
    digitalWrite(ONVOLT,LOW);
    average /= NUMSAMPLES; //value in number
    average = 5*average/1023; //value in voltage
    // convert the value to temperature
    average = (VINIT - average)*35/(VINIT - V35);
    // Send value to python
    Serial.print(average);
    Serial.print('\n');
  }
  else if(oper == 'w'){
    setPointS = Serial.readStringUntil('\n');
    setPointF = setPointS.toFloat();
  }
  if (average > setPointF){
    digitalWrite(ledPin, HIGH);
  }
  else{
    digitalWrite(ledPin, LOW);
  }
  if (average > (setPointF + 1.0))
    digitalWrite(ACT,HIGH);
  else if(average < (setPointF - 1.0))
    digitalWrite(ACT,LOW);
}