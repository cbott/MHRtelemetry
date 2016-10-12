#include <LiquidCrystal.h>
#include <IRLib.h>

#define PROTOCOL NEC
#define BTN_UP 0x1FE58A7
#define BTN_LEFT 0x1FE807F
#define BTN_RIGHT 0x1FEC03F
#define BTN_DOWN 0x1FEA05F

#define SYMBOL_CHECKER byte(0)
#define SYMBOL_BAD byte(1)
#define SYMBOL_GOOD byte(2)
#define SYMBOL_DOTS byte(3)

const int SIGNAL_PIN = 6;

IRrecv receiver(SIGNAL_PIN);
IRdecode decoder;
LiquidCrystal lcd(7, 8, 9, 10, 11, 12);

byte bad[8] = {
 0b0,0b11011,0b1110,0b100,0b1110,0b11011,0b0,0b0
};
byte good[8] = {
    0b00000,0b00000,0b00001,0b00010,0b10100,0b01000,0b00000,0b00000
};

void setup() {
    Serial.begin(9600);
    receiver.enableIRIn();

    // set up the LCD's number of columns and rows:
    lcd.begin(20, 4);
  
    lcd.createChar(1, bad);
    lcd.createChar(2, good);
}

int val = 10;
void loop() {
    String result = "None";
  if (receiver.GetResults(&decoder)) {
    decoder.decode();       //Decode the data
    if(decoder.decode_type == NEC){
        switch(decoder.value){
            case BTN_UP:
              result = "Up";
              val += 10;
              break;
            case BTN_DOWN:
              result = "Down";
              val -= 10;
              break;
            case BTN_LEFT:
              result = "Left";
              val -= 1;
              break;
            case BTN_RIGHT:
              result = "Right";
              val += 1;
              break;
            default:
              result = "Error";
              //decoder.DumpResults();
        }
    } else {
        //decoder.DumpResults();  //Show the results on serial monitor
    }
    receiver.resume();      //Restart the receiver
  }
  
  if(result != "None"){
    lcd.clear();
    if(result == "Error"){
        lcd.write(SYMBOL_BAD);
    } else {
        lcd.write(SYMBOL_GOOD);
    }
    lcd.print(result);
    lcd.setCursor(0,1);
    lcd.print(val);
    lcd.display();
  }
  Serial.print(val);
  Serial.print("\n");
  delay(200);
}
