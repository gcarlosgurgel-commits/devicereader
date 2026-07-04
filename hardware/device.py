import subprocess
import machineid
import json

import error_treatment.error


class Device:
    """
    Class used to describe the device and all its components.

    """
    def __init__(self):
        """
        The instances attributes will be dynamically defined by the create_propertie() function thats called by get_negeral_information.
        """
        properties = self.create_properties()

    def get_general_information(self) -> dict:
        """
        Retrieve general information about the computer system.

        Returns:
            dict: A dictionary containing:
                - Model
                - Name
                - UserName
                - PrimaryOwnerName
                - MachineId
        """
        try:
            result = subprocess.run(
                [
                    "powershell",
                    "-NoProfile",
                    "-Command",
                    "Get-CimInstance",
                    "-ClassName Win32_ComputerSystem",
                    "| Select-Object Model, Name, UserName, PrimaryOwnerName",
                    "| ConvertTo-Json"
                ],
                capture_output=True,
                text= True,
                encoding="cp850"
            )

            machine_id = machineid.id()

            data = json.loads(result.stdout)
            data["MachineId"]=machine_id
            return data
        
        except Exception as e:
            error_treatment.error.error_log_message(e)

    def create_properties(self):
        try:
            for key in (data := self.get_general_information()):
                setattr(self, key.lower(), data[key])
        except Exception as e:
            error_treatment.error.error_log_message(e)



# class Component(Device):
#     """
#     SubClass Used to describe the Device´s component.
#     """
#     def __init__(self):
#         pass #This will keep here because all the properties will be create dynamically



# def _devicesPnP_get_general_information():
#     """
#     Returns a sumarize of device in a dictionary format
#     """
#     try:
#         result = subprocess.run(
#             [
#                 "powershell",
#                 "Get-CimInstance",
#                 "-ClassName",
#                 "Win32_PnPEntity",
#                 "| Select-Object Name, PNPClass",
#                 "| Sort-Object Name"
#                 "| ConvertTo-Json",
#             ],
#             capture_output=True,
#             text=True,
#             encoding="cp850"
#         )

#         data = json.loads(result.stdout)
#         return data

    
#     except Exception as e:
#         error_treatment.error.error_log_message(e)



# def _cpu_get_general_information():
#     """Return a sumarize of cpu in a dictionary format"""
#     try:
#         result = subprocess.run(
#             [
#                 "powershell",
#                 "Get-CimInstance",
#                 "Win32_processor"
#                 "|",
#                 "Select-Object "
#                 "| ConvertTo-Json -Depth 3",
#             ],
#             capture_output=True,
#             text=True,
#             encoding="cp850"
#         )

#         data = json.loads(result.stdout)
#         return data
    
#     except Exception as e:
#         error_treatment.error.error_log_message(e)






# Resumo:

# Win32_PnPEntity              -> dispositivos Plug and Play
# Win32_Processor              -> CPU
# Win32_PhysicalMemory         -> RAM
# Win32_DiskDrive              -> disco físico
# Win32_LogicalDisk            -> unidades C:, D:
# Win32_VideoController        -> GPU
# Win32_NetworkAdapter         -> placa de rede
# Win32_SoundDevice            -> áudio
# Win32_BIOS                   -> BIOS
# Win32_BaseBoard              -> placa-mãe
# Win32_OperatingSystem        -> sistema operacional
# Win32_Process                -> processos
# Win32_Service                -> serviços

# Para inventário de hardware, as mais importantes são:

# Win32_ComputerSystem
    # Model
    # Name
    # UserName
    # PrimaryOwnerName
    # TotalPhysicalMemory
    # NumberOfProcessors
    # NumberOfLogicalProcessors
# Win32_BIOS
# Win32_BaseBoard
# Win32_Processor
# Win32_PhysicalMemory
# Win32_DiskDrive
# Win32_LogicalDisk
# Win32_VideoController
# Win32_NetworkAdapter
# Win32_PnPEntity