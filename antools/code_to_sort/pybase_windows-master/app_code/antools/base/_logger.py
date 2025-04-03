import __main__
import app_settings as sett

import importlib
import json
from configparser import ConfigParser

from datetime import datetime, timedelta
import logging
import os
import sys
import inspect
import unicodedata

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.mime.base import MIMEBase


VARIABLES_FILE = "error_variables.json"
DEV_LOG_FILE_PATH = "last_run_dev_log.log"

class _Logger():
    """
    Multifunctional logger

    * can perform standard logger operation
    * is able to catch and log unhandled errors
    * is able to send custom email with errors (including app_log and last used variables)

    ...

    Attributes
    ----------
    _activated : bool
        set to True when get_Logger method is called

    Following attributes are called from app_settings.py (upper version without underscore)
    _lang : str
        language of the logger
    _level : str
        in PRODUCTIONUCTION -> INFO, else DEBUG
    _console_log : bool
        log to console
    _file_log : bool
        log to file
    _file_path : str
        if _file_log enables, path to the file
    _logger : object
        instance of logging class

    Methods
    -------
    debug
        XXX
    info
        XXX
    warning
        XXX
    critical
        XXX
    error
        XXX
    exception
        XXX
    finish
        XXX
    _collect_variables
        XXX

    """

    __slots__ = "_activated", "_lang", "_level", "_console_log", "_file_log", \
                "_file_path", "_send_error_email", "_logger", "_dev_logger"
    
    def __init__(self) -> object:
        """ Only returns instance of object and set default values """
        self._activated = False
        self._lang = "ENG"
        self._level = "ERROR"
        self._console_log = False
        self._file_log = False
        self._file_path = None
        self._logger = logging.getLogger("NORMAL")
        self._dev_logger = logging.getLogger("DEV_LOG")


    def __str__(self) -> str:
        return f"{self.__class__.__name__}(level={self._level}, file={self._file_path if self._file_log else 'None'})"


    def __repr__(self) -> str:
        return self.__str__()


    def __call__(self) -> str:
        return self.__str__()


    def finish(self, notification_func=None) -> SystemExit:
        """ Call this function manually when script is finished """

        if self._lang == "ENG":
            text = "SCRIPT HAS FINISHED SUCESSFULLY!"
        elif self._lang == "CZE":
            text = "SCRIPT USPESNE DOBEHL!"
        self.info(text.center(50, "-"))

        if notification_func: notification_func()

        if sett.SUCCESS_WAIT_FOR_USER:
            if self._lang == "ENG":
                input("Press any key to close the terminal ...")
            elif self._lang == "CZE":
                input("Pro uzavreni terminalu zmacknete jakkoukoli klavesu ...")

        raise SystemExit(0)

    def debug(self, msg:str):
        """ Logs debug messages
        
        Parameters
        ----------
        msg : str
            Message to be logged.

        """
        msg = str(msg) if isinstance(msg, TypeError) else msg
        self._logger.debug(self._rmv_diacritics(self._get_msg_format() + msg))
        self._dev_logger.debug(self._rmv_diacritics(self._get_msg_format() + msg))
            

    def info(self, msg:str):
        """ Logs info messages.
        
        Parameters
        ----------
        msg : str
            Message to be logged
        
        """
        msg = str(msg) if isinstance(msg, TypeError) else msg
        self._logger.info(self._rmv_diacritics(self._get_msg_format() + msg))
        self._dev_logger.info(self._rmv_diacritics(self._get_msg_format() + msg))
        
        

    def warning(self, msg:str):
        """ Logs warning messages
        
        Parameters
        ----------
        msg : str
            Message to be logged
        
        """
        msg = str(msg) if isinstance(msg, TypeError) else msg
        self._logger.warning(self._rmv_diacritics(self._get_msg_format() + msg))
        self._dev_logger.warning(self._rmv_diacritics(self._get_msg_format() + msg))
    

    def critical(self, msg:str):
        """ Logs critical messages
        
        Parameters
        ----------
        msg : str
            Message to be logged
        
        """     
        msg = str(msg) if isinstance(msg, TypeError) else msg
        self._logger.critical(self._rmv_diacritics(self._get_msg_format() + msg))
        self._dev_logger.critical(self._rmv_diacritics(self._get_msg_format() + msg))


    def error(self, msg:str, error=SystemError, terminate:bool = False):
        """ Logs error messages and terminates the system if wanted.
        
        Parameters
        ----------
        msg : str
            Message to be logged
        error : Error, optional
            ErrorType (default is SystemError).
        terminate : bool, optional
            If true, AppReporter will shut down process (default is False).

        """
        msg = str(msg) if isinstance(msg, TypeError) else msg
        self._logger.error(self._rmv_diacritics(self._get_msg_format() + msg))
        self._dev_logger.error(self._rmv_diacritics(self._get_msg_format() + msg))
        if terminate:
            error = SystemError if error == SystemExit else error # because of VSCode
            raise error(msg)


    def exception(self, msg:str, error=SystemError, add_info:bool = True, terminate:bool = False):
        """ Logs exception messages and terminates the system if wanted
        
        Parameters
        ----------
        msg :str
            Message to be logged
        error : Error, optional
            ErrorType (default is SystemError)
        add_info : bool, optional
            Adds traceback to the message (default is False)
        terminate : bool, optional
            If true, AppReporter will shut down process (default is False)

        """
        msg = str(msg) if isinstance(msg, TypeError) else msg
        add_info = True if terminate else add_info
        self._logger.exception(self._rmv_diacritics(self._get_msg_format() + msg), exc_info=add_info)
        self._dev_logger.exception(self._rmv_diacritics(self._get_msg_format() + msg))
        if terminate:
            error = SystemError if error == SystemExit else error # because of VSCode
            raise error(msg)


    def _class_error(self, text:str, class_obj:object, err:TypeError, terminate:bool=True):
        self.error(f"{class_obj} {text.lower()} due to -> {str(err)}", terminate=terminate)


    def _start(self) -> None:
        """ Start log message when _active=True """

        if self._lang == "ENG":
            txt = "SCRIPT STARTED!"
            txt2 = "File log can be found here"
        elif self._lang == "CZE":
            txt = "SCRIPT ZACAL!"
            txt2= "Prubeh scriptu je zaznacen zde"

        self.info(txt.center(50, "-"))
        self.info(txt2 + " -> " + self._file_path) if self._file_log else None


    def _get_msg_format(self) -> str:
            """ Formats Logger msg for logging messages. """

            if self._level == "DEBUG":
                try:
                    stack = inspect.stack()[2]
                    path = stack.filename.capitalize().replace(os.getcwd().capitalize(), ".")
                    function = stack.function if stack.function != "<module>" else "module"
                    return f"{path} : line {stack.lineno} : function <{function}>" + " : "
                except:
                    return f""

            else:
                return f""


    def _rmv_diacritics(self, msg:str) -> str:
        """ Removes diacritics from string"""
        return unicodedata.normalize('NFKD', msg).encode('ASCII', 'ignore').decode('utf-8', 'ignore')


    def _collect_variables(self) -> dict:
        """ Collects variables from sett.LOGGER_FINAL_VARIABLES_COLLECTION_FILES when script fails"""


        def _hide_passwords(dict_val) -> dict:
            for key, value in dict_val.items():
                for w in ["heslo", "hesla", "hesel", "pw", "password"]:
                    if w in key.lower():
                        dict_val[key] = "XXX"
            return dict_val

        # gather all variables
        variables_dict = {}

        for file in sett.LOGGER_FINAL_VARIABLES_COLLECTION_FILES:
            if file.endswith(".py"):
                try:
                    pop_list = list()
                    temp_dict = __main__.__dict__ if file == sett.MAIN_FILE else importlib.import_module(file.replace(".py", "")).__dict__

                    for key, value in temp_dict.items():

                        # delete python stuff
                        if key.startswith("__") or key.endswith("__"):
                            pop_list.append(key)
                            continue

                        
                        # remove imported functions, modules and imported instances
                        type_val = str(type(value))
                        for w in ["function", "module", "type"]:
                            if w in type_val:
                                pop_list.append(key)
                                continue

                    curr_dict = dict()
                    for key in temp_dict:
                        if key not in pop_list:
                            curr_dict[key] = str(temp_dict[key]) if not isinstance(temp_dict[key], (str, int, float, complex, bool, list, dict)) else temp_dict[key]

                except Exception as err:
                    self._logger.warning(f"Variables from Python file {file} could not be exported due to -> {err}")

            elif file.endswith(".json"):
                try:
                    with open ("abc.json", "r") as openfile:
                        curr_dict = json.load(openfile)
                except Exception as err:
                    self._logger.warning(f"Variables from JSON file {file} could not be exported due to -> {err}")

            elif file.endswith(".ini"):
                try:
                    read_config = ConfigParser()
                    read_config.read(file)

                    curr_dict = dict()
                    for key, value in read_config._sections.items():
                        for key2, value2 in value.items():
                            curr_dict[key + "." + key2] = value2

                except Exception as err:
                    self._logger.warning(f"Variables from Config file {file} could not be exported due to -> {err}")

            else:
                self._logger.warning(f"File extenstion of file {file} is not yet supported for exporting last used variables!")


            curr_dict = _hide_passwords(curr_dict) if sett.LOGGER_ERROR_EMAIL_DEV_HIDE_PWD else curr_dict
            curr_dict = dict(sorted(curr_dict.items(), key=lambda x: x[0].lower()) )
            variables_dict[file] = curr_dict if curr_dict else f"NOT ABLE TO GET"

        return variables_dict


    def _send_email(self, email:str, email_pwd:str, server:str, port:int, 
                    email_to:str, email_to_cc:str, email_to_bcc:str, subject:str, text:str, attachments:list):

        try:
            all_recipients = list()
            msg = MIMEMultipart("alternative")
            msg['From'] = email
            msg['To'] = email_to
            msg["Cc"] = email_to_cc
            msg["Bcc"] = email_to_bcc
            msg["Subject"] = subject

            [all_recipients.append(item) for item in email_to.split(", ") if item]
            [all_recipients.append(item) for item in email_to_cc.split(", ") if item]
            [all_recipients.append(item) for item in email_to_bcc.split(", ") if item]

            msg.attach(MIMEText(text, "html" if "<html>" in text else "plain"))

            attachments = [attachments] if not isinstance(attachments, list) else attachments
            for file in attachments:
                with open(file, "rb") as attachment:
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(attachment.read())

                    encoders.encode_base64(part)
                    part.add_header(
                        "Content-Disposition",
                        f"attachment; filename= {file}",
                    )
                    msg.attach(part)

            self._dev_logger.debug(f"Email has been sent to the following emails: {all_recipients}")
            with smtplib.SMTP_SSL(server, port) as smtp:
                    if email_pwd:
                        smtp.login(email, email_pwd)
                    else:
                        smtp.starttls()
                    smtp.sendmail(email, all_recipients, msg.as_string())

            return True, "OK"
            
        except Exception as err:
            return False, str(err)


    def _send_error_email_to_dev(self) -> None:
        """ Send error email to developer with file_log and last used variables """

        
        attachments = list()

        # store current variables
        try:
            try:
                with open(VARIABLES_FILE, 'w') as openfile:
                    json.dump(self._collect_variables(), openfile, indent=2)

                attachments.append(VARIABLES_FILE)

            except Exception as err:
                print(err)

            attachments.append(DEV_LOG_FILE_PATH)
            attachments.append(self._file_path) if self._file_path else None
            
            subject = f"{sett.DEV_SCRIPT_ID} : {sett.CLIENT_SCRIPT_NAME} has FAILED! "
            text = f"""{sett.CLIENT_COMPANY_NAME}
{sett.CLIENT_CONTACT_PERSON} 
{sett.CLIENT_CONTACT_EMAIL} 
{sett.CLIENT_CONTACT_PHONE}               
"""

            sent, resp = self._send_email(
            sett.LOGGER_ERROR_EMAIL_DEV_FROM,
            sett.LOGGER_ERROR_EMAIL_DEV_FROM_PWD,
            sett.LOGGER_ERROR_EMAIL_DEV_SERVER,
            sett.LOGGER_ERROR_EMAIL_DEV_PORT,
            sett.LOGGER_ERROR_EMAIL_TO_DEV_EMAIL,
            "",
            "",
            subject,
            text,
            attachments)
            
            if os.path.exists(VARIABLES_FILE): os.remove(VARIABLES_FILE) 

            if sent:
                return True, "OK"
            else:
                return False, resp
                

        except Exception as err:
            return False, str(err)


    def _send_error_email_to_customer(self, sent_to_develeper:bool) -> None:
        """ Send error email to customer """

        try:
            if self._lang == "ENG":
                subject = f"Script {sett.CLIENT_SCRIPT_ID} : {sett.CLIENT_SCRIPT_NAME} has FAILED! "

                if sent_to_develeper:
                    text = \
                            f"""Unfortunately, the script <{sett.CLIENT_SCRIPT_ID}> : <{sett.CLIENT_SCRIPT_ID}> has failed. We know about this issue, there is no need to contact us.
We will try to solve it as soon as possible and we will contact you with further info!
Please, do not respond to this email!
                    
Best regards,
{sett.DEV_COMPANY}
{sett.DEV_NAME}
{sett.DEV_EMAIL}
{sett.DEV_PHONE}
                            """
                else:
                    text = \
                            f"""Unfortunately, the script <{sett.CLIENT_SCRIPT_ID}> : <{sett.CLIENT_SCRIPT_ID}> has failed. 
If action should be taken by developer, he has to be notified from your side first.
Please, do not respond to this email!
                    
Best regards,
{sett.DEV_COMPANY}
{sett.DEV_NAME}
{sett.DEV_EMAIL}
{sett.DEV_PHONE}
                                """


            elif self._lang == "CZE":
                subject = f"Script {sett.CLIENT_SCRIPT_ID} : {sett.CLIENT_SCRIPT_ID} NEDOBĚHL! "
                if sent_to_develeper:
                    text = \
                        f"""Bohužel, script <{sett.CLIENT_SCRIPT_ID}> : <{sett.CLIENT_SCRIPT_NAME}> nedoběhl správně. O této záležitosti víme, není potřeba nás dále kontaktovat.
Chybu se budeme snažit vyřešit co nejříve a ozveme se Vám až budeme mít nové informace.
Prosím, na tento email neodpovídejte.
                    
S přáním pěkného dne,
{sett.DEV_COMPANY}
{sett.DEV_NAME}
{sett.DEV_EMAIL}
{sett.DEV_PHONE}
                        """
                else:
                    text = \
                        f"""Bohužel, script <{sett.CLIENT_SCRIPT_ID}> : <{sett.CLIENT_SCRIPT_NAME}> nedoběhl správně.
Vývojář o této záležitosti neví. Pokud požadadujete jeho asistenci, je potřeba ho kontaktovat.
Prosím, na tento email neodpovídejte.
                    
S přáním pěkného dne,
{sett.DEV_COMPANY}
{sett.DEV_NAME}
{sett.DEV_EMAIL}
{sett.DEV_PHONE}
                        """


            attachments=list()

            if sett.LOGGER_ERROR_EMAIL_ADD_LOG_TO_CLIENT:
                attachments.append(self._file_path)
                attachments.append(DEV_LOG_FILE_PATH)
                if os.path.exists(VARIABLES_FILE): os.remove(VARIABLES_FILE) 

                try:
                    with open(VARIABLES_FILE, 'w') as openfile:
                        json.dump(self._collect_variables(), openfile, indent=2)

                    attachments.append(VARIABLES_FILE)

                except Exception as err:
                    print(err)

            sent, resp = self._send_email(
            sett.LOGGER_ERROR_EMAIL_CLIENT_FROM,
            sett.LOGGER_ERROR_EMAIL_CLIENT_FROM_PWD,
            sett.LOGGER_ERROR_EMAIL_CLIENT_SERVER,
            sett.LOGGER_ERROR_EMAIL_CLIENT_PORT,
            sett.LOGGER_ERROR_EMAIL_CLIENT_TO,
            sett.LOGGER_ERROR_EMAIL_CLIENT_TO_CC,
            sett.LOGGER_ERROR_EMAIL_CLIENT_TO_BCC,
            subject,
            text,
            attachments)

            return sent, resp

        except Exception as err:
            return False, str(err)


    def _replace_traceback(self) -> None:  
            """ Replace traceback for logging unexpected errors """

            def log_traceback_system(exc_type, exc_value, exc_traceback):

                # do nothing when keyboard interrupt
                if issubclass(exc_type, KeyboardInterrupt):
                    sys.__excepthook__(exc_type, exc_value, exc_traceback)
                    return

                # log error messages when unexpected error
                if not self._console_log:
                    sh = logging.StreamHandler()
                    sh.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"))
                    Logger._logger.addHandler(sh)
                    Logger._console_log = True

                if self._lang == "ENG":
                    txt = "The following error cannot be handled!"
                    txt2 = "SCRIPT FAILED"
                elif self._lang == "CZE":
                    txt = "Nasledujici chyba byla kriticka!"
                    txt2 = "SCRIPT CHYBNE UKONCEN"

                # add error and used variables
                self._logger.error(self._get_msg_format() + txt + " \n", exc_info=(exc_type, exc_value, exc_traceback))
                self._dev_logger.error(self._get_msg_format() + txt + " \n", exc_info=(exc_type, exc_value, exc_traceback))
                self._logger.error(txt2.center(50, "-"))
                self._dev_logger.error(txt2.center(50, "-"))
            
                # send email to developer
                sent_d, resp_d = False, None
                if sett.ERROR_SEND_EMAIL_TO_DEVELOPER:
                    sent_d, resp_d = self._send_error_email_to_dev()

                    if self._lang == "ENG":
                        if sent_d:
                            self._logger.info("Email with errors was sent to developer!")
                        else:
                            self._logger.critical(f"Email with errors was NOT sent to developer due to -> {resp_d}!")

                    elif self._lang == "CZE":
                        if sent_d:
                            self._logger.info("Email s chybami byl zaslan vyvojari!")
                        else:
                            self._logger.critical(f"Email s chybami NEBYL zaslan vyvojari z duvodu -> {resp_d}!")

                else:
                    if self._lang == "ENG":
                        self._logger.warning("Email with errors was NOT sent to developer due to -> OPTION NOT ALLOWED!")
                    elif self._lang == "CZE":
                        self._logger.warning("Email s chybami NEBYL zaslan vyvojari protoze -> MOZNOST NEBYLA POVOLENA!")
                    

                # send email to client
                if sett.ERROR_SEND_EMAIL_TO_CLIENT:
                    send_c, resp_c = self._send_error_email_to_customer(sent_d)
                    if send_c:
                        if self._lang == "ENG":
                            self._logger.info("Email with errors was sent to client!")
                        elif self._lang == "CZE":
                            self._logger.info("Email s chybami byl poslán zákazníkovi!")
                    else:
                        if self._lang == "ENG":
                            self._logger.warning(f"Email with errors was NOT sent to client due to {resp_c}!")
                        elif self._lang == "CZE":
                            self._logger.warning(f"Email s chybami NEBYL poslán zakaznikovi z důvodu {resp_c}")
                else:
                    if self._lang == "ENG":
                        self._logger.warning("Email with errors was NOT sent to client due to -> OPTION NOT ALLOWED!")
                    elif self._lang == "CZE":
                        self._logger.warning("Email s chybami NEBYL zaslan klientovi protoze -> MOZNOST NEBYLA POVOLENA!")


                if sett.ERROR_WAIT_FOR_USER:
                    print(".\n.\n.")
                    if self._lang == "ENG":
                        input("Press any key to close the terminal ...")
                    elif self._lang == "CZE":
                        input("Pro uzavreni terminalu zmacknete jakkoukoli klavesu ...")

            # replace traceback
            sys.excepthook = log_traceback_system 


Logger = _Logger()

def get_logger(_activate:bool = True, lang:str=sett.LANGUAGE, level:str=sett.LOG_LEVEL, 
                log_to_console:bool = sett.LOG_TO_CONSOLE, log_to_file:bool = sett.LOG_TO_FILE,
                log_folder:str = sett.LOGGER_FOLDER_PATH, delete_old:bool = sett.LOGGER_DELETE_OLD_LOGS,
                delete_older_than_days:int = sett.LOGGER_DELETE_OLD_LOGS_DAYS,
                file_timestamp_fmt:str = sett.LOGGER_FILE_TIMESTAMP_FORMAT) -> Logger:
    """ Method for obtaining Logger
        _activate -> set to False for all not main source code! """

    # Logger can be activated only once

    if _activate and not Logger._activated:

        Logger._lang = lang
        Logger._level = level
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

        # dev_logger
        Logger._dev_logger.setLevel("DEBUG")
        fh_dev = logging.FileHandler(DEV_LOG_FILE_PATH, mode='w')
        fh_dev.setFormatter(formatter)
        Logger._dev_logger.addHandler(fh_dev)

        # normal_logger
        Logger._logger.setLevel(Logger._level)   

        try:
            if Logger._lang not in ["ENG", "CZE"]:
                raise AttributeError("Language of Logger must be 'ENG' or 'CZE'!")

            # add console log
            if log_to_console:
                sh = logging.StreamHandler()
                sh.setFormatter(formatter)
                Logger._logger.addHandler(sh)
                Logger._console_log = True

            if log_to_file:
                now = datetime.now()
                file_start = "run_"
                file_end = ".log"

                # create folder path
                os.makedirs(log_folder) if not os.path.exists(log_folder) else None

                # delete old logs
                if delete_old:
                    for file in os.listdir(log_folder):
                        if file.endswith(file_end):
                            date = file.replace(file_start, "").replace(file_end, "")
                            log_time = datetime.strptime(date, file_timestamp_fmt)
                            os.remove(os.path.join(log_folder, file)) if log_time < now - timedelta(days=delete_older_than_days) else None

                # create new log file
                Logger._file_path = os.path.join(log_folder, file_start + now.strftime(file_timestamp_fmt) + file_end)
                fh = logging.FileHandler(Logger._file_path, mode='w')
                fh.setFormatter(formatter)
                Logger._logger.addHandler(fh)
                Logger._file_log = True

            # replace traceback for unexpected errors
            Logger._replace_traceback()
            Logger._activated = True

            # print start msg
            Logger._start()

        except Exception as err:
            raise SystemError(f"Cannot initialize Logger due to -> {err}!")

    elif _activate and Logger._activated:
        Logger.warning("Logger has already been activated! No action will be done!")

    return Logger
