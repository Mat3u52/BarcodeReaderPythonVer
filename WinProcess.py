import os

process_name = "CalculatorApp"
try:
    killed = os.system('tskill ' + process_name)
    print("ok")
except Exception:
    print("not exist")