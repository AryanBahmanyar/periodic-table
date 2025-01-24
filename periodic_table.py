"""
Displays atomic information for all the elements.
More info at: https://en.wikipedia.org/wiki/List_of_chemical_elements
"""
import csv, os, sys, re


def get_elements():
    """Returns a dictionary of elements"""
    elements = {}
    
    with open(CSV_FILE_PATH, encoding='utf-8') as file:
        reader = csv.reader(file)
        entries = list(reader)
        
    for field in entries:
        element = {}
        
        for i, attr in enumerate(ATTRIBUTES):
            element[attr] = field[i]
            
            if i not in [6, 7, 8, 9, 10, 12]:
                continue
            match i:
                case 6:
                    element[attr] += ' u'  # atomic mass unit
                case 7:
                    element[attr] += ' g/cm^3'  # grams/cubic cm
                case 8, 9:
                    element[attr] += ' K'  # kelvin
                case 10:
                    element[attr] += ' J/(g*K)'
                case 12:
                    element[attr] += ' mg/kg'
                    
        # remove the Roman numerals
        for k, v in element.items():
            element[k] = re.sub(r'\[(I|V|X)+\]', '', v)
            
        # map tuple of symbol and name to element
        elements[(field[1].lower(), field[2].lower())] = element
        
    return elements


def print_table():
    """Print the periodic table"""
    
    print(''' Periodic Table of Elements
  1  2  3  4  5  6  7  8  9  10 11 12 13 14 15 16 17 18
1 H                                                  He
2 Li Be                               B  C  N  O  F  Ne
3 Na Mg                               Al Si P  S  Cl Ar
4 K  Ca Sc Ti V  Cr Mn Fe Co Ni Cu Zn Ga Ge As Se Br Kr
5 Rb Sr Y  Zr Nb Mo Tc Ru Rh Pd Ag Cd In Sn Sb Te I  Xe
6 Cs Ba La Hf Ta W  Re Os Ir Pt Au Hg Tl Pb Bi Po At Rn
7 Fr Ra Ac Rf Db Sg Bh Hs Mt Ds Rg Cn Nh Fl Mc Lv Ts Og
''')


def print_element(name_or_symbol):
    """Print element's information"""
    
    # determine if string is element's symbol or full name
    symbol = len(name_or_symbol) <= 2
    
    for k, v in elements.items():
        if (symbol and k[0] == name_or_symbol) or (not symbol and k[1] == name_or_symbol):
            for attr in ATTRIBUTES:
                print(attr.rjust(longest_col) + ': ' + elements[k][attr])
            break
    print()
    input('Press Enter to continue...')
    print()


if __name__ == '__main__':
    ABS_DIR_PATH = os.path.dirname(os.path.abspath(__file__))
    CSV_FILE_PATH = os.path.join(ABS_DIR_PATH, 'periodic_table.csv')
    ATTRIBUTES = [
        'Atomic Number', 'Symbol', 'Element', 'Origin of Name', 'Group',
        'Period', 'Atomic Weight', 'Density', 'Melting Point', 'Boiling Point',
        'Specific Heat Capacity', 'Electronegativity', 'Abundance in Earth\'s Crust'
    ]
    # find the longest column for aligning / justifying text
    longest_col = 0
    
    for attr in ATTRIBUTES:
        if len(attr) > longest_col:
            longest_col = len(attr)
    try:
        elements = get_elements()
        print('Periodic Table of Elements', end='\n\n')
        
        symbols = [key[0] for key in elements.keys()]
        names = [key[1] for key in elements.keys()]
        
        while True:
            print_table()
            print('Enter an element\'s symbol or full name to examine it (or (Q)uit):')
            
            while True:
                response = input('> ').strip().lower()
                
                if response in ['q', 'quit']:
                    sys.exit(0)
                if response in symbols or response in names:
                    print_element(response)
                    break
                print('Invalid input')
                
    except KeyboardInterrupt:
        sys.exit(0)
