import qrcode, shutil, os
 
def qr_code(gr_code):
    print(gr_code)
    img = qrcode.make(gr_code)
    img.save(f'{gr_code}.png')
    source = f"{os.getcwd()}/{gr_code}.png"
    destination = f"{os.getcwd()}/Media/qrcodes/{gr_code}.png"
    shutil.copyfile(source, destination)
    os.remove(source)
