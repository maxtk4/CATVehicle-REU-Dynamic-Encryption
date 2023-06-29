import csv

filea = 'sample-data-a.csv'
fileb = 'sample-data-b.csv'

#maps the classes that we are looking at into consecutive numbers
class_numbers = {1: 1, 2: 2, 3: 3, 5: 4, 7: 5}

def read_numbers(filename: str):
    """
    Reads in the data from a csv file formatted as t1, t2, class
    Returns a list of lists
    """
    data = []
    with open(filename, newline='\n') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        data = [row for row in reader]

    return data

def convert_timestamp(time: int):
    """
    Takes a unix timestamp and converts it into a byte, takes the timestamp mod 256
    """
    return '{0:08b}'.format(time % 256)

def create_data_stream(source: str):
    """
    Convert a new file into a data stream of bits
    """

    #empty variable to hold the data stream of bits we will get
    data_stream = ''

    for event in read_numbers(source):
        #uses the convert_timestamp function to convert the 8 least significant bits from each timestamp into a byte
        time_data = convert_timestamp(int(event[0])) + convert_timestamp(int(event[1]))
        #uses the class_numbers map to convert classes into smaller numbers and then binary
        class_data = '{0:03b}'.format(class_numbers[int(event[2])])

        #concatenate the data
        event_data = time_data + class_data
        data_stream += event_data
    
    return data_stream
    
stream_a = create_data_stream(filea)
stream_b = create_data_stream(fileb)


print(f'Length of stream a: {len(stream_a)}')
print(f'Length of stream b: {len(stream_b)}')
print(f'Stream a: {stream_a}')
print(f'Stream b: {stream_b}')
