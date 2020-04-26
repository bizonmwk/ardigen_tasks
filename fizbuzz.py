
def fizz_buzz(input_list):
    """
    Function for print as in instructions
    """
    for nmb in range(input_list[0],input_list[1]+1):
        if nmb % 3 == 0 and nmb % 5 == 0:
            print("FizzBuzz")
            continue
        elif nmb % 3 == 0:
            print("Fizz")
            continue
        elif nmb % 5 == 0:
            print("Buzz")
            continue
        print(nmb)

def checked_input():
    """
    Function for simple secured input,
    return user input in list
    """
    lst = []
    while True:
        try:
            lst.append(int(input()))
            lst.append(int(input()))
        except:
            continue
        if (lst[0] >= 1) & (lst[1] > lst[0]) & (lst[1] <= 10000):
            break
    return lst

if __name__ == "__main__":
    """
    Runs all functions
    """
    input_list = checked_input()
    fizz_buzz(input_list)
