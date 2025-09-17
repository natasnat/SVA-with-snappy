import numpy as np
from esa_snappy import ProductIO, Product, ProductData, ProductUtils

# ----------------------------------------------------
# Spatially Variant Apodization (SVA) for SAR Images
# ----------------------------------------------------
#
# Description:
# 1️⃣ Compute the weighting function w_u(m, n):
#        w_u(m, n) = - I(m, n) / ( I(m-1, n) + I(m+1, n) + I(m, n-1) + I(m, n+1) )
#
# 2️⃣ Adjust pixel values based on w_u(m, n):
#        - If w_u(m, n) < 0   → Mainlobe is preserved
#        - If 0 ≤ w_u(m, n) ≤ 1/2 → Sidelobe is suppressed (Pixel = 0)
#        - If w_u(m, n) > 1/2  → Pixel is replaced with weighted neighbors
#
# 3️⃣ The method is applied separately for I (Real) and Q (Imaginary).
#
# Neighbors are in both azimuth and range directions considered.
#
# ----------------------------------------------------

# Load input product
file_path = "example_input.dim"  # <-- replace with your product path

product = ProductIO.readProduct(file_path)
if product is None:
    raise ValueError("Error: Product could not be loaded!")

print("Product successfully loaded!")

# Extract I and Q bands
band_I = product.getBand('i_IW2_VV')
band_Q = product.getBand('q_IW2_VV')

width, height = product.getSceneRasterWidth(), product.getSceneRasterHeight()

# Read pixel values as arrays
I = np.zeros((height, width), dtype=np.float32)
Q = np.zeros((height, width), dtype=np.float32)
band_I.readPixels(0, 0, width, height, I)
band_Q.readPixels(0, 0, width, height, Q)

# ------------------------------
# Weighting function computation
# ------------------------------
def calculate_w_2d(data):
    """
    Compute the weighting function w_u(m, n) based on 2D neighbors.

    Equation:
        w_u(m, n) = - I(m, n) / (I(m-1, n) + I(m+1, n) + I(m, n-1) + I(m, n+1))

    If neighbors are NaN, only valid values are used.
    """
    up = np.roll(data, shift=1, axis=0)
    down = np.roll(data, shift=-1, axis=0)
    left = np.roll(data, shift=1, axis=1)
    right = np.roll(data, shift=-1, axis=1)

    neighbors = np.nansum([up, down, left, right], axis=0)  # sum of valid neighbors
    with np.errstate(divide='ignore', invalid='ignore'):
        w = -data / neighbors  # compute w_u(m, n)

    return np.clip(w, 0, 0.5)  # limit to [0, 0.5]

# Compute weights for I and Q
w_I = calculate_w_2d(I)
w_Q = calculate_w_2d(Q)

# ------------------------------
# Apply SVA filter
# ------------------------------
def apply_sva_2d(data, w):
    """
    Apply the SVA filter to I or Q values.

    - If w_u(m, n) < 0 → mainlobe is preserved (value unchanged)
    - If 0 ≤ w_u(m, n) ≤ 1/2 → sidelobe suppressed (pixel set to 0)
    - If w_u(m, n) > 1/2 → pixel replaced with weighted neighbors

    If neighbors are NaN, only valid ones are used.
    """
    up = np.roll(data, shift=1, axis=0)
    down = np.roll(data, shift=-1, axis=0)
    left = np.roll(data, shift=1, axis=1)
    right = np.roll(data, shift=-1, axis=1)

    # Average of valid neighbors
    valid_neighbors = np.nansum([up, down, left, right], axis=0) / np.sum(
        ~np.isnan([up, down, left, right]), axis=0
    )

    # Initialize output
    filtered = np.full_like(data, np.nan)

    # Case 1: preserve mainlobe
    filtered[w <= 0] = data[w <= 0]

    # Case 2: suppress sidelobe
    filtered[(w > 0) & (w <= 0.5)] = 0

    # Case 3: replace with weighted neighbors
    filtered[w > 0.5] = data[w > 0.5] + 0.5 * valid_neighbors[w > 0.5]

    return filtered

# Apply filter to I and Q
I_w = apply_sva_2d(I, w_I)
Q_w = apply_sva_2d(Q, w_Q)
print("Shape I_w:", I_w.shape, "Shape Q_w:", Q_w.shape)

# ------------------------------
# Compute amplitude and intensity
# ------------------------------
intensity = I_w**2 + Q_w**2
amplitude = np.sqrt(intensity)

# ------------------------------
# Create output product
# ------------------------------
output_product = Product("SVA_Filtered", "Derived from (SLC)", width, height)
output_product.setDescription("Sentinel-1 IW Level-1 SLC Product")

# ProductWriter
writer = ProductIO.getProductWriter("BEAM-DIMAP")
output_product.setProductWriter(writer)

# Copy metadata
ProductUtils.copyMetadata(product, output_product)
ProductUtils.copyTiePointGrids(product, output_product)
output_product.setStartTime(product.getStartTime())
output_product.setEndTime(product.getEndTime())

# Add bands
I_w_band = output_product.addBand("i_IW2_VV", ProductData.TYPE_FLOAT32)
Q_w_band = output_product.addBand("q_IW2_VV", ProductData.TYPE_FLOAT32)
intensity_band = output_product.addBand("intensity", ProductData.TYPE_FLOAT32)
amplitude_band = output_product.addBand("amplitude", ProductData.TYPE_FLOAT32)

# Allocate storage
I_w_band.setRasterData(ProductData.createInstance(ProductData.TYPE_FLOAT32, width * height))
Q_w_band.setRasterData(ProductData.createInstance(ProductData.TYPE_FLOAT32, width * height))
intensity_band.setRasterData(ProductData.createInstance(ProductData.TYPE_FLOAT32, width * height))
amplitude_band.setRasterData(ProductData.createInstance(ProductData.TYPE_FLOAT32, width * height))

# Write pixels
I_w_band.setPixels(0, 0, width, height, I_w.flatten())
Q_w_band.setPixels(0, 0, width, height, Q_w.flatten())
intensity_band.setPixels(0, 0, width, height, intensity.flatten())
amplitude_band.setPixels(0, 0, width, height, amplitude.flatten())

# ------------------------------
# Save output product
# ------------------------------
output_path = "SVA_filtered_output"  # <-- set your desired output path (no extension)

# Write product (BEAM-DIMAP format: .dim + .data folder)
ProductIO.writeProduct(output_product, output_path, "BEAM-DIMAP")

print(f"✅ SVA-filtered product successfully saved to: {output_path}.dim")

