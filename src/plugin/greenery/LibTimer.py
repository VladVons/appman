# Created: 15.10.2017
# Vladimir Vons, VladVons@gmail.com


import datetime
#
from LibCommon import TControl, _Required


__all__ = ['TTimeRangeCycle', 'TTimeRangeDay', 'TTimeRangeWeek', 'TTimeRangeMonth', 'TTimeRangeYear', "TTimeCount"]


class TTimeUtil():
    @staticmethod
    def CharToSec(aChar, aValue):
        if (aChar == 'S'):
            Ratio = 1
        elif (aChar == 'M'):
            Ratio = 60
        elif (aChar == 'H'):
            Ratio = 60 * 60
        elif (aChar == 'D'):
            Ratio = 60 * 60 * 24
        elif (aChar == 'W'):
            Ratio = 60 * 60 * 24 * 7
        elif (aChar == 'm'):
            Ratio = 60 * 60 * 24 * 30
        else:
            raise ValueError('Unknown char ' + aChar)
        return aValue * Ratio


class TBaseRange(TControl):
    def __init__(self, aParent):
        super().__init__(aParent)
        self.Delim   = ''
        self.PadLen  = 2

    def LoadParam(self, aParam):
        self.Range = []
        self.Clear()

        Pattern = {'Ranges':[]}
        self.Param.Load(aParam, Pattern)

        for Range in self.Param.Ranges:
            On  = self._Adjust(Range.get('On'))
            Off = self._Adjust(Range.get('Off'))

            if (not On):
                raise ValueError('On is empty')

            if (not Off):
                raise ValueError('Off is empty')

            self._Load(On, Off)

    def _Get(self):
        return self.Param.State


class TTimeRangeCycle(TBaseRange):
    def __init__(self, aParent):
        super().__init__(aParent)
        self.Delim    = '-'

    def _Adjust(self, aValue):
        Items = aValue.split(self.Delim)
        return TTimeUtil.CharToSec(Items[1], int(Items[0]))

    def _Load(self, aOn, aOff):
        self.Range.append(aOn)
        self.Range.append(aOff)

    def _Check(self, aValue):
        Duration = self.GetDuration()
        Offset   = self.Uptime() % Duration
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
            raise ValueError('(On %s) is greater then (Off %s)' % (aOn, aOff))

        self.Range.append(aOn)
        self.Range.append(aOff)

    def _Check(self, aValue):
        Now = datetime.datetime.now().strftime(self.Format)

        for i in range(0, len(self.Range), 2):
            if ( (Now >= self.Range[i]) and (Now < self.Range[i + 1]) ):
                return True

        return False


#Data = '{"Timer_Day":{ "Range":[ { "On":"7", "Off": "09:19:30"}, { "On":"21:00:03", "Off": "22:00"}, { "On":"23:45", "Off": "23:46"} ]}}'
class TTimeRangeDay(TTimeRange):
    def __init__(self, aParent):
        super().__init__(aParent)
        self.Delim  = ':'
        self.Mask   = '00:00:00'
        self.Format = '%H:%M:%S'

#Data = '{"Timer_Week":{ "Range":[ { "On":"0", "Off": "2"}] }}'
class TTimeRangeWeek(TTimeRange):
    # 0 is Sunday 
    def __init__(self, aParent):
        super().__init__(aParent)
        self.Mask   = '0'
        self.Format = '%w'
        self.PadLen = 1

#Data = '{"Timer_Month":{ "Range":[ { "On":"2", "Off": "03"}, { "On":"10", "Off": "11"}] }}'
class TTimeRangeMonth(TTimeRange):
    def __init__(self, aParent):
        super().__init__(aParent)
        self.Mask   = '00'
        self.Format = '%m'

#Data = '{"Timer_Year":{ "Range":[ { "On":"8", "Off": "08.12"}, { "On":"10.16", "Off": "10.17"}] }}'
class TTimeRangeYear(TTimeRange):
    def __init__(self, aParent):
        super().__init__(aParent)
        self.Delim  = '.'
        self.Mask   = '00.01'
        self.Format = '%m.%d'


class TTimeCount(TControl):
    def LoadParam(self, aParam):
        Pattern = {'Count':_Required}
        self.Param.Load(aParam, Pattern)

    def Get(self):
        return self.Uptime() - self.Count

    def _Check(self, aValue):
        return self.Get() > 0
