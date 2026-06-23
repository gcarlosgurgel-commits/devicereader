#Function thats create and format the logged errors messages.

#Anotações:
#Falta estudar formatos de erro no pytyhon e a melhor forma de aramazenalos se devo trata-lo como um objeto

from datetime import date, datetime
from functools import partial
from pathlib import Path
import json


error_file_path = Path(__file__).resolve().parent / "errors.log" #Dyanmic path to erros.log file. No hard Coded.

__all__ = ["error_log_message"]

def __error_date_format():
    """
    Create a pattern for the date logged into erros.log file;
    Returns a tuple with date and a timestamp.
    """

    today = date.today().strftime(r"%d/%m/%Y")
    hour = datetime.now().strftime(r"%H:%M:%S")

    return today, hour


def __pattern_message(date_time, error_message):
    """
    Create the pattern message of errors log;

    Parameters:
        date_time - A positional parameter. The tuple returned by the _error_dateformat() function;
        message - A positional parameter. The message raised for the error.

    Returns a string that contains , date , hours and error message.
    
    """

    error_struct = {
        "TypeError": str(type(error_message).__name__),
        "ArgumentsListErro": list(error_message.args),
        "LinePathError": str(error_message.__traceback__.tb_frame),
        "StartScopeError": str(error_message.__traceback__.tb_frame.f_code),
        "ErrorFileName": error_message.__traceback__.tb_frame.f_code.co_filename,
        "ErrorScopeName": error_message.__traceback__.tb_frame.f_code.co_name,
        "ErrorLineNo": int(error_message.__traceback__.tb_lineno),
    }
    return f"{date_time[0]} | {date_time[1]}: {json.dumps(error_struct, indent=3)}"


def __base_error_log_message(func_message, date_time, error_message):
    """
    Function: Main function. Calls the other functions _error_date_format() and _pattern_message() to write in error.log file.";
    Parameters:
        func_message - Receive the _pattern_menssage() function.
        date_time - Receive the _error_date_format() function.
        message  - the message error raised. The message will be argument to the _patter_message() function.
    """

    with open(error_file_path, "a+") as archive:
        print(f"[ERROR]: Something went wrong. Try later...") 
        print(func_message(date_time, error_message), file=archive)
        


error_log_message = partial(__base_error_log_message, __pattern_message, __error_date_format()) #Fix the first and second positional argument in base_error_log_message 

error_log_message.__doc__ ="""
Write an error message to the errors.log file.

The function automatically formats the log entry using the current
date and time and appends the message to the log file.

Parameters:
    message (str):
        Error message to be written to the log file.

Example:
    error_log_message("File not found")
"""