from big_finish.process_product import *
from big_finish.get_products import *

s = process_product("releases/v/bernice-summerfield-oh-no-it-isn-t-8")
print(s)

t = process_product("releases/v/doctor-who-charlotte-pollard-the-further-adventuress-2500")
print(t)

u = process_product("releases/v/big-finish-podcast-2022-01-16-eighth-and-ninth-doctors-2612")
print(u)

ps = get_products()
print(ps)