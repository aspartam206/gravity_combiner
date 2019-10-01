import requests

class Download_Block:
    def dwl(self,url):
        block_dwl = requests.get(url)
        return block_dwl.text
    def combine_set(self, set_a, set_b):
        return set_a.union(set_b)

if __name__ == "__main__":
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
    
    __dwlclass    = Download_Block()
    final_set = set()
    outfile = open('block.txt', 'w')
    
    for target_list in block_sets:
        downloaded = __dwlclass.dwl(target_list).split()
        set_dwl    = set(downloaded)
        del downloaded
        
        final_set = __dwlclass.combine_set(final_set,set_dwl)
    
    final_set = sorted(final_set)
    outfile.write('\n'.join(final_set))
    print(len(final_set))