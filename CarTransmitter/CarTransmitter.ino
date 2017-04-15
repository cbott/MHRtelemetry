//CarTransmitter.ino
// Runs on LoRa board on car

#include <SPI.h>
#include <RH_RF95.h>

// for feather m0  
#define RFM95_CS 8
#define RFM95_RST 4
#define RFM95_INT 3

#define RF95_FREQ 915.0

const int SIZE = 16;
const char TERM = 255;

RH_RF95 rf95(RFM95_CS, RFM95_INT);

void setup() {
  //Serial.begin(9600);           // start serial for output
  Serial1.begin(115200);

  pinMode(RFM95_RST, OUTPUT);
  digitalWrite(RFM95_RST, HIGH);

  // manual reset
  digitalWrite(RFM95_RST, LOW);
  delay(10);
  digitalWrite(RFM95_RST, HIGH);
  delay(10);
  
  pinMode(13, OUTPUT);

  while (!rf95.init()) {
    //Serial.println("LoRa radio init failed");
    while (1);
  }
  //Serial.println("LoRa radio init OK!");

  // Defaults after init are 434.0MHz, modulation GFSK_Rb250Fd250, +13dbM
  if (!rf95.setFrequency(RF95_FREQ)) {
    //Serial.println("setFrequency failed");
    while (1);
  }

  rf95.setTxPower(23, false);
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
    digitalWrite(13, x[0] % 2 == 0);

    // Send the packet over radio
    rf95.send((uint8_t *)x, SIZE);
    //delay(10);
    rf95.waitPacketSent();
  }
}

