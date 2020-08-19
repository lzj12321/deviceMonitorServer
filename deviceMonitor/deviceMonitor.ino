#include <EEPROM.h>
#include <ArduinoOTA.h>
#include <ESP8266WiFi.h>
#include <ESP8266WiFiGratuitous.h>
#include <ESP8266WiFiMulti.h>
#include <WiFiClient.h>
#include <WiFiClientSecure.h>
#include <WiFiServer.h>
#include <WiFiServerSecure.h>
#include <WiFiUdp.h>


/* work states declartion */
#define NORMAL 3
#define STOP 4
#define PAUSE 5

#define MAX_CONNECT_WIFI_TIME 5
#define MAX_CONNECT_SERVER_TIME 10
#define MIN_DETECTED_SIGNAL_TIME 10

#define MONITOR_MODE 0
#define OTA_MODE 1
#define IDLE_MODE 2
#define UNKNOWN_MODE 3
#define CALCULATE_MODE 4

String checkConnectionMsg="";
const int workModeAddress=1;
IPAddress localIp(192, 168, 1, 34);
IPAddress gateway(192, 168, 1, 1);
IPAddress subnet(255, 255, 255, 0);
struct stru_netWorkParam {
    String ssid = "TEXE-Robot";
    String ssidPasswd = "JX_TELUA";
    String serverIp = "192.168.16.106";
  
//  String ssid = "NETGEAR";
//  String ssidPasswd = "sj13607071774";
//  String serverIp = "10.0.0.3";

//  String ssid = "TEXE-MONITOR";
//  String ssidPasswd = "JX_TELUA";
//  String serverIp = "192.168.1.100";

  unsigned int serverPort = 8888;
};

struct stru_deviceParam {
  String deviceSerial = "xe_line3_ultra";
  String firmWareVersion = "1";
  int workMode = CALCULATE_MODE;
  unsigned int workState = NORMAL;
};

struct stru_ioParam {
  unsigned int stopIO = 14;
  unsigned int pauseIO = 12;
  unsigned int detectSensorIO=4;
};

struct stru_msgParam {
  const String splitFlag = ":";
  const String stopMsg = "stop";
  const String pauseMsg = "pause";
  const String restartMsg = "restart";
  const String setMonitorMsg = "monitor";
  const String setIdleMsg = "idle";
  const String setOtaMsg = "ota";
  const String setCalculateMsg="calculate";
  const String calculateCheckMsg="calculate_check";
  const String otaCheckMsg = "ota_check";
  const String monitorCheckMsg = "monitor_check";
  const String idleCheckMsg = "idle_check";
  const String calculateMsg="calculate-";
  const String unknownCheckMsg = "unknown_check";
  const String clearProductMsg="clear_productData";
};

struct stru_productParam {
  unsigned int productedNum1 = 0;
  unsigned int productedNum2 = 0;
  String productModel = "";

  unsigned int detectedSignalTime=0;
  unsigned int minDetectedSignalTime=5;
  unsigned int minDetectInterval=10;
  unsigned int detectInterval=0;

  /* max calculate num is 65280*/
  unsigned int productedNumAddress1=2;
  unsigned int productedNumAddress2=3;
  unsigned int isDetectRiseAddress=4;
  bool isDetectRise=true;
};

/* device param */
struct stru_deviceParam deviceParam;

/* network param */
WiFiClient client;
struct stru_netWorkParam networkParam;

/* io param */
struct stru_ioParam ioParam;

/* msg param */
struct stru_msgParam msgParam;

/* product param */
struct stru_productParam productParam;

/* Timer param*/
int loopInterval = 1000;
unsigned int loopTime=0;
int detectNormalTime = 0;
int detectStopSignalTime = 0;
int detectPauseSignalTime = 0;
int retryConnectWifiTime = 0;
int retryConnectServerTime = 0;

//loop connect the wifi until connected//
void connectWifi() {
  Serial.print("Connecting to ");
  Serial.print(networkParam.ssid);
//  WiFi.config(localIp, gateway, subnet);
  WiFi.mode(WIFI_STA);
  WiFi.begin(networkParam.ssid, networkParam.ssidPasswd);
  while (WiFi.status() != WL_CONNECTED)
  {
    Serial.print(".");
    retryConnectWifiTime++;
    if (retryConnectWifiTime > MAX_CONNECT_WIFI_TIME) {
      Serial.println("restart the chip now!");
      ESP.restart();
    }
    delay(5000);
  }
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());//WiFi.localIP()返回8266获得的ip地址
}

//loop connect the server until connected//
void connectServer() {
  while (!client.connected())//几个非连接的异常处理
  {
    if (!client.connect(networkParam.serverIp, networkParam.serverPort))
    {
      Serial.print("connecting server:");
      Serial.println(networkParam.serverIp);
      retryConnectServerTime++;
      if (retryConnectServerTime > MAX_CONNECT_SERVER_TIME) {
        Serial.println("restart the chip now!");
        ESP.restart();
      }
      delay(1000);
    }
    else {
      retryConnectServerTime = 0;
      if (deviceParam.workMode == MONITOR_MODE) {
        sendMsg(msgParam.monitorCheckMsg);
      }
      else if (deviceParam.workMode == OTA_MODE) {
        sendMsg(msgParam.otaCheckMsg);
      }
      else if (deviceParam.workMode == IDLE_MODE) {
        sendMsg(msgParam.idleCheckMsg);
      }
      else if (deviceParam.workMode == CALCULATE_MODE) {
        sendMsg(msgParam.calculateCheckMsg);
      }
      else {
        deviceParam.workMode = UNKNOWN_MODE;
        sendMsg(msgParam.unknownCheckMsg);
      }
      client.setSync(true);
      Serial.print("connected server:");
      Serial.println(networkParam.serverIp);
    }
  }
}

void initializeWorkmode(){
  deviceParam.workMode = readWorkModeFromRom();
  Serial.print("work mode:");
  Serial.println(deviceParam.workMode);
  if(deviceParam.workMode==OTA_MODE){
    OTA_Mode_Ini();
  }
  
  if(deviceParam.workMode==CALCULATE_MODE){
    CALCULATE_Mode_Ini();
  }
  
  if(deviceParam.workMode==MONITOR_MODE){
    MONITOR_Mode_Ini();
  }
}

void setup(){
  /*initialize EEPROM*/
  EEPROM.begin(512);

  //initialize serial//
  Serial.begin(115200);
  delay(50);

  //connect wifi//
  connectWifi();

  //connect server//
  connectServer();

  //initialize workmode//
  initializeWorkmode();
}

void processMsgFromServer(String msg) {
  if (msg == msgParam.setOtaMsg)
  {
    if (deviceParam.workMode != OTA_MODE) {
      //initialize the ota env//
      OTA_Mode_Ini();
      Serial.println("enter ota mode");
      deviceParam.workMode = OTA_MODE;
      writeWorkModeToRom(deviceParam.workMode);
    }
    sendMsg(msgParam.otaCheckMsg);
  }
  else if (msg == msgParam.setCalculateMsg)
  {
    if (deviceParam.workMode != CALCULATE_MODE) {
      //initialize the calculate env//
      CALCULATE_Mode_Ini();
      Serial.println("enter calculate mode");
      deviceParam.workMode = CALCULATE_MODE;
      writeWorkModeToRom(deviceParam.workMode);
    }
    sendMsg(msgParam.calculateCheckMsg);
  }
  else if (msg == msgParam.setMonitorMsg) {
    if (deviceParam.workMode != MONITOR_MODE) {
      Serial.println("enter monitor mode");
      MONITOR_Mode_Ini();
      deviceParam.workMode = MONITOR_MODE;
      writeWorkModeToRom(deviceParam.workMode);
    }
    sendMsg(msgParam.monitorCheckMsg);
  }
  else if (msg == msgParam.setIdleMsg) {
    if (deviceParam.workMode != IDLE_MODE) {
      Serial.println("enter idle mode");
      deviceParam.workMode = IDLE_MODE;
      writeWorkModeToRom(deviceParam.workMode);
    }
    sendMsg(msgParam.idleCheckMsg);
  }
  else if (msg == msgParam.restartMsg) {
    Serial.println("restart!");
    ESP.restart();
  }
  else if(msg==msgParam.clearProductMsg){
    EEPROM.write(productParam.productedNumAddress1,0);
    EEPROM.write(productParam.productedNumAddress2,0);
    EEPROM.write(productParam.isDetectRiseAddress,1);
    
    if (EEPROM.commit()) {
      Serial.println("EEPROM successfully clear product num!");
    } else {
      Serial.println("ERROR! failed to clear product num!");
    }
  }
  else if (msg != "") {
    Serial.println("unknown order:" + msg);
  }
}

void loop(){
  if (client.connected()){
    if (client.available())
    {
      String msg = client.readStringUntil('\n');
      processMsgFromServer(msg);
    }
    switch (deviceParam.workMode) {
      case MONITOR_MODE: {
          MONITOR_Mode_Run();
          break;
        }
      case OTA_MODE: {
          OTA_Mode_Run();
          break;
        }
      case IDLE_MODE: {
          IDLE_Mode_Run();
          break;
        }
      case CALCULATE_MODE: {
          CALCULATE_Mode_Run();
          break;
        }
      case UNKNOWN_MODE: {
          sendMsg(msgParam.unknownCheckMsg);
          delay(5000);
          break;
        }
      default: {
          Serial.println("no task mode");
          delay(5000);
        }
    }
    if(loopTime>10)
    {
      sendMsg(checkConnectionMsg);
      loopTime=0;
    }
  }
  ++loopTime;
  delay(loopInterval);
}

void sendMsg(const String msg){
  if(!client.connected()){
    Serial.println("Disconnect from server,send msg error!");
    return;
  }
  String result = deviceParam.deviceSerial + msgParam.splitFlag + msg;
  client.write(result.c_str());
}

void MONITOR_Mode_Ini() {
  pinMode(ioParam.stopIO, INPUT);
  pinMode(ioParam.pauseIO, INPUT);
  checkConnectionMsg=msgParam.monitorCheckMsg;
}

void CALCULATE_Mode_Ini(){
  pinMode(ioParam.detectSensorIO, INPUT);

  productParam.productedNum1=int(EEPROM.read(productParam.productedNumAddress1));
  productParam.productedNum2=int(EEPROM.read(productParam.productedNumAddress2));
  productParam.isDetectRise=bool(EEPROM.read(productParam.isDetectRiseAddress));
  checkConnectionMsg=msgParam.calculateCheckMsg;
}

void OTA_Mode_Ini() {
  ArduinoOTA.onStart([]() {
    String type;
    if (ArduinoOTA.getCommand() == U_FLASH) {
      type = "sketch";
    } else { // U_FS
      type = "filesystem";
    }

    // NOTE: if updating FS this would be the place to unmount FS using FS.end()
    Serial.println("Start updating " + type);
  });
  ArduinoOTA.onEnd([]() {
    Serial.println("\nEnd");
  });
  ArduinoOTA.onProgress([](unsigned int progress, unsigned int total) {
    Serial.printf("Progress: %u%%\r", (progress / (total / 100)));
  });
  ArduinoOTA.onError([](ota_error_t error) {
    Serial.printf("Error[%u]: ", error);
    if (error == OTA_AUTH_ERROR) {
      Serial.println("Auth Failed");
    } else if (error == OTA_BEGIN_ERROR) {
      Serial.println("Begin Failed");
    } else if (error == OTA_CONNECT_ERROR) {
      Serial.println("Connect Failed");
    } else if (error == OTA_RECEIVE_ERROR) {
      Serial.println("Receive Failed");
    } else if (error == OTA_END_ERROR) {
      Serial.println("End Failed");
    }
  });
  ArduinoOTA.setHostname(deviceParam.deviceSerial.c_str());
  ArduinoOTA.setRebootOnSuccess(true);
  ArduinoOTA.begin();
  checkConnectionMsg=msgParam.otaCheckMsg;
}

void IDLE_Mode_Ini(){
  checkConnectionMsg=msgParam.idleCheckMsg;
}

void MONITOR_Mode_Run(){
  if (digitalRead(ioParam.stopIO))
  {
    ++detectStopSignalTime;
    detectPauseSignalTime = 0;
    if (deviceParam.workState != STOP && (detectStopSignalTime > MIN_DETECTED_SIGNAL_TIME)) {
      detectNormalTime = 0;
      deviceParam.workState = STOP;
      sendMsg(msgParam.stopMsg);
      checkConnectionMsg=msgParam.stopMsg;
      detectStopSignalTime = 0;
    }
  }
  else if (digitalRead(ioParam.pauseIO))
  {
    ++detectPauseSignalTime;
    detectStopSignalTime = 0;
    if(deviceParam.workState != PAUSE && (detectPauseSignalTime > MIN_DETECTED_SIGNAL_TIME)) {
      detectNormalTime = 0;
      deviceParam.workState = PAUSE;
      sendMsg(msgParam.pauseMsg);
      checkConnectionMsg=msgParam.pauseMsg;
      detectPauseSignalTime = 0;
    }
  }
  else
  {
    detectPauseSignalTime = 0;
    detectStopSignalTime = 0;
    detectNormalTime++;
    if (deviceParam.workState!=NORMAL)
    {
      deviceParam.workState = NORMAL;
      sendMsg(msgParam.monitorCheckMsg);
      checkConnectionMsg=msgParam.monitorCheckMsg;
      detectNormalTime = 0;
    }
  }
}

void OTA_Mode_Run() {
  ArduinoOTA.handle();
  // detectNormalTime++;
  // if (detectNormalTime > (MIN_DETECTED_SIGNAL_TIME * 2))
  // {
  //   deviceParam.workState = NORMAL;
  //   sendMsg(msgParam.otaCheckMsg);
  //   detectNormalTime = 0;
  //   detectPauseSignalTime = 0;
  //   detectStopSignalTime = 0;
  // }
}

void IDLE_Mode_Run() {
  // sendMsg(msgParam.idleCheckMsg);
  // delay(5000);
  Serial.println("IDLE MODE RUNNING!");
}

void CALCULATE_Mode_Run(){
  Serial.print("sensor state:");
  Serial.println(digitalRead(ioParam.detectSensorIO));
  Serial.print("isDetectRise:");
  Serial.println(productParam.isDetectRise);

  if(productParam.isDetectRise){
    if(!digitalRead(ioParam.detectSensorIO)){
      ++productParam.detectedSignalTime;
    }
    if(productParam.detectedSignalTime>productParam.minDetectedSignalTime){
      productParam.isDetectRise=!productParam.isDetectRise;
      calculateAddNum();
      saveDetectMode();
      productParam.detectedSignalTime=0;
    }
  }else{
    if(digitalRead(ioParam.detectSensorIO)){
      ++productParam.detectedSignalTime;
    }
    if(productParam.detectedSignalTime>productParam.minDetectedSignalTime){
      productParam.detectedSignalTime=0;
      productParam.isDetectRise=!productParam.isDetectRise;
      saveDetectMode();
    }
  }
}

int readWorkModeFromRom() {
  byte _value = EEPROM.read(workModeAddress);
  Serial.print("read work mode: ");
  Serial.println(_value, DEC);
  delay(500);
  return int(_value);
}

void writeWorkModeToRom(int workMode) {
  EEPROM.write(workModeAddress, workMode);
  if (EEPROM.commit()) {
    Serial.println("EEPROM successfully save work mode!");
  } else {
    Serial.println("ERROR! failed to save work mode!");
  }
  delay(100);
}

void calculateAddNum(){
  Serial.println("add a num!");
  if(productParam.productedNum1==255){
    productParam.productedNum1=0;
    ++productParam.productedNum2;
  }else{
    ++productParam.productedNum1;
  }

  unsigned int productedNum=productParam.productedNum2*255+productParam.productedNum1;

  EEPROM.write(productParam.productedNumAddress1,productParam.productedNum1);
  delay(30);
  EEPROM.write(productParam.productedNumAddress2,productParam.productedNum2);
  delay(30);
  if (EEPROM.commit()) {
    Serial.println("EEPROM successfully save product num!");
  } else {
    Serial.println("ERROR! failed to save product num!");
  }
  Serial.print("calculate msg:");
  Serial.println(msgParam.calculateMsg+String(productedNum));
  sendMsg(msgParam.calculateMsg+String(productedNum));
}

void saveDetectMode(){
  EEPROM.write(productParam.isDetectRiseAddress,productParam.isDetectRise);
  if (EEPROM.commit()) {
    Serial.println("EEPROM successfully save detect mode!");
  } else {
    Serial.println("ERROR! failed to save detect mode!");
  }
  delay(30);
}
