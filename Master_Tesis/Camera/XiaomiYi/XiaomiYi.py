#!/usr/bin/python3
import json
import socket

from time import sleep, perf_counter

REST = 3


class NotConnected(Exception):
    def __init__(self, error):
        self.error = error


class XiaomiYi:

    def __init__(self, ip="192.168.42.1", port=7878, timeout=5):
        self._ip = ip
        self._port = port
        self._timeout = timeout

        self.__token = None
        self.__control = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __repr__(self):
        return "XiaomiYi('{}', {}, {})".format(self._ip, self._port, self._timeout)

    def send(self, data, connect=False):
        """
        There needs to be little delay after every command,
        except while getting token, 
        otherwise Yi will ignore following commands.
        """
        if self.__token or connect:
            self.__control.send(bytes(json.dumps(data), 'UTF-8'))
            if not connect:
                sleep(REST)
        else:
            raise NotConnected("Make connection with object.connect() first.")

    def token(self):
        # print("Your token is: ", __token)
        return self.__token

    def connect(self):
        self.__control.settimeout(self._timeout)
        self.__control.connect((self._ip, self._port))

        self.send({"msg_id": 257, "token": 0}, True)
        data = self.__control.recv(512).decode("utf-8")
        if not "rval" in data:
            data = self.__control.recv(512).decode("utf-8")
        self.__token = json.loads(data)["param"]

    def take_photo(self):
        self.send({"msg_id": 769, "token": self.__token})

    def start_video(self, duration=False):
        self.send({"msg_id": 513, "token": self.__token})
        if duration:
            sleep(duration)
            self.send({"msg_id": 514, "token": self.__token})

    def stop_video(self):
        self.send({"msg_id": 514, "token": self.__token})

    def seq_photos(self, every, until=False):
        # "every" needs to be at least "REST" seconds.
        if every < REST:
            every = REST

        begin = perf_counter()
        while True:
            self.take_photo()
            if until and (until < perf_counter() - begin):
                break
            sleep(every - REST)

    def stream(self, until=False):
        begin = perf_counter()

        self.send({"msg_id": 259, "token": self.__token, "param": "none_force"})
        while True:
            if until and (until < perf_counter() - begin):
                break
            sleep(REST)

        return json(self.__control.recv(512).decode("utf-8"))

    def close(self):
        self.__control.close()
