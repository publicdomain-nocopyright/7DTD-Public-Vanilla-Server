using System;
using System.Collections.Generic;
using UnityEngine;
using System.IO;
using Newtonsoft.Json;
using System.Reflection;

public class TimePollingModlet : IModApi
{
    private const float PollingIntervalSeconds = 1f; // Poll every 1 second
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

        int hours = (int)Math.Floor(totalHours % 24);
        int minutes = (int)Math.Floor(totalMinutes % 60);

        string timeString = $"Current game time: Day {days}, {hours:D2}:{minutes:D2}";

        // Create a dictionary to hold the time data
        var timeData = new Dictionary<string, string>
        {
            { "currentGameTime", timeString }
        };

        // Convert the dictionary to JSON
        string json = JsonConvert.SerializeObject(timeData, Formatting.Indented);

        // Get the directory of the current DLL
        string dllPath = Assembly.GetExecutingAssembly().Location;
        string dllDirectory = Path.GetDirectoryName(dllPath);

        // Write the JSON to a file in the DLL directory
        string filePath = Path.Combine(dllDirectory, "current_game_time.json");
        File.WriteAllText(filePath, json);

        //Debug.Log($"Game time saved to {filePath}");
    }
}