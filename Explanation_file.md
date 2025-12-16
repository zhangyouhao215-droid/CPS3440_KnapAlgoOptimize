# **Understanding the Knapsack Algorithm: From Standard 2D to Optimized 1D**

## **1\. The Scenario**

To understand the algorithm, we will manually solve a small problem.

The Mission:  
You have a backpack with a Capacity of 4kg.  
You need to choose from the following items to maximize the total value inside the backpack.  
**The Items:**

1. 🎸 **Guitar**: Weight **1kg**, Value **$15**  
2. 📻 **Stereo**: Weight **4kg**, Value **$30**  
3. 💻 **Laptop**: Weight **3kg**, Value **$20**

## **Part 1: Standard Solution (2D Dynamic Programming)**

**Concept:** Imagine filling a large Excel sheet.

* **Rows (**$i$**):** Represent the items available (0=None, 1=Guitar, 2=Stereo, 3=Laptop).  
* **Columns (**$w$**):** Represent the hypothetical capacity of the backpack (from 0kg to 4kg).  
* **Cell dp\[i\]\[w\]:** Stores the *maximum value* we can get using only the first $i$ items with capacity $w$.

### **Step 0: Initialization**

We create a table of size (n+1) x (capacity+1). Initially, it is filled with zeros.

| Item \\ Capacity | 0kg | 1kg | 2kg | 3kg | 4kg |
| :---- | :---- | :---- | :---- | :---- | :---- |
| **0 (None)** | 0 | 0 | 0 | 0 | 0 |
| **1 (Guitar)** | 0 | 0 | 0 | 0 | 0 |
| **2 (Stereo)** | 0 | 0 | 0 | 0 | 0 |
| **3 (Laptop)** | 0 | 0 | 0 | 0 | 0 |

### **Step 1: Processing Item 1 (Guitar) \- Weight 1, Value 15**

We iterate through all capacities ($w$ from 1 to 4).  
Since the guitar (1kg) fits in all capacities $\\ge$ 1kg, we calculate:

* **Value:** 15 \+ Value of remaining space (0) \= **15**.

| Item \\ Capacity | 0kg | 1kg | 2kg | 3kg | 4kg |
| :---- | :---- | :---- | :---- | :---- | :---- |
| **0 (None)** | 0 | 0 | 0 | 0 | 0 |
| **1 (Guitar)** | 0 | **15** | **15** | **15** | **15** |

### **Step 2: Processing Item 2 (Stereo) \- Weight 4, Value 30**

We decide: Do we keep the previous best value (Guitar), or do we switch to the Stereo?

* **For Capacity 1, 2, 3:** The Stereo (4kg) is too heavy. We must copy the value from the row above (15).  
* **For Capacity 4:**  
  * **Option A (Exclude Stereo):** Take value from row above $\\rightarrow$ **15**.  
  * **Option B (Include Stereo):** Value of Stereo (30) \+ Value of remaining space (4-4=0) from row above (0) $\\rightarrow$ 30 \+ 0 \= **30**.  
  * **Result:** 30 \> 15, so we choose **30**.

| Item \\ Capacity | 0kg | 1kg | 2kg | 3kg | 4kg |
| :---- | :---- | :---- | :---- | :---- | :---- |
| **1 (Guitar)** | 0 | 15 | 15 | 15 | 15 |
| **2 (Stereo)** | 0 | **15** | **15** | **15** | **30** |

### **Step 3: Processing Item 3 (Laptop) \- Weight 3, Value 20**

* **For Capacity 1, 2:** Laptop (3kg) is too heavy. Copy from above (15).  
* **For Capacity 3:** Laptop fits.  
  * Option A (Keep Stereo row): 15\.  
  * Option B (Take Laptop): 20 \+ dp\[2\]\[0\] (0) \= 20\.  
  * Result: **20** (Better than 15).  
* **For Capacity 4 (CRITICAL STEP):**  
  * **Option A (Exclude Laptop):** Keep previous best (Stereo) $\\rightarrow$ **30**.  
  * **Option B (Include Laptop):**  
    * Take Laptop (Value: **20**).  
    * Remaining Space: $4 \- 3 \= 1$kg.  
    * Check best value for 1kg from previous row (dp\[2\]\[1\]) $\\rightarrow$ **15** (Guitar).  
    * Total: 20 \+ 15 \= **35**.  
  * **Result:** 35 \> 30\. We update the cell to **35**.

| Item \\ Capacity | 0kg | 1kg | 2kg | 3kg | 4kg |
| :---- | :---- | :---- | :---- | :---- | :---- |
| **2 (Stereo)** | 0 | 15 | 15 | 15 | 30 |
| **3 (Laptop)** | 0 | **15** | **15** | **20** | **35** |

**Final Answer:** 35\.

## **Part 2: Optimized Solution (1D Dynamic Programming)**

Concept:  
Instead of a large table, we use a single row (array) representing the backpack's capacity. We constantly overwrite this row with new data.  
**Key Rule:** We must loop **backwards** (from Capacity 4 down to 0\) to avoid using the same item twice.

### **Initial State**

dp \= \[0, 0, 0, 0, 0\]

### **Round 1: Guitar (Weight 1, Value 15\)**

Loop backwards from 4 to 1\.

* dp\[4\]: max(0, 15 \+ dp\[3\]) $\\rightarrow$ 15  
* ...  
* dp\[1\]: max(0, 15 \+ dp\[0\]) $\\rightarrow$ 15

**Array:** \[0, 15, 15, 15, 15\]

### **Round 2: Stereo (Weight 4, Value 30\)**

Loop backwards from 4 down to 4\.

* w \= 4:  
  * **Old Value:** 15\.  
  * **New Value:** Stereo (30) \+ dp\[4-4\] (0) \= 30\.  
  * **Update:** 30 \> 15, so overwrite index 4 with 30\.

**Array:** \[0, 15, 15, 15, 30\]

### **Round 3: Laptop (Weight 3, Value 20\)**

Loop backwards from 4 down to 3\.

* **When w \= 4:**  
  * **Old Value:** 30 (Stereo).  
  * **New Value:** Laptop (20) \+ dp\[4-3\] (dp\[1\]).  
  * *Note:* dp\[1\] is currently **15** (Guitar from Round 1). We haven't touched it in this round yet.  
  * Calculation: 20 \+ 15 \= **35**.  
  * **Update:** Overwrite index 4 with 35\.  
* **When w \= 3:**  
  * **Old Value:** 15\.  
  * **New Value:** Laptop (20) \+ dp\[0\] (0) \= 20\.  
  * **Update:** Overwrite index 3 with 20\.

**Final Array:** \[0, 15, 15, 20, 35\]

**Final Answer:** dp\[4\] is **35**. (Same as 2D method\!)

## **Comparison Summary**

| Feature | 2D DP (Standard) | 1D DP (Optimized) |
| :---- | :---- | :---- |
| **Logic** | Fill a full grid | Overwrite a single array |
| **Memory** | High ($O(N \\times W)$) | Low ($O(W)$) |
| **Loop Direction** | Usually Forward (1 to W) | **Must be Backward** (W to 1\) |
| **Why Backward?** | N/A (Uses previous row) | To prevent "Double Counting" an item |

### **Why "Double Counting" Happens in Forward Loops (1D)**

If we looped **forward** (1 to 4\) for the Guitar (Value 15, Weight 1):

1. **At w=1:** We add Guitar. dp\[1\] \= 15\.  
2. **At w=2:** We calculate Guitar \+ dp\[1\]. Since dp\[1\] is now 15, we get 15 \+ 15 \= 30\.  
3. **Error:** The algorithm thinks we put **two guitars** in the bag\!

By looping **backwards**, when we calculate dp\[4\], we look at dp\[3\]. Since we haven't processed 3 yet in this round, dp\[3\] still holds the "old" data (without the current item), ensuring we only add the item once.
