//CarTransmitter.ino
const int SIZE = 10;
const char TERM = 255;

void setup() {
  Serial.begin(9600);           // start serial for output
  Serial1.begin(9600);
}

byte x[SIZE];
void loop() {
  while(Serial1.available() <= SIZE){ delay(1); }
  byte buf[SIZE];
  byte chars_read = Serial1.readBytesUntil(TERM, buf, SIZE);

  if(chars_read == SIZE){
    // Successful read. Copy temporary buffer in to data array
    Serial.print("\nReceived:");
    for(int i=0; i<SIZE; ++i){
      x[i] = buf[i];
      Serial.print(x[i], DEC);
      Serial.print(" ");
    }
  }
}


