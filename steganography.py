from PIL import Image # Library for image handling

def genData(data): # Function to convert encoding data into 8-bit binary form
    newdata = []
    for i in data:
        newdata.append(format(ord(i), "08b"))
    return newdata

def modifyPixels(pix, data): # Function for modifying pixels accoding to 8-bit binary data 
    datalist = genData(data)
    lendata = len(datalist)
    imgdata = iter(pix)

    for i in range(lendata):
        pix = [value for value in next(imgdata)[:3] +
                                next(imgdata)[:3] +
                                next(imgdata)[:3]]

        for j in range(0, 8):
            if (datalist[i][j] == '0' and pix[j] % 2 != 0):
                pix[j] -= 1
            elif (datalist[i][j] == '1' and pix[j] % 2 == 0):
                if pix[j] != 0:
                    pix[j] -= 1
                else:
                    pix[j] += 1

        if (i == lendata - 1):
            if (pix[-1] % 2 == 0):
                if pix[-1] != 0:
                    pix[-1] -= 1
                else:
                    pix[-1] += 1
        else:
            if (pix[-1] % 2 != 0):
                pix[-1] -= 1

        pix = tuple(pix)
        yield pix[0:3]
        yield pix[3:6]
        yield pix[6:9]

def encrypt(data, shift): # Function for encrypting the message that is to be hidden in the input image
    encrypted_data=""
    for char in data:
        if char.isalpha():
            ascii_offset = ord('a') if char.islower() else ord('A')
            encrypted_char = chr((ord(char)-ascii_offset+shift)%26 + ascii_offset)
            encrypted_data+=encrypted_char
        else:
            encrypted_data+=char
    return encrypted_data
            
def decrypt(data, shift): # Function for decrypting the message that is hidden in the input image
    decrypted_data=""
    for char in data:
        if char.isalpha():
            ascii_offset = ord('a') if char.islower() else ord('A')
            decrypted_char = chr((ord(char)-ascii_offset-shift)%26 + ascii_offset)
            decrypted_data+=decrypted_char
        else:
            decrypted_data+=char
    
    return decrypted_data


def encode_enc(newimg, data): # Function for keeping the modified pixels into the image
    w = newimg.size[0]
    (x, y) = (0, 0)

    for pixel in modifyPixels(newimg.getdata(), data):
        newimg.putpixel((x, y), pixel)
        if (x == w - 1):
            x = 0
            y += 1
        else:
            x += 1

def encode(): # Function for hiding the message in the input image
    img = input("Enter image name (with extension): ")
    try:
        image = Image.open(img, 'r')
    except FileNotFoundError:
        print(f"Error: File {img} not found.")
        return
    except IOError:
        print("Error: Cannot open image.")
        return

    data = input("Enter data to be encoded: ")
    enc_data=encrypt(data, 3)
    if len(enc_data) == 0:
        raise ValueError('Data is empty')

    # Convert image to PNG format internally
    if image.format != 'PNG':
        image = image.convert('RGBA')  # Ensures transparency is handled
        img = img.split('.')[0] + '.png'
    
    newimg = image.copy()
    encode_enc(newimg, enc_data)

    new_img_name = input("Enter the name of new image (with extension): ")
    newimg.save(new_img_name, 'PNG')

def decode(): # Function for finding the message that is hidden in the image
    img = input("Enter image name (with extension): ")
    try:
        image = Image.open(img, 'r')
    except FileNotFoundError:
        print(f"Error: File {img} not found.")
        return ""
    except IOError:
        print("Error: Cannot open image.")
        return ""

    # Convert image to PNG format internally
    if image.format != 'PNG':
        image = image.convert('RGBA')  # Ensures transparency is handled
        img = img.split('.')[0] + '.png'

    data = ''
    imgdata = iter(image.getdata())

    while True:
        pixels = [value for value in next(imgdata)[:3] +
                                next(imgdata)[:3] +
                                next(imgdata)[:3]]

        binstr = ''

        for i in pixels[:8]:
            if i % 2 == 0:
                binstr += '0'
            else:
                binstr += '1'

        data += chr(int(binstr, 2))
        dec_data = decrypt(data,3)
        if pixels[-1] % 2 != 0:
            return dec_data

def main(): # Driver Code
    while True:
        try:
            a = int(input(":: Welcome ::\n1. Encode\n2. Decode\n3. Exit\n"))
            if a == 1:
                encode()
            elif a == 2:
                decoded_message = decode()
                if decoded_message:
                    print("Decoded word: " + decoded_message)
            elif a == 3:
                print("Exiting...")
                break
            else:
                print("Enter correct input")
        except ValueError:
            print("Invalid input, please enter a number.")

main()