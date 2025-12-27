-- Lists all bands with Glam rock as their main style, ranked by longevity up to 2024

SELECT
  band_name,
  CAST(COALESCE(split, 2024) - COALESCE(formed, 0) AS SIGNED) AS lifespan
FROM metal_bands
WHERE TRIM(style) = 'Glam rock'
ORDER BY lifespan DESC, band_name ASC;
