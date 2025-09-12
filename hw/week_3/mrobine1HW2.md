# Homework Assignment No. 2
**Title:** Prompt Engineering and Distant Writing

---

### Part 1: Reconstruct Your Reflection (Explicit Prompting)

#### User Prompt 1
I want to set up some context here. Are you familiar with the Borges' The Library of Babel? If so would you be able to contextualize it for an NLP course.

**Commentary:** The idea here is to establish context.

#### Copilot Response 1 

Absolutely, Michael — Borges’ *The Library of Babel* is a brilliant and rich metaphor that can be contextualized in fascinating ways for an NLP course. Here's a breakdown of how we can frame it:

---

### **Overview of Borges’ "The Library of Babel"**

In this short story, Borges imagines a universe composed of an infinite library containing every possible 410-page book made up of a fixed set of characters. Most of the books are nonsensical, but among them are all possible combinations — including coherent texts, false truths, and even the catalog of the library itself.

The story explores themes of:

- **Infinity and randomness**
- **Search and meaning**
- **Information vs. knowledge**
- **Epistemology and despair**

---

### **Contextualizing for NLP**

You can use *The Library of Babel* as a conceptual springboard to discuss several key NLP topics:

#### **1. Combinatorics and Language Space**
- The library is a metaphor for the **combinatorial explosion** of possible texts.
- In NLP, we deal with **language models** that try to navigate this space intelligently.
- You can compare Borges’ random generation with **probabilistic models** like n-grams or transformers that assign likelihoods to sequences.

#### **2. Information Retrieval**
- The story’s inhabitants search for meaningful texts in a sea of noise — akin to **search engines** or **semantic retrieval systems**.
- This leads to discussions on **vector embeddings**, **semantic similarity**, and **ranking algorithms**.

#### **3. Language Modeling and Generative AI**
- Borges’ library contains all possible texts — similar to how large language models can generate coherent text from a vast latent space.
- You can explore how models like GPT differ from random generation by learning **statistical patterns** from real data.

#### **4. Meaning and Semantics**
- The despair of the librarians mirrors the challenge of **semantic understanding** in NLP.
- Introduce **distributional semantics**, **word embeddings**, and **contextual meaning** (e.g., BERT).

#### **5. Noise vs. Signal**
- Most books in the library are gibberish — a great analogy for **data preprocessing**, **tokenization**, and **filtering noise** in NLP pipelines.

#### **6. Ethics and Epistemology**
- Borges touches on the danger of misinformation and the futility of absolute truth.
- This can segue into **bias in language models**, **hallucinations**, and **truthfulness in AI-generated content**.

#### User Prompt 2
I am interested in answering this question. What does the Library of Babel say about the nature of language and meaning?

The response should be 2-3 sentences.

Also, I want to be sure to capture my tone and style of writing. To do so I will provide some writing samples. 

**Sample 1:**
> I know this work was published in 1941, but I couldn't stop drawing comparisons to the current moment. While I am not at all certain this was the intention, it felt prescient to me. The library conjured for me the internet. Both seem to contain a nearly endless (but not quite) landscape of information filled with wisdom and gibberish. One thing I found interesting about the library is that there seemed to be no framework for validation - no scientific method, no experimentation, only random strings that may or may not come together to convey some kind of idea. This is where it significantly differs from the internet. However, we have all the same issues despite all of our tools for validating information and critical thinking skills. Another comparison one could make, if so inclined, is that we may become somewhat like those in the library in that through recommendation algorithms we tend to not stray too far from our home hexagon.
> 
> I suppose I should think about this in the context of NLP as well. It seems logical to connect the challenges mentioned in my class notes above. If you imagine the library as the training corpus, you would have to make sense of repeating nonsense like M C V, endless noise and contradiction. Maybe the idea is that language in all its glory will always lead to issues of context and ambiguity. 

**Sample 2:**
> I found this dataset in the 2025.07.16 edition of "Data is Plural". This selection looks at "legal decisions in cases where generative AI produced hallucinated content - typically fake citations, but also other types of arguments." I find adoption of AI to be a crucial topic in all settings - professional, educational, etc. However, I found this dataset to be exceptionally interesting given that legal proceedings are typically environments of rigorous preparation. In infiltrating this environment, it really gets at the heart of the idea that AI might be reducing the quality of human thought and work.

**Commentary:** Here I provide a few-shot prompt to help it achieve a similar tone and style. Sample one is from a journal entry in which I explore The Library immediately after a first read. Sample 2 is just a description of a dataset for DS1. I suppose it's a bit of a meta prompt as well in that I provide guidelines in how to structure the response.

#### Copilot Response 2
Thanks for sharing your writing samples — they're thoughtful, reflective, and nuanced, with a clear voice that blends curiosity, skepticism, and a touch of philosophical inquiry. Based on that tone and style, here's a 2–3 sentence response to the question:

#### User Prompt 3
The second line there is perfect. I think the first sentence could be made stronger by adding a quote from the story to support this idea. You are arriving at the idea of combining symbols in all the possible ways doesn't "guarantee meaning" and there are some good quotes in the story about the combining of symbols.

**Commentary:** Already Copilot has managed to capture something close to the idea I was going for. From here it's a matter of shape prompting.

#### Copilot Response 3 

Great — here’s a revised version of your response, now incorporating a quote from *The Library of Babel* that directly supports the idea that combining symbols doesn’t guarantee meaning:

---

**What does *The Library of Babel* say about the nature of language and meaning?**

Borges writes, *“That this book contains an understandable phrase does not necessarily mean anything. It is one of an endless recombination of spaces and letters that happens to be able to be read.”*[1](https://www.sparknotes.com/short-stories/the-library-of-babel/key-quotes/) This underscores the idea that language alone doesn’t guarantee meaning — it’s just structure, endlessly combinable. Meaning arises only through interpretation, context, and shared understanding, which makes it both elusive and deeply human.

---

**What does *The Library of Babel* say about the nature of language and meaning?**

Borges’ library suggests that language, in its purest form, is both infinite and indifferent — capable of producing every possible combination of symbols, but utterly unconcerned with whether those combinations convey meaning. It’s a reminder that meaning isn’t inherent in language itself, but emerges through context, interpretation, and shared understanding — all of which are fragile, human constructs. In that sense, the story feels eerily relevant to NLP, where the challenge is not generating language, but discerning what (if anything) it means.

#### User Prompt 4
I was thinking about how the library contains "all possible combinations of the twenty-two orthographic symbols". Maybe we could use that to support "Borges suggests that language alone doesn't guarantee meaning" suggesting that meaning does not emerge out of combinatorics or even language alone. I like sentence 2 a lot.

**Commentary:** I wasn't able to track down the quote from the response above. Also, I figured for this kind of explicit exercise it would be fine to provide quotes and guidance on how to use them.

#### Copilot Response 4 

Perfect — here’s a refined version that integrates the quote about the orthographic symbols and sharpens the first sentence to support your idea more directly:

---

**What does *The Library of Babel* say about the nature of language and meaning?**

Borges describes the library as containing *“all possible combinations of the twenty-two orthographic symbols,”* suggesting that language alone — even in its most exhaustive form — doesn’t guarantee meaning. Meaning arises only through interpretation, context, and shared understanding, which makes it both elusive and deeply human.

---

Let me know if you'd like to add a reference to NLP or keep it purely literary/philosophical.

### Part 2: Say it without saying it (Implicit Prompting)

#### User Prompt 1
Are you familiar with Barney the dinosaur?

**Commentary:** The idea here is nothing more than the power of suggestion.

#### Copilot Response 1
Yes, I'm familiar with Barney the Dinosaur! He's the big, friendly purple dinosaur from the children's television show Barney & Friends, which originally aired in the early 1990s. The show was designed to teach young children educational and moral lessons through songs, dance, and storytelling. Barney is known for his cheerful personality, his signature song "I Love You", and his interactions with a cast of kids and other dinosaur characters like Baby Bop and BJ.

Are you asking about Barney for nostalgia, research, or something creative?

#### User Prompt 2
What do Barney the Dinosaur and sweet potatoes have in common?

**Commentary:** Given Copilot associates Barney with purple in the response above I figured this would be something worth exploring, but I didn't anticipate it going this well!

#### Copilot Response 2
That’s a delightfully quirky question! Let’s explore what **Barney the Dinosaur** and **sweet potatoes** might have in common:

### 🟣 1. **Color Connection**
- **Barney** is famously purple.
- **Purple sweet potatoes** (like Okinawan or Stokes varieties) share that vibrant hue. So, they’re both purple and visually striking!

### 🌱 2. **Wholesome & Friendly**
- Barney promotes **kindness, sharing, and learning**—all wholesome values.
- Sweet potatoes are considered a **nutritious, wholesome food**, often associated with comfort and health.

### 🎶 3. **Popular with Kids**
- Barney is a beloved children’s character.
- Sweet potatoes are often used in kid-friendly meals—mashed, baked, or turned into fries—making them a hit with little ones too.

### 🌎 4. **Global Appeal**
- Barney aired in many countries and was adapted for international audiences.
- Sweet potatoes are grown and enjoyed worldwide, from the U.S. to Asia to Africa.

### 🧠 5. **Educational Value**
- Barney teaches lessons through songs and stories.
- Sweet potatoes are often used in **nutrition education** to teach kids about healthy eating.

Would you like a silly poem or cartoon-style image combining the two? I’d be happy to whip one up!

#### User Prompt 3
That's an interesting point you make in part 1 above. If you were ignoring all specifics and talking about a singular sweet potato, how might you phrase that?

**Commentary:** From here it was just a matter of shaping the response.

#### Copilot Response 3

If we’re ignoring all specifics and talking about a **singular sweet potato**, you could phrase the connection like this:

> “A sweet potato, like Barney the Dinosaur, can be purple.”

It’s a simple, direct statement that highlights the shared trait without diving into varieties or context. If you want to make it a bit more playful or poetic, you could say:

> “Both Barney and a sweet potato can wear the color purple with pride.”

Would you like to explore more whimsical comparisons like this?

#### User Prompt 4
Let's ignore Barney and just focus on the sweet potato. Strip it of all literary flare. I just want to know how you would state the facts there.

**Commentary:** A thought I had here is how the amount of extra information an LLM might add is determined in response training. In the response above I am thinking about how it associates purple with pride. I digress! Look at the response below in all its glory!

#### Copilot Response 4
Here’s a stripped-down, factual statement:

> A sweet potato can be purple.

Let me know if you want to build on that or explore other traits.

---

**Model Information**
- Model Used: Microsoft Copilot (based on OpenAI's GPT-4 architecture)
- Date of Interaction: September 11, 2025
- Location Context: Burlington, Vermont, United States
- User: Michael Robinette


### Citation
> Robinette, M. (2025, September 11). *Creative reflection and ranking of sample texts using Microsoft Copilot (GPT-4)* [AI-assisted writing]. Microsoft Copilot. https://copilot.microsoft.com

---

## Part 3: Reflection

### P3Q1 - Reflection
For reconstruction, I chose to work with **P1Q1** from assignment 1. This was an interesting in that it was retroactive, and I can't help but wonder how it may have been different if this had not been the case. If I had not had a very clear idea about what I wanted to convey I can see how my thinking could have been completely highjacked by the LLM. Its response to my initial response was so thorough and convincing it's tempting to characterize it as thoughtful. However, in coming to this work with a clear and direct intention I was able to center the LLM around a theme - Information vs. knowledge and focus on the spirit and tone of my writing rather than the development of my ideas. This distinction is something I really want to reflect on as I move forward - the generation and development of ideas versus the shaping of language around my own ideas. A question I have, and I am not at all sure how to answer is to what degree can we trust LLMs to help us develop ideas.

One other idea I had in this exercise is the importance of drawing one's on analogies and conclusions even if they are completely unoriginal. When the LLM cranked out the themes we could highlight in this work in seconds, I thought of the training data from which the response was derived, and all the thinkers that came before me. There is something "deeply human" about this act of interpreting, contextualizing, and sharing in the understanding of all that language has to offer.

### P3Q1 - Technical Details
I used Microsoft Copilot. The complete details are in the citation above. In this explicit prompting exercise I had success in using a combination of zero-shot and few-shot/meta prompts followed by what I would call shaping prompts. The main idea that meaning comes from human interaction with language is clearly present in the distant writing. The results are below.

**Original:**
> Borges' work suggests that language and meaning are not a numbers game. In containing "all possible combinations of the twenty-two orthographic symbols" the library contained far more nonsense than rational thought. For language to have meaning, language requires the human touch, which brings structure, intention, and context.

**Result:**
> Borges describes the library as containing "all possible combinations of the twenty-two orthographic symbols," suggesting that language alone — even in its most exhaustive form — doesn't guarantee meaning. Meaning arises only through interpretation, context, and shared understanding, which makes it both elusive and deeply human.

### P3Q2
In the implicit prompting exercise, I used the same LLM as instructed and a combination of contextual association and cultural hook, and the results were eerily fantastic. I went from an "Are you familiar with Barney the dinosaur?" prompt to the desired response of "A sweet potato can be purple." in four interactions. What's really compelling about this exchange is the effectiveness of Barney as cultural hook given the age of the reference and its targeted demographic. It gets at something quite interesting about context and cultural events/icons and that is the notion of their weight and duration. Less significant cultural events and icons might disappear in human discourse, but remain in the memory of LLMs.

### P3Q3
Distant and close writing each comes with its own set of challenges. However, the challenges of close writing are something I am far more familiar with, and I think this is important. For distant writing to be productive the human in the loop needs to truly own the architect role. In this way it should be a process more focused on crafting the articulation of ideas rather than developing ideas.

After engaging in this process there is one question that will keep me up at night. What happens if we lean on these tools too heavily for both interpretation and communication? It's not hard to imagine a world in which human interaction is reduced to prompt engineering. This greatly underscores the importance of education around the usage of these tools - specifically around healthy and productive usage.