import requests
import subprocess
import time
import os
    
# download and save(stream) response from url 
def download_blocklist(url,file_path,s):
    r = s.get(url,allow_redirects=True,stream=True)    
    with open(file_path, 'wb') as current_file:
            for chunk in r.iter_content(None):
                current_file.write(chunk)
    return file_path

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
def sort_linux(src_path,out_path):
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
    
    sentences = line.split()
    if len(sentences) > 0:
        line = sentences[-1]
        line = line.lower()
        if not line in remove_list:
            return line
    
def clean_non_domain_data(path_file):  
    temp_file = f"{path_file}.tmp" 
    with open(temp_file,'w') as temp:
        with open(path_file, 'r', encoding="ISO-8859-1") as current_file:
            for raw_line in current_file:
                # call remove_localhost to split the line and get only domain
                line = remove_localhost(raw_line)
                if line is not None:
                    # print(line)
                    temp.write(f"{line}\n") 
    os.replace(temp_file, path_file)
    
def main():
    # set of blocklist provider link
    block_sets = set()
    block_sets.add('https://blocklist.site/app/dl/ads')
    block_sets.add('https://blocklist.site/app/dl/spam')
    block_sets.add('https://blocklist.site/app/dl/scam')
    block_sets.add('https://blocklist.site/app/dl/crypto')
    block_sets.add('https://blocklist.site/app/dl/fraud')
    block_sets.add('https://blocklist.site/app/dl/malware')
    block_sets.add('https://blocklist.site/app/dl/ransomware')
    block_sets.add('https://blocklist.site/app/dl/tracking')
    block_sets.add('https://dbl.oisd.nl')
    block_sets.add('https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts')
    block_sets.add('https://mirror1.malwaredomains.com/files/justdomains')
    block_sets.add('http://sysctl.org/cameleon/hosts')
    block_sets.add('https://s3.amazonaws.com/lists.disconnect.me/simple_tracking.txt')
    block_sets.add('https://s3.amazonaws.com/lists.disconnect.me/simple_ad.txt')
    block_sets.add('https://hosts-file.net/ad_servers.txt')
    
    # init
    gawk_src      = os.path.join(f"{os.getcwd()}","dwl","*.txt")
    gawk_output   = os.path.join(f"{os.getcwd()}","blocklist","unordered.txt")
    sort_output   = os.path.join(f"{os.getcwd()}","blocklist","ordered.txt")
    
    ## DOWNLOAD CODE
    try:
        # init requests persistance connection
        session = requests.Session()
        session.headers.update({'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:69.0) Gecko/20100101 Firefox/69.0'})
        
        # loop through block_sets to download the blocklist
        index = 1
        print("[Download:  Starting]")
        for target_list in sorted(block_sets):
            print(f"  {target_list}", end="   ")
            filename   = f"{index}.txt"
            file_path  = f"dwl/{filename}"
            downloaded = download_blocklist(target_list,file_path,session)
            print(downloaded)
            index+=1
    finally:
        # close requests persistance connection
        session.close()
        # some housekeeping LOL
        del(index,filename,file_path,downloaded)
        print("[Download:  Finished]\n")
    
    ## PROCESSING CODE
    # loop through downloaded files for removing comments
    print("[Processing:  Cleaning Comments]")
    for i in range(len(block_sets)):
        i+=1
        start = time.time()
        filename  = f"{i}.txt"
        src_path = f"dwl/{filename}"
        clean_comments(src_path)
        clean_non_domain_data(src_path)
        print("  Process took: {:.2f} seconds".format(time.time() - start))        
    
    # remove duplicate and combine to one file
    print("[Processing:  Compiling]")
    start = time.time()
    combine_list(gawk_src, gawk_output)
    print("  Process took: {:.2f} seconds".format(time.time() - start))
    
    # sort the output file
    print("[Processing: Sorting]")
    start = time.time()
    sort_linux(gawk_output, sort_output)
    print("  Process took: {:.2f} seconds".format(time.time() - start))


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
    main()