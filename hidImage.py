from PIL import Image
import stepic
import os
os.chdir(r"C:\Users\talmid\Downloads")


# encryption
def m1_encrypt_image (image,data):
    """

    :param image:
    :param data:
    :return none:
    """
    im = Image.open(image)
    im1 = stepic.encode(im, data.encode())
    im1.save('encoded_' + image)
    #im.show()
    #im1.show()


def m1_decrypt_img(image):
    """

    :param image:
    :return the decrypted msg:
    """
    im = Image.open(image)
    s = stepic.decode(im)
    return s

def m2_encrypt_image (image,data):
    """

    :param image:
    :param data:
    :return none what it does it emcrypt the file with m2 method:
    """
    with open(image, "rb") as f:
        header, pixels = f.read(54), f.read()

    w = int.from_bytes(header[18:22], "little")
    row_padded = ((w * 3 + 3) // 4) * 4
    pad_size = row_padded - (w * 3)

    payload = len(data).to_bytes(4, "big") + data.encode()
    new_px, p_idx = bytearray(), 0

    for i in range(0, len(pixels), row_padded):
        row = bytearray(pixels[i: i + row_padded])
        for j in range(w * 3, row_padded):
            if p_idx < len(payload):
                row[j] = payload[p_idx]
                p_idx += 1
        new_px.extend(row)

    with open("m2_" + image, "wb") as f:
        f.write(header + new_px)
    print("M2: File size unchanged.")


def m2_decrypt_img(image):
    """
    :param image:
    :return none what it does it decrypt the file with m2 method:
    """
    with open(image, "rb") as f:
        header, pixels = f.read(54), f.read()

    w = int.from_bytes(header[18:22], "little")
    row_padded = ((w * 3 + 3) // 4) * 4

    extracted = bytearray()
    for i in range(0, len(pixels), row_padded):
        extracted.extend(pixels[i + (w * 3): i + row_padded])

    length = int.from_bytes(extracted[:4], "big")
    return extracted[4: 4 + length].decode()

while True:
    #dir = os.getcwd()
    img = input("enter image path: ")
    if not os.path.exists(img):
        print("path does not exist")
        continue


    choice = int(input("enter 1 to encode message 2 to decode message: "))
    if choice!= 1 and choice !=2:
        continue
    if choice ==1:
        method =  int(input("enter 1 to encode message with changing file size 2 to encode message without changing file size "))
        msg = input("enter msg to encode: ")
        if choice ==1:
            m1_encrypt_image(img,msg)
        elif choice ==2:
            m2_encrypt_image(img,msg)
        else:
            continue


    elif choice ==2:
        try:
            msg = m1_decrypt_img(img)
            print(msg)
            continue
        except Exception as e:
            print(e)

        try:
            msg = m2_decrypt_img(img)
            print(msg)
            continue
        except Exception as e:
            print(e)

