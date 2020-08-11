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

/* states declartion */
#define ANFANG 0
#define CATCH_ERROR 1
#define HIPOT 2
#define NORMAL 3
#define STOP 4
#define PAUSE 5


#define MAX_CONNECT_WIFI_TIME 5
#define MAX_CONNECT_SERVER_TIME 10
#define MIN_DETECTED_SIGNAL_TIME 10

#define MONITOR_MODE 0
#define OTA_MODE 1

/* robot serialNum */
const String robotFlag = "xe_line4_ultra";

/* work mode and firmWare version */
unsigned int workMode = MONITOR_MODE;
const String firmWareVersion = "0.1";

/* wifi param */
char *ssid     = "TEXE-Robot";//wifi ssid
char *password = "JX_TELUA";//wifi password

/* server param */
WiFiClient client;
const char *host = "192.168.16.106";//server ip
const int tcpPort = 8888;//server port

/* io param */
const int hipotIO = 34;
const int catchErrorIO = 35;
const int anfangIO = 39;
const int stopIO = 14;
const int pauseIO = 12;

/* msg param */
const String splitFlag = ":";
const String anfangMsg = "anfang";
const String hipotMsg = "hipot";
const String catchErrorMsg = "catchError";
const String checkMsg = "check";
const String stopMsg = "stop";
const String pauseMsg = "pause";
const String otaCheckMsg = "ota_check";
const String monitorCheckMsg = "monitor_check";
const String unknowWorkModeMsg="unknownWorkmode";

/* Timer param*/
int checkInterval = 300;
int currentRobotState = NORMAL;
int detectNormalTime = 0;
int detectStopSignalTime = 0;
int detectPauseSignalTime = 0;
int retryConnectWifiTime = 0;
int retryConnectServerTime = 0;

void setup()
{
  // pinMode(4, OUTPUT);
  // digitalWrite(4, HIGH);
  // pinMode(hipotIO,INPUT);
  // pinMode(catchErrorIO,INPUT);
  // pinMode(anfangIO,INPUT);
  pinMode(stopIO, INPUT);
  pinMode(pauseIO, INPUT);

  Serial.begin(9600);
  delay(50);
  Serial.println("test ota");
  Serial.print("Connecting to ");
  Serial.print(ssid);
  WiFi.begin(ssid, password);
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
  otaIni();
}

void loop()
{
  while (!client.connected())//几个非连接的异常处理
  {
    if (!client.connect(host, tcpPort))
    {
      Serial.print("connecting server:");
      Serial.println(host);
      retryConnectServerTime++;
      if (retryConnectServerTime > MAX_CONNECT_SERVER_TIME) {
        Serial.println("restart the chip now!");
        ESP.restart();
      }
      delay(500);
    }
    else {
      retryConnectServerTime = 0;
      if(workMode==MONITOR_MODE){
        sendMsg(monitorCheckMsg);
      }
      else if(workMode==OTA_MODE){
        sendMsg(otaCheckMsg);
      }
      else{
        sendMsg(unknowWorkModeMsg);
        ESP.restart();
      }
      Serial.print("connected server:");
      Serial.println(host);
    }
  }

  while (client.connected()) {
    String msg = readMsg();
    if (msg == "ota")
    {
      if (workMode != OTA_MODE) {
        Serial.println("enter ota mode");
        workMode = OTA_MODE;
      }
      sendMsg(otaCheckMsg);
    }
    else if (msg == "monitor") {
      if (workMode != MONITOR_MODE) {
        Serial.println("enter monitor mode");
        workMode = MONITOR_MODE;
      }
      sendMsg(monitorCheckMsg);
    }
    else if (msg != "") {
      Serial.println("unknown order:" + msg);
    }

    switch (workMode) {
      case MONITOR_MODE: {
          monitorRun();
          break;
        }
      case OTA_MODE: {
          otaRun();
          break;
        }
      default: {
          Serial.println("no task mode");
        }
    }
      delay(checkInterval);
  }
}

void sendMsg(const String msg) {
  String result = robotFlag + splitFlag + msg;
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

void monitorRun() {
  if (digitalRead(stopIO))
  {
    ++detectStopSignalTime;
    detectPauseSignalTime = 0;
    if ((currentRobotState != STOP && (detectStopSignalTime > MIN_DETECTED_SIGNAL_TIME)) || detectStopSignalTime > ( MIN_DETECTED_SIGNAL_TIME * 5)) {
      detectNormalTime = 0;
      currentRobotState = STOP;
      sendMsg(stopMsg);
      detectStopSignalTime = 0;
    }
  }
  else if (digitalRead(pauseIO))
  {
    ++detectPauseSignalTime;
    detectStopSignalTime = 0;
    if ((currentRobotState != PAUSE && (detectPauseSignalTime > MIN_DETECTED_SIGNAL_TIME)) || detectPauseSignalTime > (MIN_DETECTED_SIGNAL_TIME * 5)) {
      detectNormalTime = 0;
      currentRobotState = PAUSE;
      sendMsg(pauseMsg);
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
      currentRobotState = NORMAL;
      sendMsg(monitorCheckMsg);
      detectNormalTime = 0;
    }
  }
}

void otaRun() {
  ArduinoOTA.handle();
  detectNormalTime++;
  if (detectNormalTime > (MIN_DETECTED_SIGNAL_TIME * 5))
  {
    currentRobotState = NORMAL;
    sendMsg(otaCheckMsg);
    detectNormalTime = 0;
    detectPauseSignalTime = 0;
    detectStopSignalTime = 0;
  }
}

void otaIni() {
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
  ArduinoOTA.begin();
}
