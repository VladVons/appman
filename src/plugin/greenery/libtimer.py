#!/usr/bin/python
# Created: 15.10.2017
# Vladimir Vons, VladVons@gmail.com


import json
import datetime
import time

class TCheckRange():
    def __init__(self, aObj = []):
        self.Obj = aObj

    def Clear(self):
        self.Obj = []

    def Add(self, aObj):
        self.Obj.append(aObj)

    def Validate(self):
        for Obj in self.Obj:
            if (not Obj.Check()):
                return False
        return True


class TBaseRange():
    def __init__(self):
        self.Range   = []
        self.Invert  = False
        self.Delim   = ''
        self.PadLen  = 2

    def Load(self, aValue):
        self.Invert = aValue.get('Invert', False)

        self.Range = []
        for Range in aValue.get('Range'):
            On  = self._Adjust(Range.get('On'))
            Off = self._Adjust(Range.get('Off'))

            if (not On):
                raise ValueError('On is empty')

            if (not Off):
                raise ValueError('Off is empty')

            self._Load(On, Off)

    def Check(self):
        raise NotImplementedError("Method not Implemented")


class TCycleRange(TBaseRange):
    def __init__(self):
        TBaseRange.__init__(self)
        self.Delim    = '-'
        self.Start    = int(time.time())

    def _Adjust(self, aValue):
        Items = aValue.split(self.Delim)
        if (Items[1] == 'S'):
            Result = int(Items[0])
        elif (Items[1] == 'M'):
            Result = int(Items[0]) * (60)
        elif (Items[1] == 'H'):
            Result = int(Items[0]) * (60 * 60)
        elif (Items[1] == 'D'):
            Result = int(Items[0]) * (60 * 60 * 24)
        elif (Items[1] == 'W'):
            Result = int(Items[0]) * (60 * 60 * 24 * 7)
        else:
            raise ValueError('Unknown value ' + Items[1])
        return Result

    def _Load(self, aOn, aOff):
        self.Range.append(aOn)
        self.Range.append(aOff)

    def Check(self):
        Duration = self.GetDuration()
        Elapsed  = int(time.time() - self.Start)
        Offset   = Elapsed % Duration
        Idx      = 0
        for i in range(0, len(self.Range), 2):
            if ( (Offset >= Idx) and (Offset < Idx + self.Range[i]) ):
                return True

            Idx += self.Range[i] + self.Range[i + 1]

        return False

    def GetDuration(self):
        Result = 0
        for Item in self.Range:
            Result += Item
        return Result


class TTimeRange(TBaseRange):
    def __init__(self, aRange = []):
        TBaseRange.__init__(self)
        self.Range = aRange  

    def _Adjust(self, aValue):
        # 7 to 07:00:00, 07:5 to 07:05:00, etc
        Result = self.Mask

        if (self.Delim == ''):
            Items = [aValue]
        else:
            Items = aValue.split(self.Delim)

        Idx = 0
        for Item in Items:
            Replace =  Item.zfill(self.PadLen)
            Result = Result[:Idx] + Replace + Result[Idx + len(Replace):]
            Idx += self.PadLen + len(self.Delim)

        return Result

    def _Load(self, aOn, aOff):
        if (aOn >= aOff):
            raise ValueError('(Off %s) must be greater then (On %s)' % (aOff, aOn))

        self.Range.append(aOn)
        self.Range.append(aOff)

    def Check(self):
        Now = datetime.datetime.now().strftime(self.Format)

        #print(self.Range)
        for i in range(0, len(self.Range), 2):
            if ( (Now >= self.Range[i]) and (Now < self.Range[i + 1]) ):
                return (True != self.Invert)
        return (False != self.Invert)


#Data = '{"Timer_Day":{ "Range":[ { "On":"7", "Off": "09:19:30"}, { "On":"21:00:03", "Off": "22:00"}, { "On":"23:45", "Off": "23:46"} ]}}'
class TDayRange(TTimeRange):
    def __init__(self):
        TTimeRange.__init__(self)
        self.Delim  = ':'
        self.Mask   = '00:00:00'
        self.Format = '%H:%M:%S'

#Data = '{"Timer_Week":{ "Range":[ { "On":"0", "Off": "2"}] }}'
class TWeekRange(TTimeRange):
    # 0 is Sunday 
    def __init__(self):
        TTimeRange.__init__(self)
        self.Mask   = '0'
        self.Format = '%w'
        self.PadLen = 1

#Data = '{"Timer_Month":{ "Range":[ { "On":"2", "Off": "03"}, { "On":"10", "Off": "11"}] }}'
class TMonthRange(TTimeRange):
    def __init__(self):
        TTimeRange.__init__(self)
        self.Mask   = '00'
        self.Format = '%m'

#Data = '{"Timer_Year":{ "Range":[ { "On":"8", "Off": "08.12"}, { "On":"10.16", "Off": "10.17"}] }}'
class TYearRange(TTimeRange):
    def __init__(self):
        TTimeRange.__init__(self)
        self.Delim  = '.'
        self.Mask   = '00.01'
        self.Format = '%m.%d'
