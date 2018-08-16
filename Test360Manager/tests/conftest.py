import pytest
import os.path

def pytest_runtest_makereport(item, call):
    if "incremental" in item.keywords:
        if call.excinfo is not None:
            parent = item.parent
            parent._previousfailed = item


def pytest_runtest_setup(item):
    if "incremental" in item.keywords:
        previousfailed = getattr(item.parent, "_previousfailed", None)
        if previousfailed is not None:
            pytest.xfail("previous test failed (%s)" % previousfailed.name)


def fill_new_customers(used_count):
    with open(os.path.abspath("data/new_customer.txt"), 'r+') as f:
        capacity = used_count + 31
        f.write(str(used_count) + "\n")
        for i in range(used_count+1, capacity):
            f.write("test_customer_" + str(i) + " " + "test_folder_" + str(i) + "\n")
        f.truncate()


@pytest.fixture()
def getNewCustomer():
    with open(os.path.abspath("data/new_customer.txt"), 'r+') as f:
        used_count = f.readline().strip()
        next_customer = f.readline().strip()

        try:
            used_count = int(used_count)
        except ValueError:
            used_count = 0
            f.seek(0)

        if next_customer == '':
            fill_new_customers(used_count)
            temp = f.readline()
            if temp.strip() == "" or temp.strip() == "0":
                temp = f.readline()
            next_customer = temp

        pending_customers = f.readlines()
        print(pending_customers)
        f.seek(0)
        f.write(str(used_count+1) + "\n")
        f.writelines(pending_customers)
        f.truncate()

    return next_customer.split(" ")
