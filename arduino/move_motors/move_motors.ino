#include <Herkulex.h>

String data;

// Vertical controlling motor variables
int vertical_motorID = 0;
int vertical_change = 0;
int vertical_cur_angle = 0;
int vertical_angle = 0;

// Horizontal controlling motor variables
//int horizontal_motorID = 1;
//int horizontal_change = 0;
//int horizontal_cur_angle = 0;
//int horizontal_angle = 0;

void setup()  
{
  delay(2000);  //a delay to have time for serial monitor opening
  Serial.begin(9600);    // Open serial communications
  //Serial.println("Begin");
  Herkulex.begin(57600,10,11); //open serial with rx=10 and tx=11 
  
  Herkulex.reboot(vertical_motorID); //reboot vertical motor
  //Herkulex.reboot(horizontal_motorID); //reboot horizontal motor
  
  delay(500); 
  Herkulex.initialize(); //initialize motors TODO: Check if this works for two motors on the bus
  delay(200);

  // send current motor angles to Pi
  //Serial.println('v');
  //Serial.println(Herkulex.getAngle(vertical_motorID));
  //Serial.println('h');
  //Serial.println(Herkulex.getAngle(horizontal_motorID));  
}

void loop(){
  
  // wait until data comes in from Pi
  if (Serial.available())
  {
    data = Serial.readString();  // read each byte (char) of incoming data

    Herkulex.moveOneAngle(vertical_motorID, data.toInt(), 1000, LED_BLUE); //move motor with 300 speed  
    
    Serial.println(data);

  }
  // input angle to move by
  //if read 'v', move vertical. if read 'h', move horizontal
  //vertical_change = Serial.read();
  //horizontal_change = Serial.read();
  
  // get current angle of motors
  //vertical_cur_angle = Herkulex.getAngle(vertical_motorID);
  //vertical_angle = vertical_cur_angle + vertical_change;
  //horizontal_cur_angle = Herkulex.getAngle(horizontal_motorID);
  //horizontal_angle = horizontal_cur_angle + horizontal_change;
  
  // move motors (-160 deg to 160 deg)
  //Herkulex.moveOneAngle(vertical_motorID, vertical_angle, 1000, LED_BLUE); //move motor with 300 speed  
  //Herkulex.moveOneAngle(horizontal_motorID, horizontal_angle, 1000, LED_GREEN); //move motor with 300 speed  
  
  // send current angle to Pi
  //Serial.println(Herkulex.getAngle(vertical_motorID));
  //Serial.println(Herkulex.getAngle(horizontal_motorID));
  
}


