import fitz
from PIL import Image, ImageDraw

PDF = "uploads/Adobe Scan 02 Aug 2026_removed.pdf"
PAGE = 0

#
# Starting coordinates
#

left = 0.21
top = 0.19
right = 0.60
bottom = 0.28

STEP = 0.002

doc = fitz.open(PDF)

page = doc.load_page(PAGE)

pix = page.get_pixmap(dpi=300)

base = Image.frombytes(
    "RGB",
    [pix.width, pix.height],
    pix.samples
)


def render():

    img = base.copy()

    draw = ImageDraw.Draw(img)

    w, h = img.size

    x1 = int(w * left)
    y1 = int(h * top)

    x2 = int(w * right)
    y2 = int(h * bottom)

    draw.rectangle(
        (x1, y1, x2, y2),
        outline="red",
        width=5
    )

    img.show()

    print()
    print("--------------------------------")
    print(f"LEFT   = {left:.3f}")
    print(f"TOP    = {top:.3f}")
    print(f"RIGHT  = {right:.3f}")
    print(f"BOTTOM = {bottom:.3f}")
    print("--------------------------------")


while True:

    render()

    key = input(
        "\nW/S=Up/Down  A/D=Left/Right\n"
        "I/K=Top Edge  J/L=Right Edge\n"
        "Z/X=Left Edge C/V=Bottom Edge\n"
        "P=Print  Q=Quit\n\n> "
    ).lower()

    if key == "w":
        top -= STEP
        bottom -= STEP

    elif key == "s":
        top += STEP
        bottom += STEP

    elif key == "a":
        left -= STEP
        right -= STEP

    elif key == "d":
        left += STEP
        right += STEP

    elif key == "i":
        top -= STEP

    elif key == "k":
        top += STEP

    elif key == "j":
        right -= STEP

    elif key == "l":
        right += STEP

    elif key == "z":
        left += STEP

    elif key == "x":
        left -= STEP

    elif key == "c":
        bottom -= STEP

    elif key == "v":
        bottom += STEP

    elif key == "p":

        print()

        print("===================================")
        print("COPY THIS")
        print("===================================")

        print("FLIGHT_BOX = (")

        print(f"    {left:.3f},")

        print(f"    {top:.3f},")

        print(f"    {right:.3f},")

        print(f"    {bottom:.3f},")

        print(")")

        print("===================================")

    elif key == "q":
        break