
Data = '{"Timer_Day":{ "Range":[ { "On":"7", "Off": "14:39:30"}, { "On":"21:00:03", "Off": "22:00"}, { "On":"23:45", "Off": "23:46"} ]}}'
#Data = '{"Timer_Day":{ "Range":[ { "On":"7", "Off": "07:19:30"}, { "On":"21:00:03", "Off": "22:00"}, { "On":"23:45", "Off": "23:46"} ], "Invert" : "True"}}'
root = json.loads(Data)
DayRange = TDayRange()
DayRange.Load(root.get('Timer_Day'))
print(DayRange.Check())

Data = '{"Timer_Week":{ "Range":[ { "On":"0", "Off": "2"}] }}'
root = json.loads(Data)
WeekRange = TWeekRange()
WeekRange.Load(root.get('Timer_Week'))
print(WeekRange.Check())

Data = '{"Timer_Month":{ "Range":[ { "On":"2", "Off": "03"}, { "On":"10", "Off": "11"}] }}'
root = json.loads(Data)
MonthRange = TMonthRange()
MonthRange.Load(root.get('Timer_Month'))
print(MonthRange.Check())

Data = '{"Timer_Year":{ "Range":[ { "On":"8", "Off": "08.12"}, { "On":"10.16", "Off": "10.17"}] }}'
root = json.loads(Data)
YearRange = TYearRange()
YearRange.Load(root.get('Timer_Year'))
print(YearRange.Check())

Data = '{"Timer_Cycle":{ "Range":[ { "On":"5-S", "Off": "2-S"}, { "On":"3-S", "Off": "3-S"}, { "On":"2-S", "Off": "2-S"} ] }}'
root = json.loads(Data)
CycleRange = TCycleRange()
CycleRange.Load(root.get('Timer_Cycle'))
print(CycleRange.Check())


CheckRange = TCheckRange([DayRange, WeekRange, MonthRange, YearRange, CycleRange])
while True: 
    print('Validate', CheckRange.Validate())
    time.sleep(1)
