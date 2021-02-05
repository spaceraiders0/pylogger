# spacelogger
spacelogger is a small logging utility that was created for simple and small projects. I personally found the Logger module in Python's standard library to be quite bulky, and had interference from other module's loggers. While this is for a reason, I did not want this. I also liked the idea of having colored text in my log messages.

## How to use
To initialize your Logger, all that must be done is to import the Logger module, and provide it with the string that each log message will be prefixed with, and the directory that files should be logged to. From there, you are free to use the **log** method provided by the Logger class. Here is some example code:


```python
from spacelogger import SpaceLogger

my_logger = SpaceLogger("%L %N @ %T", logging_directory="./logs")
my_logger.log("This is a log message.", "CRITICAL")
#=> "CRITICAL ROOT @ 07:44:26 This is a log message."
```

## Logger modes
spacelogger comes with 5 base modes that have different colored assigned to their output text. This is the main difference between them, outside of being able to use different log levels in your format prefixes. Here is a list of each mode, and the color that is assigned to it.
```
DEBUG    - White
INFO     - Grey
SUCCESS  - Green
WARNING  - Yellow
CRITICAL - Red
```

## Format specifiers
spacelogger provides a few format specifiers that can be used in the log prefixes,
as well as the log messages themselves. Here are the format specifiers that can
currently be used:
```
%D - The current date.
%T - The current time.
%C - The logger's creation time.
%N - The logger's name.
%P - The path of the file
%L - The message's level.
%% - An escaped percent sign.
```
