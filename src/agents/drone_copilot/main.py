# This file is part of the Drone Copilot project.
# We should be able to give copilot instructions to the drone and it will execute them,
# or deny that request if it is not safe or possible.
import os
import pydantic
import numpy as np
import json
import pandas as pd
import time
import base64
import jinja2
from dotenv import load_dotenv
from IPython.display import display
from typing import List, Dict, Any, Generator
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

MODEL: str = os.environ.get("OPENAI_API_MODEL")

# Initialize OpenAI client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Utility functions
def get_chat_completion(
    messages: List[Dict[str, str]],
    model: str = MODEL,
    max_tokens: int = 500,
    temperature: float = 0.0,
    stop = None,
    tools = None,
    seed: int = 42,
    functions = None,
    tool_choice = None,
) -> tuple[str, dict[str, Any]]:
    """
    Get a chat completion from the OpenAI API.

    Args:
        messages (list[dict[str, str]]): List of messages to send to the model.
        model (str): The model to use for the completion.
        max_tokens (int): Maximum number of tokens to generate.
        temperature (float): Sampling temperature.
        stop (list[str]): List of stop sequences.
        tools (list[dict[str, Any]]): List of tools available for function calling.
        seed (int): Random seed for reproducibility.
        functions (list[dict[str, Any]]): List of function definitions for structured function calling.
        tool_choice: Tool choice strategy.

    Returns:
        tuple[str, dict[str, Any]]: The generated text and usage information.
    """
    params = {
        "model": model,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "stop": stop,
        "tools": tools,
        "seed": seed,
        "tool_choice": tool_choice,
    }

    if functions:
        params["functions"] = functions

    completion = client.chat.completions.create(**params)
    return completion.choices[0].message, completion.usage


def eval(model: str, 
    system_prompt: str, 
    functions_list: List[Dict[str, Any]], 
    prompts_to_expected_tool_name: Dict[str, Dict[str, Any]]):
    """
    Evaluate the performance of a model in selecting the correct function based on given prompts.

    Args:
        model (str): The model name to be evaluated.
        system_prompt (str): The system prompt to guide the model's behavior.
        functions_list (List[Dict[str, Any]]): List of function definitions that the model can call.
        prompts_to_expected_tool_name (Dict[str, Dict[str, Any]]): A dictionary mapping prompts to expected function calls.
    Returns:
        None
    """

    prompts_to_actual = []
    latencies = []
    tokens_used = []

    for prompt, expected_function in prompts_to_expected_tool_name.items():
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ]

        start_time = time.time()
        completion, usage = get_chat_completion(
            model=model,
            messages=messages,
            seed=42,
            tools=functions_list,
            #functions=functions_list,
            temperature=0.0,
            tool_choice="required",
        )
        end_time = time.time()

        latency = (end_time - start_time) * 1000  # Convert to milliseconds
        latencies.append(latency)

        prompts_to_actual.append({
            prompt: completion.tool_calls[0].function.name if completion.tool_calls else None,
        })

        # calculate tokens used
        tokens_used.append(usage.total_tokens)
    
    # Calculate the total number of prompts
    total_prompts = len(prompts_to_expected_tool_name)

    # Calculate the number of matches
    matches = sum(
        1
        for results in prompts_to_actual
        if list(results.values())[0] == prompts_to_expected_tool_name[list(results.keys())[0]]
    )
    match_percentage = (matches / total_prompts) * 100

    # calculate average latency
    average_latency = sum(latencies) / total_prompts if total_prompts > 0 else 0
    # calculate average tokens used
    average_tokens_used = sum(tokens_used) / total_prompts if total_prompts > 0 else 0

    # create dataframe for results
    results_df = pd.DataFrame(columns=["Prompt", "Expected Func", "Actual Func", "Match", "Latency (ms)", "Tokens Used"])

    results_list = []
    for results in prompts_to_actual:
        prompt = list(results.keys())[0]
        actual_function = list(results.values())[0]
        expected_function = prompts_to_expected_tool_name[prompt]
        match = actual_function == expected_function
        latency = latencies.pop(0) if latencies else 0
        tokens_used_value = tokens_used.pop(0) if tokens_used else 0

        results_list.append({
            "Prompt": prompt,
            "Actual Func": actual_function,
            "Expected Func": expected_function,
            "Match": "Yes" if match else "No",
            "Latency (ms)": latency,
            "Tokens Used": tokens_used_value,
        })

    results_df = pd.DataFrame(results_list)

    def style_rows(row):
        """
        Style the rows of the DataFrame based on matches.
        """
        matches = row["Match"]
        background_color = "red" if matches == "No" else "lightcoral"
        return ["background-color: {}; color: black".format(background_color)] * len(row)

    styled_results_df = results_df.style.apply(style_rows, axis=1)

    # display the dataframe as a table
    display(styled_results_df)

    print(f"Number of matches: {matches} out of {total_prompts} ({match_percentage:.2f}%)")
    print(f"Average latency per request: {average_latency:.2f} ms")
    print(f"Average tokens used per request: {average_tokens_used:.2f}")


# System prompt
DRONE_SYSTEM_PROMPT = """You are an intelligent AI that controls a drone. Given a command or request from the user,
call one of your functions to complete the request. If the request cannot be completed by your available functions, call the reject_request function.
If the request is ambiguous or unclear, reject the request."""

# structured function definitions
# 0. takeoff_drone: Instruct the drone to take off and hover at a specified altitude.
# 1. land_drone: Instruct the drone to land safely at its current position or a specified landing point.
# 2 control_drone_movement: Instruct the drone's movement in a specific direction.
# 3. capture_image: Capture an image or video using the drone's camera.
# 4. control_gimbal: Adjust the drone's gimbal for camera stabilization and direction.
# 5. set_flight_mode: Set the flight mode of the drone.
# 6. set_drone_lighting: Control the drone's lighting for visibility and signaling.
# 7. set_return_to_home: Set the return to home location for the drone.
# 8. set_battery_saver_mode: Toggle battery saver mode.
# 9. set_obstacle_avoidance: Configure obstacle avoidance settings.
# 10. set_flight_path: Set a predefined flight path for the drone.
# 11. set_follow_me_mode: Enable or disable 'follow me' mode.
# 12. calibrate_sensors: Calibrate the drone's sensors for accurate operation.
# 13. update_firmware: Update the drone's firmware to the latest version.
# 14. set_autopilot: Enable or disable autopilot mode.
# 15. set_emergency_landing: Instruct the drone to perform an emergency landing.
# 16. configure_led_display: Configure the LED display on the drone for notifications or messages.
# 17. set_drone_speed: Set the speed of the drone.
# 18. set_home_location: Set the home location for the drone.
# 19. reject_request: Reject the request if it is not safe or possible.
DRONE_FUNCTIONS_LIST = [
    {
        "type": "function",
        "function": {
            "name": "takeoff_drone",
            "description": "Instruct the drone to take off and hover at a specified altitude.",
            "parameters": {
                "type": "object",
                "properties": {
                    "altitude": {
                        "type": "integer",
                        "description": "The altitude in meters to which the drone should ascend.",
                    },
                },
                "required": ["altitude"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "land_drone",
            "description": "Instruct the drone to land safely at its current position or a specified landing point.",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "enum": ["current", "home_base", "custom"],
                        "description": "Specifies the landing location for the drone.",
                    },
                    "coordinates": {
                        "type": "object",
                        "description": "GPS coordinates for custom landing location. Required if location is 'custom'.",
                    },
                },
                "required": ["location"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "control_drone_movement",
            "description": "Instruct the drone's movement in a specific direction.",
            "parameters": {
                "type": "object",
                "properties": {
                    "direction": {
                        "type": "string",
                        "enum": ["forward", "backward", "left", "right", "up", "down"],
                        "description": "Specifies the direction in which the drone should move.",
                    },
                    "distance": {
                        "type": "integer",
                        "description": "Distance in meters the drone should travel in the specified direction.",
                    },
                },
                "required": ["direction", "distance"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "capture_image",
            "description": "Capture an images or videos using the drone's camera.",
            "parameters": {
                "type": "object",
                "properties": {
                    "mode": {
                        "type": "string",
                        "enum": ["photo", "video", "panorama"],
                        "description": "Specifies camera mode to capture content.",
                    },
                    "resolution": {
                        "type": "string",
                        "enum": ["low", "medium", "high"],
                        "description": "The resolution of the captured image.",
                    },
                    "duration": {
                        "type": "integer",
                        "description": "Duration in seconds for video capture. Required if mode is 'video'.",
                    },
                },
                "required": ["resolution", "mode"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "control_gimbal",
            "description": "Adjust the drone's gimbal for camera stabilization and direction.",
            "parameters": {
                "type": "object",
                "properties": {
                    "pitch": {
                        "type": "integer",
                        "description": "Pitch angle in degrees to adjust the gimbal.",
                    },
                    "roll": {
                        "type": "integer",
                        "description": "Roll angle in degrees to adjust the gimbal.",
                    },
                    "yaw": {
                        "type": "integer",
                        "description": "Yaw angle in degrees to adjust the gimbal.",
                    },
                    "tilt": {
                        "type": "integer",
                        "description": "Tilt angle in degrees to adjust the gimbal.",
                    },
                    "pan": {
                        "type": "integer",
                        "description": "Pan angle in degrees to adjust the gimbal.",
                    },
                },
                "required": ["pitch", "roll", "yaw", "tilt", "pan"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "set_flight_mode",
            "description": "Set the flight mode of the drone.",
            "parameters": {
                "type": "object",
                "properties": {
                    "mode": {
                        "type": "string",
                        "enum": ["manual", "autonomous", "follow_me", "waypoint_navigation"],
                        "description": "Specifies the flight mode to set for the drone.",
                    },
                },
                "required": ["mode"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "set_drone_lighting",
            "description": "Control the drone's lighting for visibility and signaling.",
            "parameters": {
                "type": "object",
                "properties": {
                    "mode": {
                        "type": "string",
                        "enum": ["off", "on", "flashing", "strobe"],
                        "description": "Specifies the lighting mode for the drone.",
                    },
                    "color": {
                        "type": "string",
                        "description": "Color of the drone's lights. Optional, defaults to white.",
                    },
                },
                "required": ["mode", "color"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "set_return_to_home",
            "description": "Set the return to home location for the drone.",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "enum": ["current", "home_base", "custom"],
                        "description": "Specifies the return to home location.",
                    },
                    "coordinates": {
                        "type": "object",
                        "description": "GPS coordinates for custom return to home location. Required if location is 'custom'.",
                    },
                },
                "required": ["location", "coordinates"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "set_battery_saver_mode",
            "description": "Toggle battery saver mode.",
            "parameters": {
                "type": "object",
                "properties": {
                    "status": {
                        "type": "string",
                        "enum": ["enable", "disable"],
                        "description": "Enable or disable battery saver mode.",
                    },
                },
                "required": ["status"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "set_obstacle_avoidance",
            "description": "Configure obstacle avoidance settings.",
            "parameters": {
                "type": "object",
                "properties": {
                    "mode": {
                        "type": "string",
                        "enum": ["on", "off", "auto"],
                        "description": "Set the obstacle avoidance mode.",
                    },
                },
                "required": ["mode"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "set_flight_path",
            "description": "Set a predefined flight path for the drone.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "latitude": {"type": "number"},
                                "longitude": {"type": "number"},
                                "altitude": {"type": "integer"},
                            },
                            "required": ["latitude", "longitude", "altitude"],
                        },
                        "description": "List of GPS coordinates defining the flight path.",
                    },
                },
                "required": ["path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "set_follow_me_mode",
            "description": "Enable or disable 'follow me' mode.",
            "parameters": {
                "type": "object",
                "properties": {
                    "status": {
                        "type": "string",
                        "enum": ["enable", "disable"],
                        "description": "Enable or disable the 'follow me' mode.",
                    },
                },
                "required": ["status"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "calibrate_sensors",
            "description": "Calibrate the drone's sensors for accurate operation.",
            "parameters": {
                "type": "object",
                "properties": {
                    "sensors": {
                        "type": "array",
                        "items": {
                            "type": "string",
                            "enum": ["gyroscope", "accelerometer", "compass", "barometer"],
                        },
                        "description": "List of sensors to calibrate.",
                    },
                },
                "required": ["sensors"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "update_firmware",
            "description": "Update the drone's firmware to the latest version.",
            "parameters": {
                "type": "object",
                "properties": {
                    "version": {
                        "type": "string",
                        "description": "The version of the firmware to update to. If not specified, update to the latest version.",
                    },
                },
                "required": ["version"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "set_autopilot",
            "description": "Enable or disable autopilot mode.",
            "parameters": {
                "type": "object",
                "properties": {
                    "status": {
                        "type": "string",
                        "enum": ["enable", "disable"],
                        "description": "Enable or disable autopilot mode.",
                    },
                },
                "required": ["status"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "set_emergency_landing",
            "description": "Instruct the drone to perform an emergency landing.",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "enum": ["current", "home_base", "custom"],
                        "description": "Specifies the emergency landing location.",
                    },
                    "coordinates": {
                        "type": "object",
                        "description": "GPS coordinates for custom emergency landing location. Required if location is 'custom'.",
                    },
                },
                "required": ["location", "coordinates"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "configure_led_display",
            "description": "Configure the LED display on the drone for notifications or messages.",
            "parameters": {
                "type": "object",
                "properties": {
                    "pattern": {
                        "type": "string",
                        "enum": ["solid", "blink", "pulse", "rainbow"],
                        "description": "Pattern for the LED display.",
                    },
                    "color": {
                        "type": "string",
                        "enum": ["white", "red", "green", "blue", "yellow"],
                        "description": "Color of the LED display. Not required if pattern is 'rainbow'. Optional, defaults to white.",
                    },
                },
                "required": ["message"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "set_drone_speed",
            "description": "Set the speed of the drone.",
            "parameters": {
                "type": "object",
                "properties": {
                    "speed": {
                        "type": "integer",
                        "description": "Specifies the speed in km/h. Valid range is 0 and 100.",
                        "minimum": 0,
                    },
                },
                "required": ["speed"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "set_home_location",
            "description": "Set or change the home location for the drone.",
            "parameters": {
                "type": "object",
                "properties": {
                    "coordinates": {
                        "type": "object",
                        "description": "GPS coordinates for the home location.",
                    },
                },
                "required": ["coordinates"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "reject_request",
            "description": "Use this function if the request is not possible.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    },
]


# how function calling performs with some straight forward feasible prompts
straightforward_prompts_to_expected = {
    "Take off the drone to an altitude of 50 meters.": "takeoff_drone",
    "Land the drone at the current location.": "land_drone",
    "Move the drone forward by 5 meters.": "control_drone_movement",
    "Can you take a photo?": "capture_image",
    "Set the flight mode to autonomous.": "set_flight_mode",
    # Add more prompts and expected function calls as needed
}

# evaluate the model with the straightforward prompts
eval(
    model=MODEL,
    system_prompt=DRONE_SYSTEM_PROMPT,
    functions_list=DRONE_FUNCTIONS_LIST,
    prompts_to_expected_tool_name=straightforward_prompts_to_expected,
)


# let's try some more difficult requests: requests that are almost feasible and are drone-related,
# but that the drone cannot actually do, and the pilot should reject.
challenging_prompts_to_expected = {
    "Can you take off the drone and fly it to the moon?": "reject_request",
    "Land the drone on a moving train.": "reject_request",
    "Can you make the drone fly upside down?": "reject_request",
    "Take a photo of the entire city from 1000 meters above.": "reject_request",
    # Add more challenging prompts and expected function calls as needed
}

# evaluate the model with the challenging prompts
eval(
    model=MODEL,
    system_prompt=DRONE_SYSTEM_PROMPT,
    functions_list=DRONE_FUNCTIONS_LIST,
    prompts_to_expected_tool_name=challenging_prompts_to_expected,
)