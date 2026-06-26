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
    
    def get_cpu_frequency(self) -> dict:
        """
        Returns CPU frequencies.

        Returns a dict that contains:
         - Current: A frequência atual do processador em MHz
         - Min: É a frequência mínima absoluta em MHZ que o processador consegue atingir sob o controle do sistema operacional.
         - Max: É a frequência em MHz máxima nominal (ou de fábrica) que o processador pode atingir em condições normais de uso.


        """

        try:
            data = psutil.cpu_freq(percpu=False)
            return {
                "current": data.current,
                "min": data.min,
                "max": data.max
            }
        except Exception as e:
            error.error_log_message(e)
            return "Não foi possível exibir essa informação"