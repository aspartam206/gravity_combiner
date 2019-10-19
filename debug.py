import os

path_file = "dwl/13.txt"
def clean_localhost(line):
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
    
    sentences = line.split()
    if len(sentences) > 0:
        line = sentences[-1]
        line = line.lower()
        if not line in remove_list:
            return line


temp_file = f"{path_file}.tmp" 
with open(temp_file,'w') as temp:
    with open(path_file, 'r') as current_file:
        for raw_line in current_file:
            # split the line and get only domain
            line = clean_localhost(raw_line)
            if line is not None:
                temp.write(f"{line}\n") 
os.replace(temp_file, path_file)
