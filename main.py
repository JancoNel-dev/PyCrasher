# main.py
# Copyright MIT license
# By Janco Nel

import ctypes
from ctypes import wintypes
import sys

class Status:
    Succeeded = 0
    IncorrectUsage = 1
    InvalidPid = 2
    EnumProcessesFailed = 3
    OpenProcessFailed = 4
    ProcessNotFound = 5
    CrashProcessFailed = 6

def print_usage():
    print(
        "Usage: \n"
        "    crasher <PID>\n"
        "        Crash the process whose ID matches <PID>.\n"
        "\n"
        "    crasher <ProcessName>\n"
        "        Crash all processes whose names match <ProcessName>.\n"
    )

def is_pid(argument):
    return argument.isdigit()

def crash_process_matches_pid(pid_string):
    try:
        converted_pid = int(pid_string)
        if converted_pid <= 0:
            print(f"Invalid PID: {pid_string}.")
            return Status.InvalidPid
        return crash_process_with_pid(converted_pid, None)
    except ValueError:
        print(f"Invalid PID: {pid_string}.")
        return Status.InvalidPid

def crash_processes_match_name(process_name):
    TH32CS_SNAPPROCESS = 0x00000002
    snapshot_handle = ctypes.windll.kernel32.CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0)
    if snapshot_handle == wintypes.HANDLE(-1).value:
        print(f"Fail to enumerate processes. Error: {ctypes.GetLastError()}.")
        return Status.EnumProcessesFailed

    status = Status.ProcessNotFound

    class PROCESSENTRY32(ctypes.Structure):
        _fields_ = [
            ("dwSize", wintypes.DWORD),
            ("cntUsage", wintypes.DWORD),
            ("th32ProcessID", wintypes.DWORD),
            ("th32DefaultHeapID", ctypes.POINTER(wintypes.ULONG)),
            ("th32ModuleID", wintypes.DWORD),
            ("cntThreads", wintypes.DWORD),
            ("th32ParentProcessID", wintypes.DWORD),
            ("pcPriClassBase", ctypes.c_long),
            ("dwFlags", wintypes.DWORD),
            ("szExeFile", wintypes.CHAR * 260),
        ]

    process_entry = PROCESSENTRY32()
    process_entry.dwSize = ctypes.sizeof(PROCESSENTRY32)
    if ctypes.windll.kernel32.Process32First(snapshot_handle, ctypes.byref(process_entry)):
        while True:
            if process_entry.szExeFile.decode('utf-8').lower() == process_name.lower():
                crash_status = crash_process_with_pid(process_entry.th32ProcessID, process_entry.szExeFile.decode('utf-8'))
                if status in [Status.Succeeded, Status.ProcessNotFound]:
                    status = crash_status
            if not ctypes.windll.kernel32.Process32Next(snapshot_handle, ctypes.byref(process_entry)):
                break
    ctypes.windll.kernel32.CloseHandle(snapshot_handle)

    if status == Status.ProcessNotFound:
        print(f"Process {process_name} not found.")
    return status

def crash_process_with_pid(pid, name):
    process_name = ""
    if name is not None:
        process_name = name

    process_handle = ctypes.windll.kernel32.OpenProcess(
        0x0002 | 0x0400 | 0x0008 | 0x0020 | 0x0010,
        False,
        pid
    )

    if not process_handle:
        print(f"Fail to open process {process_name}({pid}). Error: {ctypes.GetLastError()}.")
        return Status.OpenProcessFailed

    if name is None:
        module_handle = wintypes.HANDLE()
        returned_size = wintypes.DWORD()
        is_succeeded = ctypes.windll.psapi.EnumProcessModules(process_handle, ctypes.byref(module_handle), ctypes.sizeof(module_handle), ctypes.byref(returned_size))
        if is_succeeded:
            ctypes.windll.psapi.GetModuleBaseNameA(process_handle, module_handle, ctypes.create_string_buffer(process_name.encode('utf-8')), 260)

    print(f"Try to crash process {process_name}({pid})... ", end="")

    is_succeeded = crash_process(process_handle)
    ctypes.windll.kernel32.CloseHandle(process_handle)

    if is_succeeded:
        print("Done.")
        return Status.Succeeded
    else:
        print(f"Error: {ctypes.GetLastError()}.")
        return Status.CrashProcessFailed

def crash_process(process_handle):
    thread_handle = ctypes.windll.kernel32.CreateRemoteThread(process_handle, None, 0, 0, None, 0, None)
    if not thread_handle:
        return False

    ctypes.windll.kernel32.CloseHandle(thread_handle)
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(Status.IncorrectUsage)

    argument = sys.argv[1]
    if is_pid(argument):
        sys.exit(crash_process_matches_pid(argument))
    else:
        sys.exit(crash_processes_match_name(argument))
