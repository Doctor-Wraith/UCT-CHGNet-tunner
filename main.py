import data_extracter as ode
import json

def get_data_test():
    data = ode.processe_data("./data/New_opt_p3x3", True)
    with open("./data/test_out.json", 'w') as file:
        file.write(json.dumps(data, indent=2))

def main():
    get_data_test()

if __name__ == "__main__": main()