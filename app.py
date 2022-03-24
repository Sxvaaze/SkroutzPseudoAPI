import main as skroutzapi
"""
          _____                    _____                    _____                   _______         
         /\    \                  /\    \                  /\    \                 /::\    \        
        /::\    \                /::\    \                /::\____\               /::::\    \       
       /::::\    \              /::::\    \              /::::|   |              /::::::\    \      
      /::::::\    \            /::::::\    \            /:::::|   |             /::::::::\    \     
     /:::/\:::\    \          /:::/\:::\    \          /::::::|   |            /:::/~~\:::\    \    
    /:::/  \:::\    \        /:::/__\:::\    \        /:::/|::|   |           /:::/    \:::\    \   
   /:::/    \:::\    \      /::::\   \:::\    \      /:::/ |::|   |          /:::/    / \:::\    \  
  /:::/    / \:::\    \    /::::::\   \:::\    \    /:::/  |::|___|______   /:::/____/   \:::\____\ 
 /:::/    /   \:::\ ___\  /:::/\:::\   \:::\    \  /:::/   |::::::::\    \ |:::|    |     |:::|    |
/:::/____/     \:::|    |/:::/__\:::\   \:::\____\/:::/    |:::::::::\____\|:::|____|     |:::|    |
\:::\    \     /:::|____|\:::\   \:::\   \::/    /\::/    / ~~~~~/:::/    / \:::\    \   /:::/    / 
 \:::\    \   /:::/    /  \:::\   \:::\   \/____/  \/____/      /:::/    /   \:::\    \ /:::/    /  
  \:::\    \ /:::/    /    \:::\   \:::\    \                  /:::/    /     \:::\    /:::/    /   
   \:::\    /:::/    /      \:::\   \:::\____\                /:::/    /       \:::\__/:::/    /    
    \:::\  /:::/    /        \:::\   \::/    /               /:::/    /         \::::::::/    /     
     \:::\/:::/    /          \:::\   \/____/               /:::/    /           \::::::/    /      
      \::::::/    /            \:::\    \                  /:::/    /             \::::/    /       
       \::::/    /              \:::\____\                /:::/    /               \::/____/        
        \::/____/                \::/    /                \::/    /                 ~~              
         ~~                       \/____/                  \/____/            

                            SkroutzPseudo API V1.0.1 by github.com/Sxvaaze
"""

#If link is empty or not a valid skroutz product url (does not contain "skroutz.gr/s/") then all api calls will return an error defined by function filter_input in main.py
link = input("Give url: ")

#Demo 1 (API request for an item's data with no show_all & no limit)
#Returns base data and info of first store
res1 = skroutzapi.call(link)

#Demo 2 (API request for an item with show_all & no limit (Returns data from ALL STORES))
#Returns base data and info for all stores 
res2 = skroutzapi.call(link, show_all=True)

#Demo 3 (API request for an item with show_all & a limit (Returns ALL STORES if store_count <= limit, else returns data from up to << LIMIT >> stores))
#Returns base data and info for up to << limit >> stores
res3 = skroutzapi.call(link, show_all=True, limit=6)

print(res1)
print('-' * 100)
print(res2)
print('-' * 100)
print(res3)
