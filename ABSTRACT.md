In the **BRACOL: A Brazilian Arabica Coffee Leaf Images Dataset to Identification and Quantification of Coffee Diseases and Pests** authors describe the importance of addressing biotic stress, which involves harm to plants caused by living organisms such as pests and pathogens. It emphasizes the link between efficient control of biotic agents and agricultural sustainability, promoting the development of technologies for reduced environmental impact and increased productivity. The authors propose a multi-task system based on convolutional neural networks, incorporating data augmentation techniques to enhance robustness and accuracy, with experimental results suggesting the system's potential as a valuable tool for identifying and quantifying biotic stresses in coffee plantations.

The dataset created for this study comprises images of coffee leaves affected by major biotic stresses impacting the coffee tree. Captured with various smartphones (ASUS Zenfone 2, Xiaomi Redmi 5A, Xiaomi S2, Galaxy S8, and iPhone 6S), the images were collected at different times and locations in the state of Espírito Santo, Brazil. The photos were taken from the lower side of the leaves under partially controlled conditions against a white background, with acquisition intentionally varied to enhance dataset heterogeneity.

A comprehensive dataset comprising 1747 images of coffee leaves was assembled, encompassing both healthy and diseased leaves affected by various biotic stresses. Recognition and labeling of biotic stresses, including leaf miner, rust, brown leaf spot, and cercospora leaf spot, were facilitated by a specialist. Image below illustrates examples of images present in the dataset.

<img src="https://github.com/dataset-ninja/bracol/assets/115161827/20aa6f77-8f76-4416-891f-f51e6193b7df" alt="image" width="800">

<span style="font-size: smaller; font-style: italic;">Examples of coffee leaves affected by different biotic stresses: leaf miner (a), rust (b), brown leaft spot (c) and cercospora leaf
spot (d).</span>

Each image is classified with the following tags: **id** and **predominant_stress** and classes tags if present: **miner**, **rust**, **phoma** and **cercospora** along the **severity** tag that indicates how severe the disease is. If the leaf is healthy, a **healthy** tag is added to an image.

- **id** represnts image's id
- **predominant_stress** is the type of stress that is predominant on the leaf (0 if there is no stress, 1 is for **miner**, 2 is for **rust**, 3 is for **phoma**, 4 is for **cercospora**)
- **severity** is a range from 0-4, where labels were assigned as follows: healthy (< 0.1%), very low (0.1% − 5%), low (5.1% − 10%), high (10.1% − 15%) and very high (> 15%).