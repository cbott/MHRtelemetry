#include "TinyGPS.h"
#include <SPI.h>
#include <RH_RF95.h>

// for feather m0  
#define RFM95_CS 8
#define RFM95_RST 4
#define RFM95_INT 3

#define RF95_FREQ 915.0

const int SIZE = 4;
const char TERM = 255;

RH_RF95 rf95(RFM95_CS, RFM95_INT);
TinyGPS gps;

void setup() {
  Serial.begin(9600);
  Serial1.begin(9600);
  Serial.println("Beginning");
  
  pinMode(RFM95_RST, OUTPUT);
  digitalWrite(RFM95_RST, HIGH);

  // manual reset
  digitalWrite(RFM95_RST, LOW);
  delay(10);
  digitalWrite(RFM95_RST, HIGH);
  delay(10);
  
  pinMode(13, OUTPUT);

  while (!rf95.init()) {
    Serial.println("LoRa radio init failed");
    while (1);
  }
  Serial.println("LoRa radio init OK!");

  // Defaults after init are 434.0MHz, modulation GFSK_Rb250Fd250, +13dbM
  if (!rf95.setFrequency(RF95_FREQ)) {
    Serial.println("setFrequency failed");
    while (1);
  }

  rf95.setTxPower(23, false);
}

byte x[SIZE];
bool ledstate = 1;
void loop() {
  char packet;
  bool newData = false;

  // Read in all available serial data from the GPS
  while(Serial1.available()){
    packet = Serial1.read();
    if(gps.encode(packet)) newData = true;
  }
  // If we got new info, print it out
  if(newData){
    ledstate = 0;
    int year;
    byte month, day, hour, minute, second, hundredths;
    unsigned long fix_age;
    gps.crack_datetime(&year, &month, &day, &hour, &minute, &second, &hundredths, &fix_age);

    float flat, flon;
    unsigned long age;

    float gps_speed = gps.f_speed_mph();
    gps.f_get_position(&flat, &flon, &age);
    Serial.print("LAT=");
    Serial.print(flat == TinyGPS::GPS_INVALID_F_ANGLE ? 0.0 : flat, 6);
    Serial.print(" LON=");
    Serial.print(flon == TinyGPS::GPS_INVALID_F_ANGLE ? 0.0 : flon, 6);
    Serial.print(" SAT=");
    Serial.print(gps.satellites() == TinyGPS::GPS_INVALID_SATELLITES ? 0 : gps.satellites());
    Serial.print(" PREC=");
    Serial.print(gps.hdop() == TinyGPS::GPS_INVALID_HDOP ? 0 : gps.hdop());
    Serial.print(" ");
    Serial.print(hour);
    Serial.print(":");
    Serial.print(minute);
    Serial.print(":");
    Serial.print(second);
    Serial.print("\n");
    Serial.print(gps_speed);
    Serial.println(" MPH\n");

    x[0] = gps_speed*2;
    x[1] = hour;
    x[2] = minute;
    x[3] = second;
    // Send the packet over radio
    rf95.send((uint8_t *)x, SIZE);
    //delay(10);
    rf95.waitPacketSent();
  }
  digitalWrite(13, ledstate);
}
