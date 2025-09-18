# RecommenderGPT
This algorithm uses RAG and LLM to provide an informed recommendation for products.

# RAG Pipeline
To perform RAG, we first identify the products in the query, find their reviews, and augment the query with said reviews.
We expect the final product to only name the products (games) that the user has used. From this, we will build a cummulative vector.
This vector will be used to find similar products by genre (current widely used technique).
After finding the similar products, we find their reviews and continue with the aforementioned pipeline.

# LLM Used
From our early testing, we have discovered that OpenAI's ChatGPT has performed the best so far.
However due to token and credit limits, we will be using Deepseek by default, which is the second best in our testing.
Claude and Gemini performed far below par.

# Limitations
Due to the nature of ML/DL, our LLM's comparison is not definitive, and there are possibilities of hallucinations.
Sometimes, despite having the appropriate context, the system may say that comparison isn't possible.
However, with Deepseek, this later issue has not yet occurred, and it has a decently high consistency in between responses.

# Reviews
We are using IGN's reviews to inform our comparison.
We don't care if they reviewer liked the game or not, we only care how similar the games' mechanics and feel are.
We are aware of the controversy around IGN reviews, and have considered using other sources, including YouTube reviews, to inform our LLM.
Some reviews may be very large and exceed our context limit for the LLM; in such a case, we will be using an LLM to either
* summarize the review
* inform the LLM in chunks
The latter is not preferred as the overall history may still exceed context limits.

# License
Exclusive Software License and Intellectual Property Notice

Copyright © 2025 CE Ali Usman. All Rights Reserved.

1. Ownership
All software, source code, object code, documentation, algorithms, designs, and related materials (collectively, the “Software” or "System" or "Algorithm") are the exclusive intellectual property of Ali Usman ("Owner").

2. Restrictions on Use
No individual, entity, or organization may copy, modify, distribute, sublicense, reverse engineer, decompile, disassemble, or otherwise use the Software in any manner without the prior explicit written permission of the Owner.

3. Enforcement
Any unauthorized use, reproduction, distribution, or exploitation of the Software constitutes a violation of copyright law and may subject the violator to civil and criminal penalties under applicable intellectual property laws.

4. License Grant
Upon receipt of a signed written agreement from the Owner, a license to use the Software may be granted under terms explicitly stated in such agreement. No implied licenses are granted by this notice.

5. Disclaimer
The Software is provided “as is,” without warranty of any kind, express or implied, including but not limited to any warranties of merchantability, fitness for a particular purpose, or non-infringement.

6. Governing Law
This License shall be governed by and construed in accordance with the laws of US, Pakistan, and Berne Convention. Any disputes arising under this License shall be subject to the exclusive jurisdiction of the courts located in Lahore, Pakistan.
