//CarTransmitter.ino
const int SIZE = 10;
const char TERM = 255;

void setup() {
  Serial.begin(9600);           // start serial for output
  Serial1.begin(9600);
  pinMode(13, OUTPUT);
}

byte x[SIZE];
void loop() {
  while(Serial1.available() <= SIZE){}
  byte buf[SIZE+1];
  byte chars_read = Serial1.readBytesUntil(TERM, buf, SIZE+1);

  if(chars_read == SIZE){
    // Successful read. Copy temporary buffer in to data array
    //Serial.print("\nReceived:");
    for(int i=0; i<SIZE; ++i){
      x[i] = buf[i];
      //Serial.print(x[i], DEC);
      //Serial.print(" ");
    }
    digitalWrite(13, x[1] % 2 == 0);
  }
}

