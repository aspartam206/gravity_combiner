import requests

class Download_Block:
    # download and save(stream) response from url 
    def dwl(self,url,file_path):
        r = requests.get(url,allow_redirects=True,stream=True)    
        with open(file_path, 'wb') as curr_file:
                for chunk in r.iter_content(None):
                    curr_file.write(chunk)
        return file_path
    
    # combine two set
    def combine_set(self, set_a, set_b):
        return set_a.union(set_b)
    
    # read file download from dwl()
    def read_file(self,path_file):
        z      = open(path_file, 'r', encoding='ISO-8859-1')
        z_list = [line.strip() for line in z if not line.startswith('#')]
        # convert to set() for easy remove the duplicate
        z_set = set(z_list)
        return z_set

if __name__ == "__main__":
    
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
    
    # init
    __dwlclass    = Download_Block()
    outfile = open('block.txt', 'w')
    final_set = set()
    index = 1
    
    # loop through block_sets to download the blocklist
    for target_list in block_sets:
        filename   = f"{index}.txt"
        file_path  = f"dwl/{filename}"
        downloaded = __dwlclass.dwl(target_list,file_path)
        print(downloaded)
        index+=1
    
    # loop through downloaded files for removing duplicates
    for i in range(len(block_sets)):
        i+=1
        filename  = f"{i}.txt"
        file_path = f"dwl/{filename}"
        file_set  = __dwlclass.read_file(file_path)
        final_set = __dwlclass.combine_set(final_set,file_set)
    
    final_set = sorted(final_set)
    outfile.write('\n'.join(final_set))
    print(len(final_set))
    