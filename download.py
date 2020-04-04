import requests
import subprocess
import time
import os
    
# download and save(stream) response from url 
def download_blocklist(url,file_path,s):
    r = s.get(url,allow_redirects=True,stream=True)
    if r.encoding is None:
        r.encoding = 'utf-8'    
    with open(file_path, 'w', encoding="utf-8") as current_file:
            for chunk in r.iter_content(chunk_size=None, decode_unicode=True):
                current_file.write(chunk)
    return r.status_code

def main():
    # set of blocklist provider link
    block_sets = set()
    
    # Default Pi-hole List
    block_sets.add('https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts')
    block_sets.add('https://mirror1.malwaredomains.com/files/justdomains')
    block_sets.add('http://sysctl.org/cameleon/hosts')
    block_sets.add('https://s3.amazonaws.com/lists.disconnect.me/simple_tracking.txt')
    block_sets.add('https://s3.amazonaws.com/lists.disconnect.me/simple_ad.txt')
    block_sets.add('https://hosts-file.net/ad_servers.txt')
    
    # the Block List Project
    block_sets.add('https://blocklist.site/app/dl/ads')
    block_sets.add('https://blocklist.site/app/dl/spam')
    block_sets.add('https://blocklist.site/app/dl/scam')
    block_sets.add('https://blocklist.site/app/dl/crypto')
    block_sets.add('https://blocklist.site/app/dl/fraud')
    block_sets.add('https://blocklist.site/app/dl/malware')
    block_sets.add('https://blocklist.site/app/dl/ransomware')
    block_sets.add('https://blocklist.site/app/dl/tracking')
    
    # dbl.oisd.nl | Internet's #1 domain blocklist
    block_sets.add('https://dbl.oisd.nl')
    
    # firebog list
    
    r =  requests.get('https://v.firebog.net/hosts/lists.php?type=tick')
    
    for eLine in r.iter_lines(decode_unicode=True):
        if eLine:
            block_sets.add(eLine)
    
    # for target in sorted(block_sets):
    #     print(target)
    
    ## DOWNLOAD CODE
    try:
        # init requests persistance connection
        session = requests.Session()
        session.headers.update({'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:69.0) Gecko/20100101 Firefox/69.0'})
        
        # loop through block_sets to download the blocklist
        index = 1
        print("[Download:  Starting]")
        for target_list in sorted(block_sets):
            start = time.time()
            filename   = f"{index}.txt"
            file_path  = f"dwl/{filename}"
            print(f"  {file_path}", end="\t")
            downloaded = download_blocklist(target_list,file_path,session)
            print(f"  {downloaded}  {(time.time() - start):.2f} sec  \t {target_list}")
            index+=1
    finally:
        # close requests persistance connection
        session.close()
        # some housekeeping LOL
        del(index,filename,file_path,downloaded)
        print("[Download:  Finished]\n")

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