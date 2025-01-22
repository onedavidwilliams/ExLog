from src.exlog.exlog import ExLog
import os
import asyncio
# Utility function to clear logs for clean testing
def clear_logs(log_dir):
    if os.path.exists(log_dir):
        for file in os.listdir(log_dir):
            os.remove(os.path.join(log_dir, file))


async def test_exlog():
    # Create directories for logs
    daily_log_dir = "logs/daily"
    hourly_log_dir = "logs/hourly"
    no_rotation_log_dir = "logs/no_rotation"
    
    # Clear logs before test
    for dir_name in [daily_log_dir, hourly_log_dir, no_rotation_log_dir]:
        os.makedirs(dir_name, exist_ok=True)
        clear_logs(dir_name)

    # Test 1: Basic synchronous logging 
    print("\n=== Test 1: Synchronous Logging ===")
    logger_sync = ExLog(log_level=1, log_dir=daily_log_dir, rotation="daily")
    logger_sync.dprint("This is a debug log.", level="debug")
    logger_sync.dprint("This is an info log.", level="info", color=ExLog.color.green)
    logger_sync.dprint("This is a warning log.", level="warning")
    logger_sync.dprint("This is an error log.", level="error")
    logger_sync.dprint("This is a critical log.", level="critical", background_color=ExLog.bg_color.red)

    # Test 2: Custom tag and colors
    print("\n=== Test 2: Custom Tag and Colors ===")
    logger_sync.dprint("Custom message with a tag", custom_tag="IMPORTANT ALERT", color=ExLog.color.cyan, background_color=ExLog.bg_color.black)

    # Test 3: Logging without timestamp
    print("\n=== Test 3: Logging Without Timestamp ===")
    logger_sync.dprint("This is a log without timestamp", show_timestamp=False)

    # Test 4: Custom log (no tag, no level, timestamp enabled)
    print("\n=== Test 4: Custom Log (No Level/Tag, With Timestamp) ===")
    logger_sync.dprint("This is a plain custom log with timestamp", level="custom", show_timestamp=True)

    # Test 5: Custom log (no tag, no level, timestamp disabled)
    print("\n=== Test 5: Custom Log (No Level/Tag, No Timestamp) ===")
    logger_sync.dprint("This is a plain custom log without timestamp", level="custom", show_timestamp=False)

    # Test 6: Asynchronous logging
    print("\n=== Test 6: Asynchronous Logging ===")
    logger_async = ExLog(log_level=1, log_dir=hourly_log_dir, rotation="hourly")

    await logger_async.adprint("Async debug log", level="debug", color=ExLog.color.blue)
    await logger_async.adprint("Async info log", level="info", color=ExLog.color.green)
    await logger_async.adprint("Async warning log", level="warning", color=ExLog.color.yellow)
    await logger_async.adprint("Async error log", level="error", background_color=ExLog.bg_color.white)
    await logger_async.adprint("Async critical log", level="critical", color=ExLog.color.red, background_color=ExLog.bg_color.white)

    # Test 7: Asynchronous custom log (no level, no tag)
    print("\n=== Test 7: Async Custom Log (No Level/Tag, With Timestamp) ===")
    await logger_async.adprint("This is an async plain custom log with timestamp", level="custom", show_timestamp=True)

    print("\n=== Test 8: Async Custom Log (No Level/Tag, No Timestamp) ===")
    await logger_async.adprint("This is an async plain custom log without timestamp", level="custom", show_timestamp=False)

    # Test 9: Log rotation (none)
    print("\n=== Test 9: No Rotation Logging ===")
    logger_no_rotation = ExLog(log_level=1, log_dir=no_rotation_log_dir, rotation="none")
    for i in range(3):
        logger_no_rotation.dprint(f"Static rotation log #{i + 1}", level="info")

    # Test 10: Log without file logging
    print("\n=== Test 10: Console Only (No File Logging) ===")
    logger_console_only = ExLog(log_level=1)  # No `log_dir`, only prints to console
    logger_console_only.dprint("This log won't save to a file, only console.", level="info")

    # Test 11: Logging with log level set to 0 (disabled)
    print("\n=== Test 11: Disabled Log Level ===")
    logger_disabled = ExLog(log_level=0, log_dir="logs/disabled_logs")
    logger_disabled.dprint("This log should NOT appear.")
    await logger_disabled.adprint("This async log should NOT appear.")

    print("\nAll tests completed!")


if __name__ == "__main__":
    asyncio.run(test_exlog())