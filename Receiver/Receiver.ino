#include <IRLib.h>

#define PROTOCOL NEC
#define BTN_UP 0x1FE58A7
#define BTN_LEFT 0x1FE807F
#define BTN_RIGHT 0x1FEC03F
#define BTN_DOWN 0x1FEA05F
#define BTN_VOL_DOWN 0x1FEE01F
#define BTN_VOL_UP 0x1FE906F
#define BTN_POWER 0x1FE7887
#define BTN_SETUP 0x1FE48B7

const int SIGNAL_PIN = 8;
const int GND_PIN = 9;
const int POWER_PIN = 10;

IRrecv receiver(SIGNAL_PIN);
IRdecode decoder;

void setup() {
    Serial.begin(9600);
    receiver.enableIRIn();
    pinMode(GND_PIN, OUTPUT);
    pinMode(POWER_PIN, OUTPUT);
    digitalWrite(GND_PIN, LOW);
    digitalWrite(POWER_PIN, HIGH);
}

int rpm = 0;
int temp = 0;
int speed = 0;

void loop() {
  String result = "";
  if (receiver.GetResults(&decoder)) {
    decoder.decode();       //Decode the data
    if(decoder.decode_type == NEC){
        switch(decoder.value){
            case BTN_UP:
              speed += 10;
              result.concat("Speed:");
              result.concat(speed);
              break;
            case BTN_DOWN:
              speed -= 10;
              result.concat("Speed:");
              result.concat(speed);
              break;
            case BTN_LEFT:
              rpm -= 100;
              result.concat("RPM:");
              result.concat(rpm);
              break;
            case BTN_RIGHT:
              rpm += 100;
              result.concat("RPM:");
              result.concat(rpm);
              break;
            case BTN_VOL_UP:
              temp += 10;
              result.concat("Temp:");
              result.concat(temp);
              break;
            case BTN_VOL_DOWN:
              temp -= 10;
              result.concat("Temp:");
              result.concat(temp);
              break;
            case BTN_POWER:
              result.concat("-- Power");
              break;
            case BTN_SETUP:
              result.concat("-- Clear");
              break;
            default:
              result.concat(decoder.value);
              //decoder.DumpResults();
        }
    } else {
        //decoder.DumpResults();  //Show the results on serial monitor
    }
    receiver.resume();      //Restart the receiver
  }
  if(result != ""){
    Serial.print(result);
    Serial.print("\n");
  }
  delay(50);
}
