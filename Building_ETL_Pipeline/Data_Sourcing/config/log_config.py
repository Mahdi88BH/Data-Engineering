import logging
import logging.config
import os.path

def log_config():
    # Define a dictionary configuration for Python's logging subsystem
    config = {
        'version': 1,  # Required by dictConfig schema; currently only version 1 is supported
        'disable_existing_loggers': False,  # Keeps any pre-existing loggers active instead of wiping them out
        
        # 1. Formatters: Define how the text of your log messages will look
        'formatters': {
            'standard': {
                # Format: Timestamp [Log Level] Logger Name: The Actual Message
                'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
            },
        },
        
        # 2. Handlers: Determine where the logs go (e.g., console, file, network)
        'handlers': {
            'default_handler': {
                'class': 'logging.FileHandler',  # Writes log output directly to a file on disk
                'level': 'DEBUG',  # Captures DEBUG messages and all higher levels (INFO, WARNING, ERROR, CRITICAL)
                'formatter': 'standard',  # Applies the 'standard' layout format defined above
                'filename': os.path.join('logs', 'etl_pipeline.log'),  # Saves logs to 'logs/etl_pipeline.log' safely across OS paths
                'encoding': 'utf8'  # Forces UTF-8 text encoding to prevent character crashes
            },
        },
        
        # 3. Loggers: Control which logs are captured and route them to handlers
        'loggers': {
            '': {  # The empty string '' represents the root logger, catching all application logs
                'handlers': ['default_handler'],  # Routes logs captured here to our FileHandler
                'level': 'DEBUG',  # Minimum severity threshold for this logger
                'propagate': False  # Prevents duplicate logging by stopping messages from bubbling up to parent loggers
            }
        }
    }
    
    # Load and apply the configuration dictionary into Python's logging system
    logging.config.dictConfig(config)

# Entry point: Runs log_config() when this script is executed directly
if __name__ == '__main__':
    log_config()




# 1. Global Settings
#     'version': 1: A mandatory schema version number for dictConfig. Always set to 1.
#     'disable_existing_loggers': False: When set to True, Python destroys any loggers that were 
#           configured elsewhere before this function ran. Setting it to False ensures third-party 
#           libraries or existing scripts retain their loggers.

# 2. Formatters ('formatters')
# Formatters specify the exact template string for your log messages.
#     In this script, the 'standard' formatter uses placeholders like %(asctime)s (timestamp), 
#       %(levelname)s (e.g., INFO, ERROR), %(name)s (the logger's module name), and %(message)s 
#       (the log content).
#     A sample output line using this format looks like:
#     2026-06-06 12:00:00,123 [INFO] root: ETL pipeline started successfully.

# 3. Handlers ('handlers')
# Handlers dictate where the logs are sent.
#     Here, you are using a 'logging.FileHandler', which creates or appends to a log file.
#     os.path.join('logs', 'etl_pipeline.log') ensures that your log is saved inside a folder named 
#       logs. (Note: Ensure the logs directory exists in your project workspace before running this 
#       code, otherwise Python will throw a FileNotFoundError when attempting to write the file).

# 4. Loggers ('loggers')
# Loggers act as the gatekeepers of your messages.
#     The key '' (empty string) represents the root logger. Any log message emitted anywhere in 
#       your code will pass through this root logger unless a specific named sub-logger overrides it.
#     'propagate': False stops messages from bubbling up to higher-level system handlers, avoiding 
#       duplicate lines in your log files.