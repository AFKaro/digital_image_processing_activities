def select_image(img_num: int) -> any:
    new_img = f"./src/archives/lena.png"

    if img_num == 1:
        new_img = f"./src/archives/lena.png"
    elif img_num == 2:
        new_img = f"./src/archives/airplane.png"
    elif img_num == 3:
        new_img = f"./src/archives/baboon.png"
    elif img_num == 4:
        new_img = f"./src/archives/fruits.png"
    elif img_num == 5:
        new_img = f"./src/archives/peppers.png"
    elif img_num == 6:
        new_img = f"./src/archives/fazenda.jpg"
    elif img_num == 7:
        new_img = f"./src/archives/mergulhador.jpg"
    elif img_num == 8:
        new_img = f"./src/archives/mapa.jpg"
    elif img_num == 9:
        new_img = f"./src/archives/digital.jpg"
    
    return new_img