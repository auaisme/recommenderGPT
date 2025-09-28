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
However, with Deepseek, this later issue has not yet occurred, and it has a decently high consistency between responses.

# Reviews
We are using IGN's reviews to inform our comparison.
We don't care if they reviewer liked the game or not, we only care how similar the games' mechanics and feel are.
We are aware of the controversy around IGN reviews, and have considered using other sources, including YouTube reviews, to inform our LLM.
Some reviews may be very large and exceed our context limit for the LLM; in such a case, we will be using an LLM to either
* summarize the review
* inform the LLM in chunks

The latter is not preferred as the overall history may still exceed context limits.

# Sample Comparison
The following sample comparison was made using no summarization and Deepseek's v3 LLM.

### Red Dead Redemption 2 v Undertale

Score: 10/100

Reasoning: The games are fundamentally opposed in design philosophy, with Red Dead Redemption 2 being a massive, realistic open-world focused on immersion and a linear narrative, while Undertale is a small, meta-narrative RPG that subverts player expectations and integrates its mechanics directly into its storytelling. Their mechanics and target audiences share almost no overlap, making them vastly dissimilar experiences.


### Red Dead Redemption 2 v Cyberpunk 2077

Score: 35/100

Reasoning: While both are highly detailed, narrative-driven open-world games, their design philosophies, mechanics, and target audiences differ significantly. Red Dead Redemption 2 emphasizes a slow-paced, immersive simulation of a historical period with deliberate, grounded mechanics, whereas Cyberpunk 2077 is a faster-paced, choice-driven RPG focused on futuristic action and player agency in a dense, vertical cityscape.


### Red Dead Redemption 2 v Grand Theft Auto V

Score: 75

Reasoning: Both games share Rockstar's core open-world design philosophy of creating dense, living worlds and a mission-based structure, with similar core mechanics for combat, driving/riding, and interaction. However, RDR2's deliberate, slower pace, greater emphasis on realism and immersion, and its serious Western tone versus GTA V's satirical, modern commentary mark significant philosophical and mechanical differences, while their mature target audiences are nearly identical.


### Red Dead Redemption 2 v Grand Theft Auto IV

Score: 75/100

Reasoning: Both games share Rockstar's core design philosophy of creating immersive, narrative-driven open worlds with realistic mechanics and a mature tone, targeting a similar adult audience. However, RDR2's slower, more deliberate pace, emphasis on survival mechanics, and unique Western setting differentiate it significantly from GTA IV's urban crime focus.


### Red Dead Redemption 2 v Red Dead Redemption

Score: 85/100

Reasoning: Both games share Rockstar's core open-world design philosophy, mechanics like Dead Eye and bounty hunting, and target the same mature audience. However, RDR2's design is more deliberate and immersive, with slower-paced mechanics and a greater emphasis on a living world, making it a deeper but not identical evolution of its predecessor's philosophy.


### Undertale v Deltarune

Score: 85/100
Reasoning: Both games share a core design philosophy of subverting RPG expectations, integrating narrative with unique combat mechanics (like ACTing and dodging), and targeting an audience that appreciates meta-commentary and heartfelt, humorous writing. However, Deltarune expands on these ideas with a multi-chapter structure, a party-based system, and a new setting, making it a distinct evolution rather than a direct copy.


### Undertale v Cyberpunk 2077

Score: 15/100

Reasoning: While both are RPGs that value player choice, their core design philosophies are opposites. Undertale is a tightly crafted, meta-narrative that subverts RPG conventions to deliver a personal, morality-driven story, whereas Cyberpunk 2077 is a massive, open-world experience focused on player freedom and a dense, reactive city. Their mechanics, scale, and target audiences are vastly different.


### Undertale v Grand Theft Auto V

Score: 10/100
Reasoning: The games are fundamentally opposed in design philosophy and mechanics. Undertale is a meta-narrative RPG focused on player choice and morality with turn-based combat, while GTA V is a satirical open-world action game focused on freedom, chaos, and realistic scale. Their target audiences and core purposes are entirely different.


### Undertale v Grand Theft Auto IV

Score: 10/100
Reasoning: The games are fundamentally opposed in design philosophy, with Undertale being a meta-narrative RPG that subverts player expectations and integrates morality into its core mechanics, while GTA IV is a realistic open-world crime simulator focused on immersive storytelling and action. Their mechanics, from combat to world interaction, and their target audiences are vastly different.


### Undertale v Red Dead Redemption

Score: 10/100

Reasoning: The games are fundamentally dissimilar in philosophy and mechanics. Undertale is a meta-narrative RPG that subverts player expectations and integrates its mechanics directly into its storytelling, while Red Dead Redemption is a vast, open-world sandbox focused on immersive simulation and player freedom within a realistic setting. Their target audiences and core design goals are entirely different.

# Steam API
We will be building our games database using Steam's database.

List all apps: https://api.steampowered.com/ISteamApps/GetAppList/v2/

Get details about specific app: https://store.steampowered.com/api/appdetails?appids=PUT_YOUR_APP_ID_HERE

Web Page from where you can scrape all tags: https://store.steampowered.com/tag/browse/#global_492


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
