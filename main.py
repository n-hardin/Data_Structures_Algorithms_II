# Data Structures and Algorithms II - C950 Performance Assessment
# Name: Nicolas Hardin
# Student ID: 010451473

# Import necessary modules
import csv
import datetime


# CustomHashTable class for implementing a hash table using chaining
# C950 - Webinar-1 - Let’s Go Hashing
# W-1_ChainingHashTable_zyBooks_Key-Value.py
# Ref: zyBooks: Figure 7.8.2: Hash table using chaining.
# Modified for Key:Value
class CustomHashTable:

    def __init__(self, initial_capacity=10):
        # Initialize the hash table as a list of buckets
        self.table = []
        for index in range(initial_capacity):
            self.table.append([])

    # Method to insert an entry into the hash table
    def insert_entry(self, key, item):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        # Check if the key already exists, update the item if found
        for kv_pair in bucket_list:
            if kv_pair[0] == key:
                kv_pair[1] = item
                return True

        # If the key does not exist, add a new key-value pair to the bucket
        key_value = [key, item]
        bucket_list.append(key_value)
        return True

    # Method to search for an entry in the hash table by key
    def search_entry(self, key):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        # Search for the key and return the corresponding item if found
        for key_value in bucket_list:
            if key_value[0] == key:
                return key_value[1]
        return None

    # Method to remove an entry from the hash table by key
    def remove_entry(self, key):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        # Search for the key and remove the corresponding key-value pair
        for kv_pair in bucket_list:
            if kv_pair[0] == key:
                bucket_list.remove([kv_pair[0], kv_pair[1]])


# CustomPackage class for representing package information
class CustomPackage:

    # Initialize package attributes
    def __init__(self, package_id, address, city, state, postal, deadline, weight, note, status, delivery_time):
        self.package_id = package_id
        self.address = address
        self.city = city
        self.state = state
        self.postal = postal
        self.deadline = deadline
        self.weight = weight
        self.note = note
        self.status = status
        self.delivery_time = delivery_time

    # Method to represent the package information as a string
    def __str__(self):
        return ("ID: %s, Address: %s, City: %s, State: %s, Postal: %s, Deadline: %s, Weight: %s, Note: %s, "
                "Status: %s, Delivery Time: %s") % (
            self.package_id, self.address, self.city, self.state,
            self.postal, self.deadline, self.weight, self.note, self.status,
            self.delivery_time)

    # Method to check the delivery status based on the given time
    def check_delivery_status(self, time):
        if self.delivery_time <= time:
            self.status = "Delivered"
        elif self.delivery_time > time:
            self.status = "En route"
        else:
            self.status = "At the hub"
        # Special case for package 9 with incorrect address, update address details after new address is received
        if self.package_id == 9:
            if time >= datetime.timedelta(hours=10, minutes=20):
                self.address = "410 S. State St."
                self.city = "Salt Lake City"
                self.state = "UT"
                self.postal = "84111"


# CustomTruck class for representing truck information
class CustomTruck:

    # Initialize truck attributes
    def __init__(self, capacity, speed, packages, location, distance_traveled, depart_time):
        self.capacity = capacity
        self.speed = speed
        self.packages = packages
        self.location = location
        self.distance_traveled = distance_traveled
        self.depart_time = depart_time

    # Method to represent the truck information as a string
    def __str__(self):
        return "Capacity: %s, Speed: %s, Packages: %s, Location: %s, Distance Traveled: %s, Departure Time: %s" % (
            self.capacity, self.speed, self.packages, self.location, self.distance_traveled, self.depart_time)


# Create a hash table for packages
package_hash = CustomHashTable()


# Method to return package information from ID
def lookup_package(package_id):
    package = package_hash.search_entry(package_id)
    return package


# Method to load data from a CSV file
def load_data(file_name):
    with open(file_name) as data_file:
        data = csv.reader(data_file, delimiter=',')
        return list(data)
        

# Method to calculate the distance between two addresses based on the given distances data
def calculate_distance(address_x, address_y, distances_data):
    distance_value = distances_data[address_x][address_y]
    if distance_value == '':
        distance_value = distances_data[address_y][address_x]
    return float(distance_value)


# Method to find a usable address ID based on a given address
def get_usable_address(address, addresses_data):
    for row in addresses_data:
        if address in row[2]:
            return int(row[0])


# Method to load truck data and create a CustomTruck object
def load_truck(truck_data):
    return CustomTruck(truck_data[0], truck_data[1], truck_data[2], truck_data[3], truck_data[4], truck_data[5])


# Method to deliver packages
def deliver_packages(truck, distances_data, addresses_data):
    remaining_packages = []
    for package_id in truck.packages:
        remaining_packages.append(lookup_package(package_id))
    truck.packages.clear()
    while len(remaining_packages) > 0:
        next_address = 1000
        next_package = None
        for package in remaining_packages:
            if calculate_distance(get_usable_address(truck.location, addresses_data),
                                  get_usable_address(package.address, addresses_data), distances_data) <= next_address:
                next_address = calculate_distance(get_usable_address(truck.location, addresses_data),
                                                  get_usable_address(package.address, addresses_data), distances_data)
                next_package = package

        if next_package:
            truck.packages.append(next_package.package_id)
            remaining_packages.remove(next_package)
            truck.distance_traveled += next_address
            truck.location = next_package.address
            truck.depart_time += datetime.timedelta(hours=next_address / 18)  # Time/speed (18 mph truck speed)
            next_package.delivery_time = truck.depart_time


# Main method
def main():
    # Load data from CSV files
    package_data = load_data('PackageCSV.csv')
    distances_data = load_data('DistancesCSV.csv')
    addresses_data = load_data('AddressesCSV.csv')

    # Populate the hash table with package data
    for package_info in package_data:
        package_id = int(package_info[0])
        address = package_info[1]
        city = package_info[2]
        state = package_info[3]
        postal = package_info[4]
        deadline = package_info[5]
        weight = package_info[6]
        note = package_info[7]
        status = None
        delivery_time = None

        package_object = CustomPackage(
            package_id, address, city, state, postal, deadline, weight, note, status, delivery_time)
        package_hash.insert_entry(package_id, package_object)

    truck1_data = [16, 18, [1, 4, 13, 14, 15, 16, 19, 20, 21, 29, 30, 31, 34, 37, 39, 40],
                   "4001 South 700 East", 0.0, datetime.timedelta(hours=8)]

    truck2_data = [16, 18, [3, 5, 8, 9, 10, 11, 12, 18, 23, 27, 35, 36, 38],
                   "4001 South 700 East", 0.0, datetime.timedelta(hours=10, minutes=20)]

    truck3_data = [16, 18, [2, 6, 7, 17, 22, 24, 25, 26, 28, 32, 33],
                   "4001 South 700 East", 0.0, datetime.timedelta(hours=9, minutes=5)]

    truck1 = load_truck(truck1_data)
    truck2 = load_truck(truck2_data)
    truck3 = load_truck(truck3_data)

    deliver_packages(truck1, distances_data, addresses_data)
    deliver_packages(truck3, distances_data, addresses_data)

    # Only 2 drivers, so one truck must return before the 3rd can depart, but truck 2 won't have the correct address
    # until 10:20 AM
    truck2.depart_time = min(truck1.depart_time, truck3.depart_time)
    if truck2.depart_time < datetime.timedelta(hours=10, minutes=20):
        truck2.depart_time = datetime.timedelta(hours=10, minutes=20)
    deliver_packages(truck2, distances_data, addresses_data)

    # Take user input for time and convert it to usable format
    time_selection = input("At what time would you like to view the status of packages? Please enter HH:MM ")
    (hours_input, minutes_input) = time_selection.split(":")
    time = datetime.timedelta(hours=int(hours_input), minutes=int(minutes_input))

    # Print trucks and the packages inside, as well as the status of the packages at the inputted time
    # TRUCK 1
    print("\nTRUCK 1 PACKAGES: \n")
    for package_id in truck1.packages:
        package = package_hash.search_entry(package_id)
        package.check_delivery_status(time)
        print(str(package))

    # TRUCK 2
    print("\nTRUCK 2 PACKAGES: \n")
    for package_id in truck2.packages:
        package = package_hash.search_entry(package_id)
        package.check_delivery_status(time)
        print(str(package))

    # TRUCK 3
    print("\nTRUCK 3 PACKAGES: \n")
    for package_id in truck3.packages:
        package = package_hash.search_entry(package_id)
        package.check_delivery_status(time)
        print(str(package))

    # Print total mileage of all trucks
    print("\nTOTAL TRUCK MILEAGE: " + str(
        int(truck1.distance_traveled + truck2.distance_traveled + truck3.distance_traveled)) + " miles")


# Run main method
main()
