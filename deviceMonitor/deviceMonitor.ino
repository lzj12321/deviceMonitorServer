#include <EEPROM.h>
#include <ArduinoOTA.h>
#include <BearSSLHelpers.h>
#include <CertStoreBearSSL.h>
#include <ESP8266WiFi.h>
#include <ESP8266WiFiAP.h>
#include <ESP8266WiFiGeneric.h>
#include <ESP8266WiFiGratuitous.h>
#include <ESP8266WiFiMulti.h>
#include <ESP8266WiFiScan.h>
#include <ESP8266WiFiSTA.h>
#include <ESP8266WiFiType.h>
#include <WiFiClient.h>
#include <WiFiClientSecure.h>
#include <WiFiClientSecureAxTLS.h>
#include <WiFiClientSecureBearSSL.h>
#include <WiFiServer.h>
#include <WiFiServerSecure.h>
#include <WiFiServerSecureAxTLS.h>
#include <WiFiServerSecureBearSSL.h>
#include <WiFiUdp.h>


// enum WORK_STATE{
//   CATCH_ERROR,HIPOT,NORMAL,STOP,PAUSE
// }

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

struct stru_netWorkParam{
  String ssid="TEXE-Robot";
  String ssidPasswd="JX_TELUA";
  String serverIp="192.168.16.106";
//  String ssid="NETGEAR";
//  String ssidPasswd="sj13607071774";
//  String serverIp="10.0.0.11";
  unsigned int serverPort=8888; 
};

struct stru_deviceParam{
  String deviceSerial="xe_line3_robot3";
  String firmWareVersion="1";
  int workMode=MONITOR_MODE;
  unsigned int workState=NORMAL;
};

struct stru_ioParam{
  unsigned int stopIO=14;
  unsigned int pauseIO=12;
};

struct stru_msgParam{
  const String splitFlag = ":";
  const String stopMsg = "stop";
  const String pauseMsg = "pause";
  const String restartMsg="restart";
  const String setMonitorMsg="monitor";
  const String setIdleMsg="idle";
  const String setOtaMsg="ota";
  const String otaCheckMsg = "ota_check";
  const String monitorCheckMsg = "monitor_check";
  const String idleCheckMsg="idle_check";
  const String unknownCheckMsg="unknown_check";
};

struct stru_productParam{
  unsigned int productedNum=0;
  String productModel="";
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

/* Timer param*/
int loopInterval = 300;
int detectNormalTime = 0;
int detectStopSignalTime = 0;
int detectPauseSignalTime = 0;
int retryConnectWifiTime = 0;
int retryConnectServerTime = 0;

//loop connect the wifi until connected//
void connectWifi(){
  Serial.print("Connecting to ");
  Serial.print(networkParam.ssid);
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
void connectServer(){
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
      delay(500);
    }
    else {
      retryConnectServerTime = 0;
      if(deviceParam.workMode==MONITOR_MODE){
        sendMsg(msgParam.monitorCheckMsg);
      }
      else if(deviceParam.workMode == OTA_MODE){
        sendMsg(msgParam.otaCheckMsg);
      }
      else if(deviceParam.workMode==IDLE_MODE){
        sendMsg(msgParam.idleCheckMsg);
      }
      else{
        deviceParam.workMode=UNKNOWN_MODE;
        sendMsg(msgParam.unknownCheckMsg);
        // ESP.restart();
      }
      Serial.print("connected server:");
      Serial.println(networkParam.serverIp);
    }
  }
}

//initialize io//
void initializeIO(){
  pinMode(ioParam.stopIO, INPUT);
  pinMode(ioParam.pauseIO, INPUT);
}

void initializeWorkmode(){
  deviceParam.workMode=readWorkModeFromRom();
}

void setup()
{
  /*initialize EEPROM*/
  EEPROM.begin(512);
  
  /*intialize the io mode*/
  initializeIO();

  //initialize serial//
  Serial.begin(115200);
  delay(50);

  //connect wifi//
  connectWifi();

  //initialize workmode//
  initializeWorkmode();
}

void processMsgFromServer(String msg){
  if (msg == msgParam.setOtaMsg)
    {
      if (deviceParam.workMode != OTA_MODE){
        //initialize the ota env//
        OTA_Mode_Ini();
        Serial.println("enter ota mode");
        deviceParam.workMode = OTA_MODE;
        writeWorkModeToRom(deviceParam.workMode);
      }
      sendMsg(msgParam.otaCheckMsg);
    }
    else if (msg == msgParam.setMonitorMsg){
      if (deviceParam.workMode != MONITOR_MODE) {
        Serial.println("enter monitor mode");
        deviceParam.workMode = MONITOR_MODE;
        writeWorkModeToRom(deviceParam.workMode);
      }
      sendMsg(msgParam.monitorCheckMsg);
    }
    else if(msg== msgParam.setIdleMsg){
      if(deviceParam.workMode!=IDLE_MODE){
        Serial.println("enter idle mode");
        deviceParam.workMode=IDLE_MODE;
        writeWorkModeToRom(deviceParam.workMode);
      }
      sendMsg(msgParam.idleCheckMsg);
    }
    else if(msg==msgParam.restartMsg){
      Serial.println("restart!");
      ESP.restart();
    }
    else if (msg != "") {
      Serial.println("unknown order:" + msg);
    }
}

void loop()
{
  /* connect wifi*/
  connectServer();

  while (client.connected()) {
    String msg = readMsg();
    processMsgFromServer(msg);

    switch (deviceParam.workMode) {
      case MONITOR_MODE: {
          MONITOR_Mode_Run();
          break;
        }
      case OTA_MODE: {
          OTA_Mode_Run();
          break;
        }
      case IDLE_MODE:{
        IDLE_Mode_Run();
      }
      default: {
          Serial.println("no task mode");
          delay(2000);
        }
    }
    delay(loopInterval);
  }
}

void sendMsg(const String msg) {
  String result = deviceParam.deviceSerial + msgParam.splitFlag + msg;
  client.write(result.c_str());
  client.flush();
}

String readMsg() {
  if (!client.available())
  {
    return "";
  }
  String msg = client.readStringUntil('\n');
  if (msg != "") {
    Serial.println("msg:" + msg);
    return msg;
  }
  else {
    return "";
  }
}

void MONITOR_Mode_Run() {
  if (digitalRead(ioParam.stopIO))
  {
    ++detectStopSignalTime;
    detectPauseSignalTime = 0;
    if ((deviceParam.workState != STOP && (detectStopSignalTime > MIN_DETECTED_SIGNAL_TIME)) || detectStopSignalTime > ( MIN_DETECTED_SIGNAL_TIME * 5)) {
      detectNormalTime = 0;
      deviceParam.workState = STOP;
      sendMsg(msgParam.stopMsg);
      detectStopSignalTime = 0;
    }
  }
  else if (digitalRead(ioParam.pauseIO))
  {
    ++detectPauseSignalTime;
    detectStopSignalTime = 0;
    if ((deviceParam.workState != PAUSE && (detectPauseSignalTime > MIN_DETECTED_SIGNAL_TIME)) || detectPauseSignalTime > (MIN_DETECTED_SIGNAL_TIME * 5)) {
      detectNormalTime = 0;
      deviceParam.workState = PAUSE;
      sendMsg(msgParam.pauseMsg);
      detectPauseSignalTime = 0;
    }
  }
  else
  {
    detectPauseSignalTime = 0;
    detectStopSignalTime = 0;
    detectNormalTime++;
    if (detectNormalTime > (MIN_DETECTED_SIGNAL_TIME * 5))
    {
      deviceParam.workState = NORMAL;
      sendMsg(msgParam.monitorCheckMsg);
      detectNormalTime = 0;
    }
  }
}

void OTA_Mode_Run() {
  ArduinoOTA.handle();
  detectNormalTime++;
  if (detectNormalTime > (MIN_DETECTED_SIGNAL_TIME * 5))
  {
    deviceParam.workState = NORMAL;
    sendMsg(msgParam.otaCheckMsg);
    detectNormalTime = 0;
    detectPauseSignalTime = 0;
    detectStopSignalTime = 0;
  }
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
}

void IDLE_Mode_Run(){
  sendMsg(msgParam.idleCheckMsg);
  delay(5000);
  // Serial.println("")
}

int readWorkModeFromRom(){
    int workModeAddress=1;
    byte _value=EEPROM.read(workModeAddress);
    Serial.print("work mode: ");
    Serial.println(_value,DEC);
    Serial.print("value: ");
    Serial.println(int(_value));
    delay(500);
    return int(_value);
}

void writeWorkModeToRom(int workMode){
    int addr = 1;
    EEPROM.write(addr, workMode);
    if (EEPROM.commit()) {
      Serial.println("EEPROM successfully save work mode!");
    } else {
      Serial.println("ERROR! failed to save work mode!");
    }
    delay(100);
}
