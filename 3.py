
        
def main():
    atupe = []
    for num in range(1,200):
        if num%3 == 0 or "3" in str(num):
            atupe.append(num)
    return atupe
 
if __name__ == "__main__":
    print main()
