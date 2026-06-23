import psutil
from error_treatment import error

class CPU:
    """
    Read and show cpus metrics.
    """
    def __init__(self):
        self.physical_cpus = self.get_physical_cpu_counter()
        self.logical_cpus = self.get_logical_cpu_counter()
        self.cpu_frequency = self.get_cpu_frequency()

    def get_general_information(self) -> dict:
        """
        Return a dict with all CPUs properties
        """

        try:
            properties = {}
            for k in (prop :=self.__dict__):
                properties[k] = prop[k]
            return properties
        except Exception as e:
            error.error_log_message(e)

    def get_physical_cpu_counter(self) -> int:
        """
        Returns the number of physical CPUs
        """
        try:
            return psutil.cpu_count(logical=False)
        except Exception as e:
            error.error_log_message(e)
    
    def get_logical_cpu_counter(self) -> int:
        """
        Returns the number of logical CPUs
        """

        try:
            return psutil.cpu_count(logical=True)
        except Exception as e:
            error.error_log_message(e)
    
    def get_cpu_frequency(self):
        """
        Returns decpu frequency
        """

        try:
            return psutil.cpu_freq(percpu=False)
        except Exception as e:
            error.error_log_message(e)
            return "Não foi possível exibir essa informação"