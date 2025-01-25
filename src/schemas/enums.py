from enum import Enum

class RepairType(str, Enum):
    demage = "demage"
    malfunction = "malfunction"
    undefined = "undefined"
    not_detected = "not_detected"
    
class TaskStatus(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    done = "cone"