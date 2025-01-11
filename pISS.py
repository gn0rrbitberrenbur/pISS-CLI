#!/usr/bin/env python3

import time
import sys
from lightstreamer.client import *
from datetime import datetime

print("""                
         ____________    _______   ____
   ___  /  _/ __/ __/___/ ___/ /  /  _/
  / _ \_/ /_\ \_\ \/___/ /__/ /___/ /  
 / .__/___/___/___/    \___/____/___/  V.1.0
/_/                                    """)

# lightstreamer subscription
sub = Subscription("MERGE", ["NODE3000005"], ["Value"])
sub.setRequestedSnapshot("yes")

previousValue = None

# listener for lightstreamer
class SubListener(SubscriptionListener):
    def onItemUpdate(self, update):
        global previousValue
        
        currentValue = float(update.getValue("Value"))
        
        currentTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if previousValue is not None:
            changePercentage = ((currentValue - previousValue) / previousValue) * 100
            changeText = f" | Changed by: {changePercentage:.2f}%"
        else:
            changeText = ""
        
        # create loading bar
        maxBarLength = 100
        numBars = int(currentValue)
        numDashes = maxBarLength - numBars
        
        bar = "[" + "|" * numBars + "-" * numDashes + "]"
        
        # print
        sys.stdout.write(f"\rUrinelevels: {currentValue}% | Last updated: {currentTime} {changeText} | {bar}")
        sys.stdout.flush()
        
        previousValue = currentValue    
    
    def onSubscription(self):
        print("Connected!")
    
    def onSubscriptionError(self, code, message):
        print(f"Subscription error: {code}, Message: {message}")

sub.addListener(SubListener())

# initalize and connect to client and subscribe
client = LightstreamerClient("https://push.lightstreamer.com", "ISSLIVE")

client.connect()

client.subscribe(sub)

# end conditions, press ctrl-c to exit
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nDisconnected")
finally:
    client.disconnect()
