// Receiver.ino
// Runs on LoRa board connected to monitoring computer

#include <SPI.h>
#include <RH_RF95.h>

// for feather m0  
#define RFM95_CS 8
#define RFM95_RST 4
#define RFM95_INT 3

#define RF95_FREQ 915.0

RH_RF95 rf95(RFM95_CS, RFM95_INT);

void setup() 
{
  pinMode(13, OUTPUT);     
  pinMode(RFM95_RST, OUTPUT);
  digitalWrite(RFM95_RST, HIGH);

  Serial.begin(9600);

  Serial.println("Telemetry Receiver:");
  
  digitalWrite(RFM95_RST, LOW);
  delay(10);
  digitalWrite(RFM95_RST, HIGH);
  delay(10);

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
  Serial.print("Set Freq to: "); Serial.println(RF95_FREQ);

  // The default transmitter power is 13dBm, using PA_BOOST.
  // If you are using RFM95/96/97/98 modules which uses the PA_BOOST transmitter pin, then 
  // you can set transmitter powers from 5 to 23 dBm:
  rf95.setTxPower(23, false);
}

bool ledstate = 1;
void loop()
{
  if (rf95.available())
  {
    // Should be a message for us now   
    uint8_t buf[RH_RF95_MAX_MESSAGE_LEN];
    uint8_t len = sizeof(buf);
    
    if (rf95.recv(buf, &len))
    {
      //RH_RF95::printBuffer("Received: ", buf, len);
      digitalWrite(13, ledstate);
      ledstate = !ledstate;
      for(int i=0; i<len; ++i){
        Serial.print(buf[i]);
        Serial.print(" ");
      }
      Serial.print("\n");
    }
    else
    {
      Serial.println("Receive failed");
    }
  }
}



//////////////////////////////////////////////////////////////////////
//----------------------- Demonstration Loop -----------------------//
//////////////////////////////////////////////////////////////////////
// Send realistic data to demonstrate telemetry capabilities
//byte engine_t = 150;
//byte l_bat_t = 0;
//byte r_bat_t = 0;
//float l_bat_soc = 100;
//float r_bat_soc = 100;
//byte rpm = 20;
//byte l_motor_t = 80;
//byte r_motor_t = 80;
//byte l_mc_t = 50;
//byte r_mc_t = 50;
//byte accel =  0;
//byte accel_err = 0;
//byte brake = 25;
//byte brake_err = 0;
//float lv_soc = 127;
//
//void loop() {
//  uint8_t serial_buf[] = {engine_t, l_bat_t, r_bat_t, l_bat_soc, r_bat_soc,
//                          rpm, l_motor_t, r_motor_t, l_mc_t, r_mc_t,
//                          accel, accel_err, brake, brake_err, lv_soc};
//
//  // Send data over serial
//  for(int i=0; i<15; ++i){
//    Serial.print(serial_buf[i]);
//    Serial.print(" ");
//  }
//  Serial.print("\n");
//
//  delay(500);
//
//  // Update the values realistically
//  engine_t += random(-1,2);
//  l_bat_soc -= 0.1;
//  r_bat_soc -= 0.1;
//  rpm += random(-4,5);
//  l_motor_t += random(-2,3);
//  r_motor_t += random(-2,3);
//  l_mc_t += random(-2,3);
//  r_mc_t += random(-2,3);
//  lv_soc -= 0.2;
//}

