
foxlang.class:
	javac -d ./build/ @sources.txt

run: foxlang.class
	cd build && java foxlang.Main

build: foxlang.class
	cd ./build/ && jar cvfe ../foxlang.jar foxlang.Main foxlang/*
	java -jar foxlang.jar

clean:
	$(RM) -r ./build/*

cr: run clean

clogs:
	$(RM) -r ./logs/
