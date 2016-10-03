
void setup()  
{
  Serial.begin(9600);    // Open serial communications 
}

void loop(){
  
  // wait until data comes in from Pi
  //while(!Serial.available())
  //{
  //}
  
  char data = Serial.read();
  Serial.print(data);
  
  Serial.println("yee");
}


