#include "interrupt.h"

void setup() {
  //initialize interrupt
  init_interrupt();
  // put your setup code here, to run once:
  pinMode(VALVE_1, OUTPUT); //screw terminal 1
  pinMode(VALVE_2, OUTPUT); //screw terminal 2
  pinMode(UPPER_GLIGHT, OUTPUT); //output 1
  pinMode(LOWER_GLIGHT, OUTPUT); //output 2
  pinMode(FISH_LIGHT, OUTPUT); //output 3
  pinMode(PUMP, OUTPUT);//pump
  digitalWrite(PUMP, LOW); //always keep pump on
  digitalWrite(VALVE_1, LOW);
  digitalWrite(VALVE_2, HIGH);
  
}
//im replacing the delay functions in the light cylce loop with the flood cycle loop
void loop() {
  double flood_interval = 5; //flood interval= 10 min
  // turn on all lights
  digitalWrite(UPPER_GLIGHT, LOW);
  digitalWrite(LOWER_GLIGHT, LOW);
  digitalWrite(FISH_LIGHT, LOW);
    for(int i=0; i<fish_light_dur * 60 * 60 * 1000/(2*flood_interval*1000); i++){
      digitalWrite(VALVE_1, HIGH);
      digitalWrite(VALVE_2, LOW);
      delay(flood_interval*60*1000); //delay x min
      digitalWrite(VALVE_1, LOW);
      digitalWrite(VALVE_2, HIGH);
      delay(flood_interval*60*1000); //delay x min
    }
    
  //delay(fish_light_dur * 60 * 60 * 1000);  //previous for loop should accomplish this

  //turn off fish light
  digitalWrite(FISH_LIGHT, HIGH);
  //delay((upper_glight_dur-fish_light_dur) * 60* 60* 1000);
    for(int i=0; i<fish_light_dur * 60 * 60 * 1000/(2*flood_interval*1000); i++){ //loops as many times as necessary to equal time elapsed by prev delay
      digitalWrite(VALVE_1, HIGH);
      digitalWrite(VALVE_2, LOW);
      delay(flood_interval*60*1000); //delay x min
      digitalWrite(VALVE_1, LOW);
      digitalWrite(VALVE_2, HIGH);
      delay(flood_interval*60*1000); //delay x min
    }
    
  //turn off plant lights 
  digitalWrite(UPPER_GLIGHT, HIGH);
  digitalWrite(LOWER_GLIGHT, HIGH);
  
 
    for(int i=0; i<fish_light_dur * 60 * 60 * 1000/(2*flood_interval*1000); i++){
      digitalWrite(VALVE_1, HIGH);
      digitalWrite(VALVE_2, LOW);
      delay(flood_interval*60*1000); //delay x min
      digitalWrite(VALVE_1, LOW);
      digitalWrite(VALVE_2, HIGH);
      delay(flood_interval*60*1000); //delay x min
    }
   //delay((24-upper_glight_dur) * 60 * 60 * 1000);



  
}
