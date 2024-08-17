/*
MyModWorldTime
.net class library 
.NET Framework 4.7.2
.net class library references

C:\Program Files (x86)\Steam\steamapps\common\7 Days To Die\7DaysToDie_Data\Managed

"Assembly-CSharp.dll" "UnityEngine.dll" "UnityEngine.CoreModule.dll" "mscorlib.dll" "System.dll" "System.Core.dll"


C:\Users\Windows10\source\repos\ClassLibrary2\ClassLibrary2\bin\Debug\.dll
*/


/*
<?xml version="1.0" encoding="UTF-8"?>
<xml>
    <Name value="MyModWorldTime"/>
    <DisplayName value="MyModWorldTime"/>
    <Version value="1.0"/>
    <Description value="Polling system for receiving World time."/>
    <Author value="BoQsc"/>
    <Website value="https://www.nexusmods.com/"/>
</xml>
-*/


using System;
using System.Collections.Generic;
using UnityEngine;

public class TimePollingModlet : IModApi
{
    private const float PollingIntervalSeconds = 5f; // Poll every 5 seconds
    private float _nextPollTime;

    public void InitMod(Mod _modInstance)
    {
        ModEvents.GameUpdate.RegisterHandler(GameUpdateHandler);
        Debug.Log("Time Polling Modlet initialized");
    }

    private void GameUpdateHandler()
    {
        if (Time.time >= _nextPollTime)
        {
            PollGameTime();
            _nextPollTime = Time.time + PollingIntervalSeconds;
        }
    }

    private void PollGameTime()
    {
        if (GameManager.Instance?.World == null)
        {
            return;
        }

        ulong worldTime = GameManager.Instance.World.worldTime;
        int days = GameUtils.WorldTimeToDays(worldTime);
        float totalHours = GameUtils.WorldTimeToHours(worldTime);
        float totalMinutes = GameUtils.WorldTimeToMinutes(worldTime);

        int hours = (int)Math.Floor(totalHours);

        int minutes = (int)Math.Floor(totalMinutes);

        Debug.Log($"Current game time: Day {days}, {hours:D2}:{minutes:D2}");

        // Add your custom logic here based on the game time
        // For example:
        if (hours >= 22 || hours < 4)
        {
            Debug.Log("It's nighttime!");
        }
        else
        {
            Debug.Log("It's daytime!");
        }
    }
}