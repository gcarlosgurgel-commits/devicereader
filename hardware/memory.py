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
        Returns the number of physical CPUs
        """
        try:
            return psutil.virtual_memory()
        except Exception as e:
            error.error_log_message(e)