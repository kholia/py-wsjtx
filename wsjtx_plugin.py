#!/usr/bin/env python3
#pylint: disable-msg=missing-function-docstring,line-too-long,invalid-name,too-many-instance-attributes,consider-using-f-string

import sys
import time
import socket
import struct
import datetime

class WSJTX_Packet():
    """
    Header class for all WSJT received packets. This class handles the header
    and will create class for handling the packet depending on the packet type
    in the header.
    """
    def __init__(self, pkt, idx):
        self.index = idx  # Keeps track of where we are in the packet parsing
        self.packet = pkt
        self.MagicNumber = 0
        self.SchemaVersion = 0
        self.PacketType = 0
        self.ClientID = ""

    # Methods to extract the different types of data in the packet.  These are shared with all
    # the other packet classes.
    def readutf8(self):
        strLength = self.getInt32()
        # BUG what happens if string length is zero?
        if strLength > 0:
            stringRead = struct.unpack(">"+str(strLength)+"s",
                    self.packet[self.index:strLength+self.index])
            self.index += strLength
            return stringRead[0].decode('utf-8')
        return ""

    def getDateTime(self):
        TimeOffset = 0
        DateOff = self.getLongLong()
        TimeOff = self.getuInt32()
        TimeSpec = self.getByte()
        if TimeSpec == 2:
            TimeOffset = self.getInt32()
        return (DateOff, TimeOff, TimeSpec, TimeOffset)

    def getByte(self):
        data = struct.unpack(">B", self.packet[self.index:self.index+1])
        self.index += 1
        return data[0]

    def getBool(self):
        data = struct.unpack(">?", self.packet[self.index:self.index+1])
        self.index += 1
        return data[0]

    def getInt32(self):
        data = struct.unpack(">i", self.packet[self.index:self.index+4])
        self.index += 4
        return data[0]

    def getuInt32(self):
        data = struct.unpack(">I", self.packet[self.index:self.index+4])
        self.index += 4
        return data[0]

    def getLongLong(self):
        data = struct.unpack(">Q", self.packet[self.index:self.index+8])
        self.index += 8
        return data[0]

    def getDouble(self):
        data = struct.unpack(">d", self.packet[self.index:self.index+8])
        self.index += 8
        return data[0]

    def Decode(self):
        # print(self.packet, len(self.packet))
        self.MagicNumber = self.getuInt32()
        self.SchemaVersion = self.getuInt32()
        self.PacketType = self.getuInt32()
        self.ClientID = self.readutf8()

class WSJTX_Status(WSJTX_Packet):
    """
    Packet Type 1 Status:
    WSJT-X  sends this  status message  when various  internal state changes to
    allow the server to  track the relevant state of each client without the
    need for  polling commands. The current state changes that generate status
    messages are:

    - Application start up,
    - "Enable Tx" button status changes,
    - Dial frequency changes,
    - Changes to the "DX Call" field,
    - Operating mode, sub-mode or fast mode changes,
    - Transmit mode changed (in dual JT9+JT65 mode),
    - Changes to the "Rpt" spinner,
    - After an old decodes replay sequence (see Replay below),
    - When switching between Tx and Rx mode,
    - At the start and end of decoding,
    - When the Rx DF changes,
    - When the Tx DF changes,
    - When the DE call or grid changes (currently when settings are exited),
    - When the DX call or grid changes,
    - When the Tx watchdog is set or reset.
    """
    def __init__(self, pkt, idx):
        WSJTX_Packet.__init__(self, pkt, idx)
        self.Frequency = 0
        self.Mode = ""
        self.DXCall = ""
        self.Report = ""
        self.TxMode = ""
        self.TxEnabled = False
        self.Transmitting = False
        self.Decoding = False
        self.RxDF = 0
        self.TxDF = 0
        self.DECall = ""
        self.DEgrid = ""
        self.DXgrid = ""
        self.TxWatchdog = False
        self.Submode = ""
        self.Fastmode = False
        self.SpecialOpMode = False
        self.FrequencyTolerance = 0
        self.TrPeriod = 0
        self.ConfigurationName = ""
        self.TxMessage = ""

    def Decode(self):
        """
        https://github.com/jtdx-project/jtdx/blob/master/MessageServer.cpp#L221

        Note: JTDX and jtdx_improved do NOT send 'TxMessage', hence they are NOT compatible!

        https://sourceforge.net/p/wsjt/wsjtx/ci/master/tree/UDPExamples/MessageServer.cpp#l253
        """
        self.Frequency = self.getLongLong()
        self.Mode = self.readutf8()
        self.DXCall = self.readutf8()
        self.Report = self.readutf8()
        self.TxMode = self.readutf8()
        self.TxEnabled = self.getBool()
        self.Transmitting = self.getBool()
        self.Decoding = self.getBool()
        self.RxDF = self.getuInt32()
        self.TxDF = self.getuInt32()
        self.DECall = self.readutf8()
        self.DEgrid = self.readutf8()
        self.DXgrid = self.readutf8()
        self.TxWatchdog = self.getBool()
        self.Submode = self.readutf8()
        self.Fastmode = self.getBool()
        self.SpecialOpMode = self.getBool()
        self.FrequencyTolerance = self.getuInt32()
        self.TrPeriod = self.getuInt32()
        self.ConfigurationName = self.readutf8()
        self.TxMessage = self.readutf8()
        self.ItoneData = self._readItoneString()

    def _readItoneString(self):
        """
        Read the itone data string (separate field after TxMessage).
        Format: "3 1 4 0 6 5 2 0 0..." (space-separated tone indices)
        Different modes have different numbers of tones.
        """
        itones = []
        try:
            # Read the itone string as a separate UTF-8 field
            itone_str = self.readutf8()
            if itone_str:
                # Parse space-separated tone indices
                parts = itone_str.strip().split()
                # Filter valid tone values (0-255 covers all modes)
                itones = [int(p) for p in parts if p.isdigit() and 0 <= int(p) <= 255]
                return itones
        except Exception:
            pass
        return []


# Connection for WSJT-X
UDP_IP = "127.0.0.1"
UDP_PORT = 2237
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))


def main():
    try:
        while True:
            packet_data, _ = sock.recvfrom(1024)
            new_packet = WSJTX_Packet(packet_data, 0)
            new_packet.Decode()
            if new_packet.PacketType == 1:
                StatusPacket = WSJTX_Status(packet_data, new_packet.index)
                StatusPacket.Decode()

                # Print itone data if available
                if StatusPacket.ItoneData:
                    print("> Itone data ({0} tones, {1}): {2}".format(
                        len(StatusPacket.ItoneData),
                        StatusPacket.Mode,
                        ' '.join(str(t) for t in StatusPacket.ItoneData)))

                # Check TX frequency and update transceiver
                new_offset = StatusPacket.TxDF
                new_mode = StatusPacket.TxMode.strip()
                new_frequency = StatusPacket.Frequency

                # Check if TX is enabled
                if StatusPacket.Transmitting == 1:
                    # Check time, avoid transmitting out of the time slot
                    utc_time = datetime.datetime.now(datetime.UTC)
                    message = StatusPacket.TxMessage
                    message = message.replace('<', '')
                    message = message.replace('>', '')
                    print(message.strip())
                    print("> Time: {0}:{1}:{2}".format(utc_time.hour, utc_time.minute, utc_time.second))
    finally:
        sock.close()

if __name__ == "__main__":
    main()
