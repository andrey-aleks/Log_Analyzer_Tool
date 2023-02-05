# Log_Analyzer_Tool
A tool for the analysis of Unreal Engine logs.

**File to analyze** - ordinary log file from Unreal Engine. I use 'profilegpu' command in particular areas of level to print the necessary details into log. Also there are some preparations in engine to specify cameras locations & names.
There are 2 types of analyzers:

**1. 1-file analyzer.** Put the script near the Log file and run it - you will get all the info about average MS & FPS and about this data for each location in game.
Video-demostration:

https://user-images.githubusercontent.com/58087965/216849109-95549ff8-8b7f-45a7-8827-d33dab4dcc65.mp4


**2. Bulk analyzer.** Nearly the same as **1-file analyzer**, but it works with a bunch of files at once. Put the script near the folders with PC specifications, run it, and it will create a CSV file for each Log down below in folders. 
Video-demostration:

https://user-images.githubusercontent.com/58087965/216849324-97ded22d-bb14-4f81-bccb-f93a256f0286.mp4

