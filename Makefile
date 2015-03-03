

all:
	cd ./hash && python setup.py build -b build && cd ..
	find ./hash/build -name "hashModule.so" -exec mv {} ./signature \;
clean:
	cd ./hash && python setup.py clean && cd ..
	rm -rf ./hash/build
	rm -f ./signature/hashModule.so
