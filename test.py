import numpy as np

data = np.array([
    [2, 3],
    [4, 5],
    [6, 7]
])

print("--- Data Awal ---")
print(data)

mean_vector = np.mean(data, axis=0)
print(f"\nRata-rata (Mean): {mean_vector}") 

X_centered = data - mean_vector
print("\nData setelah Centering (X):")
print(X_centered)

X_T = X_centered.T 

M = np.dot(X_T, X_centered)

print("\n--- Matriks Kovarians (M) ---")
print(M)

eigenvalues, eigenvectors = np.linalg.eig(M)

print("\n--- Hasil Eigen ---")
for i in range(len(eigenvalues)):
    print(f"Eigenvalue {i+1}: {eigenvalues[i]:.2f}")
    print(f"Eigenvector {i+1}: {eigenvectors[:, i]}")

idx_max = np.argmax(eigenvalues)
lambda_max = eigenvalues[idx_max]
pc1_vector = eigenvectors[:, idx_max]

print(f"\nBasis Baru: {pc1_vector}")

print("\n--- Testing Data Baru (Siswa D) ---")

# Data Baru: Mat=5, Fis=6
siswa_D = np.array([5, 6])
print(f"Nilai Asli Siswa D: {siswa_D}")

siswa_D_centered = siswa_D - mean_vector
print(f"Siswa D (Centered): {siswa_D_centered}") 

skor_pca = np.dot(siswa_D_centered, pc1_vector)

print(f"\nHASIL AKHIR PCA1: {skor_pca:.4f}")