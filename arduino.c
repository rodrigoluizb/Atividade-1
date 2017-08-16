const int ledPin1 = 2, ledPin2 = 3, ledPin3 = 4;
const int ledPin = LED_BUILTIN;
float tempF = 30.0;
int numBytes = 0, tempI = 0, setPointI;
char oper;
String setPointS = "", tempS = "";
float setPointF = 0.0;

void setup() {
  Serial.begin(9600);
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, LOW);
}

void loop() {
  // put your main code here, to run repeatedly:
  while(!Serial.available());
  digitalWrite(ledPin1, LOW);
  numBytes = Serial.available();
  oper = Serial.read();
  if (oper == 'r'){
    Serial.print(tempF);
    Serial.print('\n');
    tempF += 0.1;
  }
  else if(oper == 'w'){
    setPointS = Serial.readStringUntil('\n');
    setPointF = setPointS.toFloat();
  }
  if (tempF > setPointF){
    digitalWrite(ledPin3, HIGH);
  }
  else{
    digitalWrite(ledPin, LOW);
  }
}