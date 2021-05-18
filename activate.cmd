@echo off


IF "%1" == "-a" (
    env\Scripts\activate
    echo "Activate Env"
)

IF "%1" == "" (
    env\Scripts\activate
    echo "Activate Env"
)

IF "%1" == "-d" (
    env\Scripts\deactivate
    echo "Deactivate Env"
)