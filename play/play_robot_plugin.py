__author__ = 'cocoon'




platform_file = "../samples/robot/mobile/platform.json"


import time
from droydrunner.robot_plugin import Pilot



# setup users with device id
Alice =   "e7f54be6"
Bob = 	"388897e5"


pilot = Pilot()

pilot.setup_pilot("mobile","mobile_qualif",platform_configuration_file=platform_file)


pilot.open_Session(Alice,Bob)

time.sleep(5)
pilot.close_session()




print

