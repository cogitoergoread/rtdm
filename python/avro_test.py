from avro.datafile import DataFileReader
from avro.io import DatumReader
from sys import argv

script, filename = argv
print("Filename to check:{}".format(filename))

reader = DataFileReader(open(filename, "rb"), DatumReader())
for user in reader:
    print(user)
reader.close()
