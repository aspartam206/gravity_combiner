import requests
import subprocess
import time
import os

class Download_Block:
    
    # download and save(stream) response from url 
    def dwl(self,url,file_path):
        global s
        r = s.get(url,allow_redirects=True,stream=True)    
        with open(file_path, 'wb') as curr_file:
                for chunk in r.iter_content(None):
                    curr_file.write(chunk)
        return file_path
    
    # subprocess with GNU awk
    def gawk(self,src_path,output_path):
        system = subprocess.Popen([f"gawk '!seen[$0]++' {src_path} > {output_path}"],
                                    # stdout=subprocess.PIPE,
                                    # stderr=subprocess.PIPE,
                                    universal_newlines=True, shell=True)
        return(system.communicate())
    
    # remove commented line with sed
    def remove_comment(self,src_path):
        system = subprocess.Popen([f"sed -i '/^[[:blank:]]*#/d;s/#.*//' {src_path}"],
                                    # stdout=subprocess.PIPE,
                                    # stderr=subprocess.PIPE,
                                    universal_newlines=True, shell=True)
        return(system.communicate())
    
    # sort the file with linux command
    def sort_linux(self,src_path,out_path):
        system = subprocess.Popen([f"sort {src_path} > {out_path}"],
                                    # stdout=subprocess.PIPE,
                                    # stderr=subprocess.PIPE,
                                    universal_newlines=True, shell=True)
        return(system.communicate())

if __name__ == "__main__":
    # init requests persistance connection
    s = requests.Session()
    s.headers.update({'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:69.0) Gecko/20100101 Firefox/69.0'})
    
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
    __dwlclass    = Download_Block()
    final_set     = set()
    gawk_src      = os.path.join(f"{os.getcwd()}","dwl","*.txt")
    gawk_output   = os.path.join(f"{os.getcwd()}","gawk.txt")
    sort_output   = os.path.join(f"{os.getcwd()}","sort.txt")
    index         = 1
    
    # loop through block_sets to download the blocklist
    for target_list in sorted(block_sets):
        print(target_list, end="   ")
        filename   = f"{index}.txt"
        file_path  = f"dwl/{filename}"
        downloaded = __dwlclass.dwl(target_list,file_path)
        print(downloaded)
        index+=1
    
    # close requests persistance connection
    s.close()
    
    # loop through downloaded files for removing comments
    print("[Exec     : sed]")
    for i in range(len(block_sets)):
        i+=1
        start = time.time()
        filename  = f"{i}.txt"
        src_path = f"dwl/{filename}"
        # out_path = f"sed/{filename}"
        __dwlclass.remove_comment(src_path)
        print("Process took: {:.2f} seconds".format(time.time() - start))
    
    # remove duplicate and combine to one file
    print("[Exec     : gawk]")
    start = time.time()
    __dwlclass.gawk(gawk_src, gawk_output)
    print("Process took: {:.2f} seconds".format(time.time() - start))
    
    # sort the output file
    print("[Exec     : sort]")
    start = time.time()
    __dwlclass.sort_linux(gawk_output, sort_output)
    print("Process took: {:.2f} seconds".format(time.time() - start))
    