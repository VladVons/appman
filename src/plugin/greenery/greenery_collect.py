# https://collectd.org/documentation/manpages/collectd-python.5.shtml#examples

try: 
    import collectd
except: pass

import json
import os
#
from Manager import *


class TParam():
    def LoadCollectd(self, aItems):
        for Item in aItems:
            Key   = Item.key
            Value = Item.values[0]
            setattr(self, Key, Value)
            print('CallBack_Config. Key %s, Value %s' % (Key, Value))

    def Load(self, aItems):
        for Item in aItems:
            setattr(self, Item, aItems.get(Item))


class TCollect():
    def __init__(self):
        try:
            collectd.register_config(self.CallBack_Config)
            collectd.register_read(self.CallBack_Read)
        except: pass
        print('--- __init__')

        self.Param = TParam()

    def CallBack_Config(self, aConfig):
        print('--- CallBack_Config', self.Param)
        self.Param.LoadCollectd(aConfig.children)

    def CallBack_Read(self):
        print('--- CallBack_Read')

        Tags = self.FileLoad()
        print('---', Tags)
        for Tag in Tags:
            Keys = Tags.get(Tag)
            for Key in Keys:
                Value = Keys.get(Key)
                print('Tag', Tag, Key, Value)

                #https://github.com/collectd/collectd/blob/master/src/types.db
                #val = collectd.Values(type='brightnes')
                #val = collectd.Values(type='humidity')
                val = collectd.Values(type='gauge')
                val.plugin = Tag
                val.values = [Value]
                val.type_instance = Key
                val.dispatch()

    def FileLoad(self):
        Result = None 
        if (os.path.exists(self.Param.FileTmp)):
            with open(self.Param.FileTmp, 'rb') as File:
                Result = json.load(File)
        return Result

Collect = TCollect()
