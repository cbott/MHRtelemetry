const int SIZE = 10;
const char TERM = 255;

byte x[SIZE];
void setup() {
  Serial1.begin(9600);
  for(int i=0; i<SIZE; ++i){
    x[i] = i;
  }

  pinMode(13, OUTPUT);
}

void loop() {
  for(int i=0; i<SIZE; ++i){
    Serial1.write(x[i]);
  }
  Serial1.write(TERM);
  digitalWrite(13, x[1] % 2 == 0);
  ++x[1];
  if(x[1] == 255) ++x[1];
  delay(random(100, 500));
}
