//CarTransmitter.ino
// Runs on LoRa board on car

#include <SPI.h>
#include <RH_RF95.h>

// for feather m0  
#define RFM95_CS 8
#define RFM95_RST 4
#define RFM95_INT 3

#define RF95_FREQ 915.0

const int SIZE = 13;
const char TERM = 255;

RH_RF95 rf95(RFM95_CS, RFM95_INT);

void setup() {
  //Serial.begin(9600);           // start serial for output
  Serial1.begin(9600);

  pinMode(RFM95_RST, OUTPUT);
  digitalWrite(RFM95_RST, HIGH);

  // manual reset
  digitalWrite(RFM95_RST, LOW);
  delay(10);
  digitalWrite(RFM95_RST, HIGH);
  delay(10);

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

uint8_t transmit_data[SIZE];
void loop() {
  /*
  while(Serial1.available() <= SIZE){}
  byte serial_buf[SIZE+1];
  byte chars_read = Serial1.readBytesUntil(TERM, serial_buf, SIZE+1);
  */
  byte chars_read = 13;
  byte serial_buf[13];

  for(int i=0; i<13; ++i){
    serial_buf[i] = random(100);
  }
  delay(1000);
  if(chars_read == SIZE){
    // Successful read. Copy temporary buffer into data array
    //Serial.print("\nReceived:");
    for(int i=0; i<SIZE; ++i){
      transmit_data[i] = serial_buf[i];
      //Serial.print(transmit_data[i], DEC);
      //Serial.print(" ");
    }

    // Send the packet over radio
    rf95.send(transmit_data, SIZE);
    //delay(10);
    rf95.waitPacketSent();
  }
}

