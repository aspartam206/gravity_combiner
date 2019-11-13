import subprocess
import time
import os
import traceback

# combine file downloaded with GNU awk
def combine_list(src_path,output_path):
    system = subprocess.Popen([f"gawk '!seen[$0]++' {src_path} > {output_path}"],
                                # stdout=subprocess.PIPE,
                                # stderr=subprocess.PIPE,
                                universal_newlines=True, shell=True)
    return(system.communicate())

# remove commented line with sed
def clean_comments(src_path):
    system = subprocess.Popen([f"sed -i '/^[[:blank:]]*#/d;s/#.*//' {src_path}"],
                                # stdout=subprocess.PIPE,
                                # stderr=subprocess.PIPE,
                                universal_newlines=True, shell=True)
    return(system.communicate())

# sort the file with linux command
def sort_file(src_path,out_path):
    system = subprocess.Popen([f"sort {src_path} > {out_path}"],
                                # stdout=subprocess.PIPE,
                                # stderr=subprocess.PIPE,
                                universal_newlines=True, shell=True)
    return(system.communicate())
        
def remove_localhost(line):
    remove_list = set()
    remove_list.add("localhost")
    remove_list.add("localhost.localdomain")
    remove_list.add("local")
    remove_list.add("broadcasthost")
    remove_list.add("ip6-localhost")
    remove_list.add("ip6-loopback")
    remove_list.add("ip6-localnet")
    remove_list.add("ip6-mcastprefix")
    remove_list.add("ip6-allnodes")
    remove_list.add("ip6-allrouters")
    remove_list.add("ip6-allhosts")
    remove_list.add("0.0.0.0")
    
    sentences = line.split()       # split the line by whitespace
    if len(sentences) > 0:         # remove empty line
        line = sentences[-1]       # only get the {domain} part of the line
        line = line.lower()        # domain is case insensitive so lower it just incase.
        if not line in remove_list:
            return line
    
def clean_non_domain_data(path_file):  
    temp_file = f"{path_file}.tmp" 
    with open(temp_file,'w') as temp:
        with open(path_file, 'r', encoding="utf-8") as current_file: #ISO-8859-1
            for raw_line in current_file:
                # call remove_localhost to split the line and get only domain
                line = remove_localhost(raw_line)
                if line is not None:
                    # print(line)
                    temp.write(f"{line}\n") 
    os.replace(temp_file, path_file)

def snooze_for(how_much):
    start = time.time()
    time.sleep(how_much)
    return (time.time() - start)

def main():
    
    # init
    path_dwl      = os.path.join(f"{os.getcwd()}","dwl")
    text_files    = [f for f in os.listdir(path_dwl) if f.endswith('.txt')]
    gawk_src      = os.path.join(f"{os.getcwd()}","dwl","*.txt")
    gawk_output   = os.path.join(f"{os.getcwd()}","blocklist","unordered.txt")
    sort_output   = os.path.join(f"{os.getcwd()}","blocklist","ordered.txt")
    
    # loop through downloaded files for removing comments
    print("[Processing:  Cleaning Comments]")
    for i in range(len(text_files)):
        i+=1
        filename  = f"{i}.txt"
        src_path = f"dwl/{filename}"
        
        start = time.time()
        clean_comments(src_path)
        print(f"  Clean Comments took:   \t{(time.time() - start):.2f} seconds")       
    
    print(f"\nSleep for {snooze_for(2):.1f} sec \n")
    
    # loop through downloaded files for removing non domain
    print("[Processing:  Cleaning Non Domain]")
    for i in range(len(text_files)):
        i+=1
        filename  = f"{i}.txt"
        src_path = f"dwl/{filename}"
        
        start = time.time()
        clean_non_domain_data(src_path)
        print(f"  Domain Formatting took:\t{(time.time() - start):.2f} seconds")
    
    print(f"\nSleep for {snooze_for(2):.1f} sec \n")
    
    # remove duplicate and combine to one file
    print("[Processing:  Compiling]")
    start = time.time()
    combine_list(gawk_src, gawk_output)
    print(f"  Process took:     \t\t{(time.time() - start):.2f} seconds")
    
    print(f"\nSleep for {snooze_for(2):.1f} sec \n")
    
    # sort the output file
    print("[Processing:  Sorting]")
    start = time.time()
    sort_file(gawk_output, sort_output)
    print(f"  Process took:     \t\t{(time.time() - start):.2f} seconds")
    
    # remove unordered output
    os.remove(gawk_output)

if __name__ == "__main__":
    # try:
    #     # <<<=================== EXECUTE MAIN ===================>>>
    #     main()
    # except IOError:
    #     print('Error: Input / Output Error')
    # except ValueError:
    #     print('Error: Value Error')
    # except ImportError:
    #     print('Error: NO module found.')
    # except EOFError:
    #     print('Error: Why did you do an EOF on me?')
    # except KeyboardInterrupt:
    #     print('Error: You are cancelled LOL')
    # except:
    #     print('An error occured, and I don\'t know why')
    
    try:
        main()
    except Exception as e:
        print(e)
        traceback.print_exc()