# How the Negative Control Process Works

Given an **image** and a **mask**, the creation of a negative control image 
involves a sequence of operations that utilize the provided `RegionStrategy` 
and `NegativeControlStrategy`. Here's a step-by-step explanation of the process:

---

### 1. Input Data
You provide:
- **image**: This is the input image, either a SimpleITK `Image` or a 
  numpy `ndarray`.
- **mask**: An optional mask (numpy array or SimpleITK image) defining 
  regions of interest (ROI) within the image.
- **region strategy**: Defines where the negative control is applied (e.g., full image,
  ROI only, outside ROI).
- **negative control strategy**: Specifies how pixel values in the image 
  are transformed (e.g., shuffled, randomized).

---

### 2. The `__call__` Method of `NegativeControlStrategy`
- You invoke the negative control strategy object like a function:
  
    ```python
    negative_control(image, mask=mask, region=region)
    ```
  
- This triggers the `__call__` method of the `NegativeControlStrategy` class.

---

### 3. Converting Inputs to Numpy Arrays
- The `__call__` method converts the **image** and **mask** into numpy arrays 
  (if they are SimpleITK images) using the `to_array()` function.

---

### 4. Applying the Region Strategy
- If both a **mask** and a **region strategy** are provided:
  
    ```python
    region_mask = region(image_array, mask_array)
    ```
  
  - This generates a binary mask (`region_mask`), defining which pixels 
    in the image are part of the region.

---

### 5. Selecting Pixels Based on the Region
- Non-zero pixels in `region_mask` indicate the region where the negative 
  control will be applied. The corresponding pixel indices are extracted:
  
    ```python
    mask_indices = np.nonzero(region_mask)
    ```
  
- The pixel values at these indices are flattened and isolated for 
  transformation:
  
    ```python
    flat_region_values = image_array[mask_indices]
    ```

---

### 6. Applying the Negative Control Transformation
- The `transform()` method of the `NegativeControlStrategy` subclass 
  is called:
  
    ```python
    transformed_values = self.transform(flat_region_values)
    ```
  
- This method performs the specific transformation (e.g., shuffling, 
  randomizing) which needs to be implemented in the subclass. 

---

### 7. Updating the Image
- The transformed pixel values are re-assigned to their corresponding 
  positions in the image array:
  
    ```python
    image_array[mask_indices] = transformed_values
    ```

---

### 8. Handling the Entire Image (if No Mask or Region Provided)
- If no **mask** or **region** is provided, the entire image is transformed:
  
    ```python
    image_array = self.transform(image_array)
    ```

---

### 9. Converting Back to SimpleITK (if Needed)
- If the input was a SimpleITK `Image`, the transformed numpy array is 
  converted back:
  
    ```python
    transformed_image = sitk.GetImageFromArray(image_array)
    transformed_image.CopyInformation(image)
    ```
- The final transformed image is returned, either as a SimpleITK image or 
  a numpy array, depending on the input type.

---

### Summary
- `RegionStrategy`: Defines which part of the image to transform.
- `NegativeControlStrategy`: Defines how pixel values are altered.
- The sequence:
  1. Extract region using `region`.
  2. Apply transformation using `negative_control`.
  3. Update the original image with transformed values.

This modular design ensures flexibility, allowing easy addition of new 
region or negative control strategies.