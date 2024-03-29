"""
@Author Zach Wang
@Date 2021.9.27
@Version 1.2.1
"""
import json
from telnetlib import Telnet
from threading import Thread
import pandas as pd
import time
import recordingCSV
import classify
import firestore

# start=time.process_time();
class PyNeuro:
    """NeuroPy libraby, to get data from neurosky mindwave.
    Initialising: object1=PyNeuro() #windows
    After initialising , if required the callbacks must be set
    then using the start method the library will start fetching data from mindwave
    i.e. object1.start()
    similarly close method can be called to stop fetching the data
    i.e. object1.close()

    requirements:Telnet

    """
    # start=time.process_time();
    __attention = 0
    __meditation = 0
    __blinkStrength = 0
    __status = "NotConnected"

    __delta = 0
    __theta = 0
    __lowAlpha = 0
    __highAlpha = 0
    __lowBeta = 0
    __highBeta = 0
    __lowGamma = 0
    __highGamma = 0

    __attention_records = []
    __meditation_records = []
    __blinkStrength_records = []
    __lowAlpha_records= []
    __lowBeta_records= []
    __lowGamma_records= []
    __highAlpha_records= []
    __highBeta_records= []
    __highGamma_records= []
    __theta_records= []
    __delta_records= []

    __packetsReceived = 0
    __telnet = None

    __attention_callbacks = []
    __meditation_callbacks = []
    __blinkStrength__callbacks = []
    __delta__callbacks = []
    __theta__callbacks = []
    __status__callbacks = []
    __lowAlpha__callbacks = []
    __highAlpha__callbacks = []
    __lowBeta__callbacks = []
    __highBeta__callbacks = []
    __lowGamma__callbacks = []
    __highGamma__callbacks = []

    callBacksDictionary = {}  # keep a track of all callbacks

    def __init__(self):
        self.__parserThread = None
        self.__threadRun = False
        self.__connected = False

    def connect(self):
        """
        Connect the TCP socket via Telnet.

        """
        if self.__telnet is None:
            self.__telnet = Telnet('127.0.0.1', 13854)
            self.__telnet.write(b'{"enableRawOutput": true, "format": "Json"}');
            print("[PyNeuro] Connecting TCP Socket Host...")

    def disconnect(self):
        """
        Disconnect the TCP socket.
        """
        if self.__telnet is not None:
            self.__telnet.close()
            print("[PyNeuro] Disconnect TCP Socket.")

    def start(self):
        """
        Start Service.
        :return:
        """

        self.__parserThread = Thread(target=self.__packetParser, args=())
        self.__threadRun = True
        self.__parserThread.start()

    def close(self):
        """
        Close Service.
        :return:
        """
        self.__threadRun = False
        self.__parserThread.join()

    def __packetParser(self):
        try:
            while True:
                while len(self.__delta_records)!=30:

                    line = self.__telnet.read_until(b'\r');
                    if len(line) > 20:
                        try:
                            # timediff=time.process_time()-start;
                            # print(str(timediff))
                            # print(len(self.__theta_records))
                            raw_str = (str(line).rstrip("\\r'").lstrip("b'"))
                            data = json.loads(raw_str)
                            if "status" in data.keys():
                                if self.__status != data["status"]:
                                    self.__status = data["status"]
                                    if data["status"] == "scanning":
                                        print("[PyNeuro] Scanning device..")
                                    else:
                                        print("[PyNeuro] Connection lost, trying to reconnect..")
                            else:
                                if "eSense" in data.keys():
                                    print(data["eegPower"])
                                    # print(self.__attention_callbacks)
                                    # print(self.__attention_records)
                                    if data["eSense"]["attention"] + data["eSense"]["meditation"] == 0:
                                        if self.__status != "fitting":
                                            self.__status = "fitting"
                                            print("[PyNeuro] Fitting Device..")

                                    else:
                                        if self.__status != "connected":
                                            self.__status = "connected"
                                            print("[PyNeuro] Successfully Connected ..")
                                        print(len(self.__theta_records))    
                                        self.attention = data["eSense"]["attention"]
                                        self.meditation = data["eSense"]["meditation"]
                                        self.theta = data['eegPower']['theta']
                                        self.delta = data['eegPower']['delta']
                                        self.lowAlpha = data['eegPower']['lowAlpha']
                                        self.highAlpha = data['eegPower']['highAlpha']
                                        self.lowBeta = data['eegPower']['lowBeta']
                                        self.highBeta = data['eegPower']['highBeta']
                                        self.lowGamma = data['eegPower']['lowGamma']
                                        self.highGamma = data['eegPower']['highGamma']
                                        self.__theta_records.append(data['eegPower']['theta'])
                                        self.__delta_records.append(data['eegPower']['delta'])
                                        self.__highAlpha_records.append(data['eegPower']['highAlpha'])
                                        self.__lowAlpha_records.append(data['eegPower']['lowAlpha'])
                                        self.__lowBeta_records.append(data['eegPower']['lowBeta'])
                                        self.__highBeta_records.append(data['eegPower']['highBeta'])
                                        self.__lowGamma_records.append(data['eegPower']['lowGamma'])
                                        self.__highGamma_records.append(data['eegPower']['highGamma'])
                                        self.__attention_records.append(data["eSense"]["attention"])
                                        self.__meditation_records.append(data["eSense"]["meditation"])
                                elif "blinkStrength" in data.keys():
                                    self.blinkStrength = data["blinkStrength"]
                                    self.__blinkStrength_records.append(data["blinkStrength"])
                        except:
                            print()
          
                classification=classify.classfy(self.__lowAlpha_records,self.__highAlpha_records)
                recordingCSV.savetoCSV(self.__attention_records,self.__meditation_records,self.__delta_records,self.__theta_records,self.__lowAlpha_records,
                                    self.__highAlpha_records,self.__lowBeta_records,self.__highBeta_records,self.__lowGamma_records,self.__highGamma_records
                                    ,classification,"test")
                doc_ref = firestore.firestore_client.collection("classifications").document("1")
                doc_ref.set(
                    {
                        "classification": classification,
                    }
                )
                self.__attention_records = []
                self.__meditation_records = []
                self.__blinkStrength_records = []
                self.__lowAlpha_records= []
                self.__lowBeta_records= []
                self.__lowGamma_records= []
                self.__highAlpha_records= []
                self.__highBeta_records= []
                self.__highGamma_records= []
                self.__theta_records= []
                self.__delta_records= []
                

        except:
            print("[PyNeuro] Stop Packet Parser")

    
    def set_attention_callback(self, callback):
        """
        Set callback function of attention value
        :param callback: function(attention: int)
        """
        self.__attention_callbacks.append(callback)

    def set_meditation_callback(self, callback):
        """
        Set callback function of meditation value
        :param callback: function(meditation: int)
        """

        self.__meditation_callbacks.append(callback)

    def set_blinkStrength_callback(self, callback):
        """
        Set callback function of blinkStrength value
        :param callback: function(blinkStrength: int)
        """

        self.__blinkStrength__callbacks.append(callback)

    def set_delta_callback(self, callback):

        self.__delta__callbacks.append(callback)

    def set_theta_callback(self, callback):

        self.__theta__callbacks.append(callback)

    def set_lowAlpha_callback(self, callback):

        self.__lowAlpha__callbacks.append(callback)

    def set_highAlpha_callback(self, callback):

        self.__highAlpha__callbacks.append(callback)

    def set_lowBeta_callback(self, callback):

        self.__lowBeta__callbacks.append(callback)

    def set_highBeta_callback(self, callback):

        self.__highBeta__callbacks.append(callback)

    def set_lowGamma_callback(self, callback):

        self.__lowGamma__callbacks.append(callback)

    def set_highGamma_callback(self, callback):

        self.__highGamma__callbacks.append(callback)


    # attention
    @property
    def attention(self):
        """Get value for attention"""
        return self.__attention

    @attention.setter
    def attention(self, value):
        self.__attention = value
        # if callback has been set, execute the function
        if len(self.__attention_callbacks) != 0:
            for callback in self.__attention_callbacks:
                callback(self.__attention)

    # meditation
    @property
    def meditation(self):
        """Get value for meditation"""
        return self.__meditation

    @meditation.setter
    def meditation(self, value):
        self.__meditation = value
        # if callback has been set, execute the function
        if len(self.__meditation_callbacks) != 0:
            for callback in self.__meditation_callbacks:
                callback(self.__meditation)

    # blinkStrength
    @property
    def blinkStrength(self):
        """Get value for blinkStrength"""
        return self.__blinkStrength

    @blinkStrength.setter
    def blinkStrength(self, value):
        self.__blinkStrength = value
        # if callback has been set, execute the function
        for callback in self.__blinkStrength__callbacks:
            callback(self.__blinkStrength)

    @property
    def delta(self):
        """Get value for delta"""
        return self.__delta

    @delta.setter
    def delta(self, value):
        self.__delta = value
        # if callback has been set, execute the function
        for callback in self.__delta__callbacks:
            callback(self.__delta)

    @property
    def theta(self):
        """Get value for theta"""
        return self.__theta

    @theta.setter
    def theta(self, value):
        self.__theta = value
        # if callback has been set, execute the function
        for callback in self.__theta__callbacks:
            callback(self.__theta)

        # lowBeta
        # lowAlpha

    @property
    def lowAlpha(self):
        """Get value for lowAlpha"""
        return self.__lowAlpha

    @lowAlpha.setter
    def lowAlpha(self, value):
        self.__lowAlpha = value
        # if callback has been set, execute the function
        for callback in self.__lowAlpha__callbacks:
            callback(self.__lowAlpha)

    # highAlpha
    @property
    def highAlpha(self):
        """Get value for highAlpha"""
        return self.__highAlpha

    @highAlpha.setter
    def highAlpha(self, value):
        self.__highAlpha = value
        # if callback has been set, execute the function
        for callback in self.__highAlpha__callbacks:
            callback(self.__highAlpha)

    @property
    def lowBeta(self):
        """Get value for lowBeta"""
        return self.__lowBeta

    @lowBeta.setter
    def lowBeta(self, value):
        self.__lowBeta = value
        # if callback has been set, execute the function
        for callback in self.__lowBeta__callbacks:
            callback(self.__lowBeta)

    # highBeta
    @property
    def highBeta(self):
        """Get value for highBeta"""
        return self.__highBeta

    @highBeta.setter
    def highBeta(self, value):
        self.__highBeta = value
        # if callback has been set, execute the function
        for callback in self.__highBeta__callbacks:
            callback(self.__highBeta)

    # lowGamma
    @property
    def lowGamma(self):
        """Get value for lowGamma"""
        return self.__lowGamma

    @lowGamma.setter
    def lowGamma(self, value):
        self.__lowGamma = value
        # if callback has been set, execute the function
        for callback in self.__lowGamma__callbacks:
            callback(self.__lowGamma)

    # highGamma
    @property
    def highGamma(self):
        """Get value for midGamma"""
        return self.__highGamma

    @highGamma.setter
    def highGamma(self, value):
        self.__highGamma = value
        # if callback has been set, execute the function
        for callback in self.__highGamma__callbacks:
            callback(self.__highGamma)

    # status
    @property
    def status(self):
        """Get status"""
        return self.__status

    @status.setter
    def status(self, value):
        self.__status = value
        for callback in self.__status__callbacks:
            callback(self.__status)
