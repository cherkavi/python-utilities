import sys

def add_to_stripe(stripe, letter):
    if letter in stripe:
        stripe[letter] = stripe[letter] + 1
    else:
        stripe[letter] = 1

def flat_stripe(stripe):
    return ",".join([ key+":"+str(value) for key,value in stripe.items()])

def print_stripe(letter, stripe):
    print(letter + "\t"+flat_stripe(stripe))

def print_outer_join(values):
    for i in range(len(values)):
        stripe = dict()
        for j in range(len(values)):
            if i!=j and values[i]!=values[j]:
                add_to_stripe(stripe, values[j])
        print_stripe(values[i], stripe)

def main():
    for each_line in sys.stdin:
        words = each_line.strip().split(" ")
        print_outer_join(words)

if __name__ == '__main__':
    main()