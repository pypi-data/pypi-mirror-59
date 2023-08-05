# Python Vuetify Markdown

This is an extension for [Python-Markdown](https://github.com/Python-Markdown/markdown/) created for those who combine Python, Markdown, Vue, and Vuetify. I've been using this combination in several projects, and finally came across a need to process Markdown code, and keep it styled with Vuetify. Rather than McGuyver some solution in, I settled on a simple extension to do the heavy lifting.

The code is dead simple, and can be modified or extended to fit your needs. 

# Installation
For now, do it by hand. Load it into your project, add the extension when initializing Markdown, and it should work no problem. Once this is on PyPi, I'll change the docs to include pip installation.

# Features
Currently, this extension modifies H1 to H6 tags and P tags. The styles can be found on the [Vuetify Typography page](https://vuetifyjs.com/en/styles/typography).
* **&lt;h1&gt;** &rarr; &lt;h1 class="display-4"&gt;
* **&lt;h2&gt;** &rarr; &lt;h1 class="display-3"&gt;
* **&lt;h3&gt;** &rarr; &lt;h1 class="display-2"&gt;
* **&lt;h4&gt;** &rarr; &lt;h1 class="display-1"&gt;
* **&lt;h5&gt;** &rarr; &lt;h1 class="headline"&gt;
* **&lt;h6&gt;** &rarr; &lt;h1 class="title"&gt;
* **&lt;p&gt;** &rarr; &lt;h1 class="body-1"&gt;

# Support
There is none. This is a small side project, like 30 minutes of research and work went into it. Good luck.