#
#                py-google-search  Copyright (C) 2018  Javinator9889                
#   This program comes with ABSOLUTELY NO WARRANTY; for details add the "-h" option.
#           This is free software, and you are welcome to redistribute it
#                 under certain conditions; type "-L" for details.
#


class OfficePatents:
    USA = "ptso:us"
    Europe = "ptso:ep"
    International = "ptso:wo"
    China = "ptso:cn"
    Germany = "ptso:de"
    Canada = "ptso:ca"
    

class PatentStatus:
    Applications = "ptss:a"
    IssuedPatents = "ptss:g"


class AvailablePatentTypes:
    Utility = "ptst:u"
    Design = "ptst:d"
    Plant = "ptst:pp"
    DefensivePublication = "ptst:t"
    AdditionalImprovement = "ptst:ai"
    StatutoryInventionRegistration = "ptst:h"
    