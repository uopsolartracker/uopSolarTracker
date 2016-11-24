#include <Herkulex.h>
//int n=2; //motor ID - verify your ID !!!!

String data;
//String data1;
//String data2;

// Vertical controlling motor variables
int vertical_motorID = 0;
int vertical_change = 0;
int vertical_cur_angle = 0;
int vertical_angle = 0;

// Horizontal controlling motor variables
int horizontal_motorID = 2;
int horizontal_change = 0;
int horizontal_cur_angle = 0;
int horizontal_angle = 0;

void setup()  
{
  delay(2000);  //a delay to have time for serial monitor opening
  Serial.begin(115200);          // Open serial communications
  Serial.println("Begin");
  Herkulex.beginSerial1(115200); //open serial port 1
 
  Herkulex.reboot(vertical_motorID); //reboot vertical motor
  Herkulex.reboot(horizontal_motorID); //reboot horizontal motor
  
  delay(500); 
  Herkulex.initialize(); //initialize motors TODO: Check if this works for two motors on the bus
  delay(200);
  
  Herkulex.setLed(vertical_motorID, 0x6);
  Herkulex.setLed(horizontal_motorID, 0x6);
  
}

void loop(){
  
  // wait until data comes in from Pi
  if (Serial.available())
  {
    Serial.print("Vertical A at Loop Start= ");
    Serial.println(Herkulex.getAngle(vertical_motorID));
    Serial.print("Vertical P at Loop Start= ");
    Serial.println(Herkulex.getPosition(vertical_motorID));
    
    Serial.print("Horizontal A at Loop Start= ");
    Serial.println(Herkulex.getAngle(horizontal_motorID));
    Serial.print("Horizontal P at Loop Start= ");
    Serial.println(Herkulex.getPosition(horizontal_motorID));
    
    data = Serial.readString();  // read each byte (char) of incoming data
    Serial.println(data);
    
    if (data == "r")
    {
      Serial.println("Reboot");
      Herkulex.reboot(vertical_motorID);
      Herkulex.reboot(horizontal_motorID);
      delay(1000);
      Herkulex.initialize();
      delay(100);
    }
    else if (data == "stat")
    {
      Serial.println("Vertical Motor Stat = ");
      Serial.println(Herkulex.stat(vertical_motorID));
      
      Serial.println("Horizontal Motor Stat = ");
      Serial.println(Herkulex.stat(horizontal_motorID));
    }
    else if (data == "p")    // position request
    {
      Serial.println('v');
      Serial.println(Herkulex.getPosition(vertical_motorID));
      Serial.println('h');
      Serial.println(Herkulex.getPosition(horizontal_motorID));
    }
    else if (data == "v")  // move vertical angle motor
    {
      while(!Serial.available())
      {
        //add a timeout
      }
      
      if (Serial.available())
      {
      Serial.println('v');
      // Read in the new position and send to motor
      data = Serial.readString();
      //data = data.toInt();
      Herkulex.moveOne(vertical_motorID, data.toInt(), 1500, 1);
      
      // For relative angle (if needed)
      //vertical_cur_angle = Herkulex.getAngle(vertical_motorID);
      //vertical_angle = vertical_cur_angle + data  ;
      //Herkulex.moveOneAngle(vertical_motorID, vertical_angle, 1000, 1);
      
      // Return current angle of mirror
      Serial.println(Herkulex.getPosition(vertical_motorID));
      }
    }
    else if (data == "h")
    {
      while(!Serial.available())
      {
        //add a timeout
      }
      
      if (Serial.available())
      {
      Serial.println('h');
      // Read in the new position and send to motor
      data = Serial.readString();
      //data = data.toInt();
      Herkulex.moveOne(horizontal_motorID, data.toInt(), 1500, 2);

      // For relative angle (if needed)
      //horizontal_cur_angle = Herkulex.getAngle(vertical_motorID);
      //horizontal_angle = horizontal_cur_angle + data;
      //Herkulex.moveOneAngle(horizontal_motorID, horizontal_angle, 1000, 1);
      
      // Return current angle of mirror
      Serial.println(Herkulex.getPosition(horizontal_motorID));
      }
    }
    else
    {
      Serial.println("Got data");
      Serial.println(data);
    
      delay(10); 
      //Herkulex.moveSpeedOne(vertical_motorID, 300, 672, 1); //move motor with 300 speed  
      Herkulex.moveOne(vertical_motorID, data.toInt(), 1500, 1); //move to position 200 in 1500 milliseconds
      Herkulex.setLed(vertical_motorID, 0x6);
      delay(2000);
      Serial.print("Vertical Position = ");
      Serial.println(Herkulex.getPosition(vertical_motorID));
      
      delay(2000);

      //Herkulex.moveSpeedOne(horizontal_motorID, -300, 672, 2); //move motor with -300 speed
      Herkulex.moveOne(horizontal_motorID, data.toInt(), 1500, 2); //move to 820 position in 500 milliseconds
      delay(2000);
      Serial.print("Horizontal Position = ");
      Serial.println(Herkulex.getPosition(horizontal_motorID));
    
      //Herkulex.moveOneAngle(vertical_motorID, data.toInt(), 1000, LED_GREEN); //move motor with 300 speed 
      //delay(6000);
      //Herkulex.moveOneAngle(horizontal_motorID, data.toInt(), 1000, LED_BLUE); 
    
  
      //Serial.println(Herkulex.stat(horizontal_motorID));
      //Herkulex.setLed(horizontal_motorID, LED_BLUE);
      //Serial.println(Herkulex.getAngle(horizontal_motorID));
    
    }
   
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




