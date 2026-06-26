import psutil
from error_treatment import error

class Memory:
    """
    Read and show RAM metrics.
    """
    def __init__(self):
        self.memory_information = self.get_memory_information()

    def get_general_information(self) -> dict:
        """
        Return a dict with all RAM properties
        """

        try:
            properties = {}
            for k in (prop :=self.__dict__):
                properties[k] = prop[k]
            return properties
        except Exception as e:
            error.error_log_message(e)

    def get_memory_information(self) -> int:
        """
        Returns the memory informations expressed in bytes.
        
        - total: total physical memory available;
        - available: the memory that can be given instantly to processes without the system going into swap;
        - percent: the percentage usage calculated as (total - available) / total * 100;
        - used: the percentage usage calculated as (total - available) / total * 100;
        - free: memory not being used at all (zeroed) that is readily available;
                note that this doesn't reflect the actual memory available
                (use 'available' instead)

        """
        try:
            data = psutil.virtual_memory()
            return {
                "total": data.total,
                "available": data.available,
                "percent": data.percent,
                "used": data.used,
                "free": data.free
            }
        except Exception as e:
            error.error_log_message(e)