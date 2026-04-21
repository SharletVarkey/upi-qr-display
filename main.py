import board
import displayio
import adafruit_miniqr
import adafruit_ili9341
import busio
from fourwire import FourWire

# Release any resources currently in use for the displays
displayio.release_displays()

# ===== Display Configuration =====
disp_width  = 320
disp_height = 240
disp_cs     = board.IO7
disp_res    = board.IO9
disp_dc     = board.IO8
disp_mosi   = board.IO6
disp_clk    = board.IO10

disp_spi = busio.SPI(clock=disp_clk, MOSI=disp_mosi)
display_bus = FourWire(
    disp_spi,
    command=disp_dc,
    chip_select=disp_cs,
    reset=disp_res
)
display = adafruit_ili9341.ILI9341(display_bus, width=disp_width, height=disp_height)
# ==================================


def bitmap_QR(matrix):
    """Convert a QR matrix into a scaled displayio Bitmap."""
    BORDER_PIXELS = 2
    max_scale_x = disp_width  // (matrix.width  + 2 * BORDER_PIXELS)
    max_scale_y = disp_height // (matrix.height + 2 * BORDER_PIXELS)
    SCALE = min(max_scale_x, max_scale_y)
    size = (matrix.width + 2 * BORDER_PIXELS) * SCALE
    bitmap = displayio.Bitmap(size, size, 2)
    for y in range(matrix.height):
        for x in range(matrix.width):
            color = 1 if matrix[x, y] else 0
            for dy in range(SCALE):
                for dx in range(SCALE):
                    bitmap[(x + BORDER_PIXELS) * SCALE + dx,
                           (y + BORDER_PIXELS) * SCALE + dy] = color
    return bitmap


def show_qr(amount):
    """Generate and display a UPI QR code for the given amount."""
    # Build UPI deep link
    upi_link = (
        f"upi://pay?pa=yash8hajare@oksbi"
        f"&pn=Yash%20Hajare"
        f"&am={amount}"
        f"&cu=INR"
        f"&aid=uGICAgICtr4_LFQ"
    )

    # Generate QR code
    qr = adafruit_miniqr.QRCode(qr_type=7, error_correct=adafruit_miniqr.L)
    qr.add_data(upi_link.encode('utf-8'))
    qr.make()

    # Convert to scaled bitmap
    qr_bitmap = bitmap_QR(qr.matrix)

    # Color palette: purple background, cyan QR modules
    palette = displayio.Palette(2)
    palette[0] = 0x800080  # Background
    palette[1] = 0x00FFFF  # QR code

    # Center QR on screen
    pos_x = (disp_width  - qr_bitmap.width)  // 2
    pos_y = (disp_height - qr_bitmap.height) // 2

    qr_img = displayio.TileGrid(qr_bitmap, pixel_shader=palette, x=pos_x, y=pos_y)
    splash = displayio.Group()
    splash.append(qr_img)
    display.root_group = splash


# ===== Main Loop =====
while True:
    try:
        amount = input("Enter amount (INR): ").strip()

        if not amount.replace('.', '', 1).isdigit():
            print("❌ Invalid input. Please enter a numeric amount.")
            continue

        show_qr(amount)
        print(f"✅ QR code updated for ₹{amount}!")

    except KeyboardInterrupt:
        print("Exiting...")
        break
