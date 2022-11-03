from jmshow import show

obj = dict(
	teste1 = dict(
		in1 = dict (
			list = [0,1,2,3],
			str = 'lwrgh sth ryjth ryj dyj srj sr hiugrsdh iuarh uzsdhg lhzsdg'
		),
	),
	teste2 = dict(ok = 'ok')
)

def aaa(x, y, z): ...

from teste import Base
bbb = Base()

ccc = {'mmm', 'nnn', 9, 888}
ddd = set([1, 2, 3, 2])

from datetime import datetime
import pytz
eee = datetime.now(pytz.timezone('America/Sao_Paulo')).strftime("%Y-%m-%d %H:%M:%S%z")
fff = datetime.now(pytz.timezone('America/New_York')).strftime("%Y-%m-%d %H:%M:%S%z")

# show(obj, 'teste', 99, (2,5), aaa, Base, bbb, bbb.as_dict, ccc, eee, fff, id="Teste do Jorge")
# show('teste', 99, (33,77))
show(bbb, bbb.as_dict, id=bbb.__name__())
