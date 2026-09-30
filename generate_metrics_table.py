from print_scan_simulator import PrintScanSimulator
import cv2
import pandas as pd

print("=" * 70)
print("ROBUSTNESS METRICS TABLE")
print("=" * 70)

# Load the same test image used for robustness testing
image = cv2.imread("robustness_original.png")

if image is None:
    print("ERROR: robustness_original.png not found.")
    exit()

simulator = PrintScanSimulator()

# Run robustness tests
results = simulator.test_robustness(image)

# Prepare table data
rows = []

for test_name, result in results.items():

    rows.append({
        "Test": test_name,
        "PSNR (dB)": round(result["psnr"], 2),
        "SSIM": round(result["ssim"], 4)
    })

# Create DataFrame
df = pd.DataFrame(rows)

print("\n")
print(df.to_string(index=False))

# Save CSV
df.to_csv("robustness_metrics.csv", index=False)

print("\n" + "=" * 70)
print("Metrics table saved:")
print("robustness_metrics.csv")
print("=" * 70)