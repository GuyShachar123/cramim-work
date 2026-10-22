import win32api
import win32con
import win32security

def enable_debug_privilege():
    try:
        current_process = win32api.GetCurrentProcess()
        token = win32security.OpenProcessToken(current_process, win32con.TOKEN_ADJUST_PRIVILEGES | win32con.TOKEN_QUERY)
        luid = win32security.LookupPrivilegeValue(None, "SeDebugPrivilege")
        new_privileges = [(luid, win32security.SE_PRIVILEGE_ENABLED)]
        win32security.AdjustTokenPrivileges(token, False, new_privileges)
    except Exception as e:
        pass

def print_Privilege(pid):
    process = win32api.OpenProcess(
        win32con.PROCESS_QUERY_INFORMATION | win32con.TOKEN_ADJUST_PRIVILEGES,
        False,
        pid
    )
    token = win32security.OpenProcessToken(process, win32con.TOKEN_QUERY)
    privileges = win32security.GetTokenInformation( token, win32security.TokenPrivileges)
    flag_dic = {0:"Disabled", 1:"Enabled by Default",2:"Enabled ",3:"Default Enabled",4:"Removed "}
    print(f"{'Privilege':<40} {'Flags'}")
    for priv_luid, flags in privileges:
            try:
                priv_name = win32security.LookupPrivilegeName(None, priv_luid)
                print(f"{priv_name:<40} {flag_dic[flags]}")
            except Exception:
                continue


if __name__ == "__main__":
    enable_debug_privilege()
    while True:

        user_input = input("enter valid pid exit to exit")
        if user_input.lower() == "exit":
            print("Exiting...")
            break
        try:
            pid = int(user_input)
        except (ValueError, TypeError):
            continue
        if pid <0:
            continue


        try:
            process_handle = win32api.OpenProcess(   win32con.PROCESS_QUERY_INFORMATION,  False,pid    )
            token = win32security.OpenProcessToken(process_handle, win32con.TOKEN_ADJUST_PRIVILEGES | win32con.TOKEN_QUERY)
        except Exception as e:
            print(f"eroor{e}")
            continue
        print_Privilege(pid)

        privilege_name = input("enter privlage to change")
        privlage_flag = input("enter 0 for disable 1 for enable by defult 2 for enable 3 defult enable 4 disable")
        try:
            privlage_flag =int(privlage_flag)
        except Exception as e:
            continue

        #need to check for int valid and make it chosen privlage
        try:
            luid = win32security.LookupPrivilegeValue(None, privilege_name)
        except Exception as e:
            print("invalid privlage name ")
            continue
        new_privileges = [(luid, privlage_flag)]
        win32security.AdjustTokenPrivileges(token, False, new_privileges)
        print_Privilege(pid)

