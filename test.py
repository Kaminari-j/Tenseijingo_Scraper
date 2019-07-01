class TestClass:
	@staticmethod
	def TestMethod():
		print('TestMethod called')
		
class TestMethod2:
	@staticmethod
	def main(methodname:str):
		locals[methodname]()

if __name__ == '__main__':
	TestMethod2.main('TestClass.TestMethod')
